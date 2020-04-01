import pandas as pd
import io
import time

def stringify_names(df):
    scols = []
    for col in df.columns:
        if type(col) != str:
            scols.append("c%s" % str(col))
        else:
            scols.append(col)
    df.columns = scols
    return df


def loads(data, fmt, **args):
    fmt = fmt.lower()
    if fmt == "parquet":
        bio = io.BytesIO(data)
        df = pd.read_parquet(bio, **args)
        return df
    elif fmt == "json":
        df = pd.read_json(data, **args)
        return df
    elif fmt == "csv":
        if type(data) == bytes:
            data = data.decode("utf-8", "ignore")
        sio = io.StringIO(data)
        df = pd.read_csv(sio, **args)
        return df
    else:
        raise ValueError("do not know format")


def dumps(df, fmt, **args):
    fmt = fmt.lower()
    if fmt == "parquet":
        bio = io.BytesIO()
        df.to_parquet(bio, **args)
        bio.seek(0)
        return bio.read()
    elif fmt == "json":
        return df.to_json(**args)
    elif fmt == "csv":
        sio = io.StringIO()
        df.to_csv(sio, **args)
        sio.seek(0)
        return sio.read()
    else:
        raise ValueError("do not know format")


class OpContext:
    def __init__(self,
                 api,
                 on_dataframe,
                 outport="output",
                 in_format="csv",
                 out_format="csv",
                 in_properties={},
                 out_properties={}):
        self.msg = None
        self.api = api
        self.on_dataframe = on_dataframe
        self.outport = outport
        self.in_format = in_format
        self.out_format = out_format
        self.in_props = in_properties
        self.out_props = out_properties

    def send(self, df, attr={}, fmt=None, **args):
        assert self.msg != None
        attr.update(self.msg.attributes)

        if fmt == None:
            fmt = self.out_format

        out_props = self.out_props.copy()
        out_props.update(args)
        self.api.logger.debug("output properties: %s" % str(out_props))

        data = dumps(df, fmt, **out_props)
        self.api.send(self.outport, self.api.Message(data, attr))
        self.done()

    def done(self):
        assert self.msg != None
        self.msg = None

    def process(self, msg):
        self._register_and_block(msg)
        df = self._parse_df(msg.body)
        self.on_dataframe(df, self)

    def _register_and_block(self, msg):
        while self.msg != None:
            time.sleep(0.05)
        self.msg = msg

    def _parse_df(self, data):
        self.api.logger.debug("input properties: %s" % str(self.in_props))
        df = loads(data, self.in_format, **self.in_props)
        return df


# //////////////////////////////////////////////


def test_df(csvdata="0,1,2\n3,4,5\n"):
    sio = io.StringIO(csvdata)
    df = pd.read_csv(sio, header=-1)
    return df


def test_stringify_names():
    df = test_df()
    assert (type(df.columns[0]) != str)
    stringify_names(df)
    assert (type(df.columns[0]) == str)
    print("done")


def test_opcontext():
    from pyop_api_mock import API
    api = API()

    test_csv = "aaa,2019-01-01,1.1\nbbb,2019-01-02,2"

    def on_dataframe(df, ctx):
        ctx.send(df, {"foo2": 2})

    ctx = OpContext(api,
                    on_dataframe,
                    "output",
                    in_properties={"header": -1},
                    out_properties={
                        "header": False,
                        "index": False
                    })
    ctx.process(api.Message(test_csv, {"foo1": 1}))
    msg = api.test.read("output")
    print(msg.attributes)
    print(msg.body)


if __name__ == "__main__":
    test_stringify_names()
    test_opcontext()
