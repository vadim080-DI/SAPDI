import pandas as pd
import numpy as np
import json

pandas_mapping = {
    "int": np.int32,
    "long": np.int64,
    "float": np.float32,
    "double": np.float64,
    "bytes": np.bytes_,
    "fixed": np.bytes_,
    "boolean": np.bool,
    "string": np.unicode,
    "decimal": np.float64
}


def to_readcsv_params(avro_schema):
    schema = avro_schema
    if avro_schema != None:
        if type(avro_schema) == str:
            schema = json.loads(avro_schema)
        elif type(avro_schema) == dict:
            schema = avro_schema
        else:
            raise ValueError("not a valid avro_schema")

    # default pandas attributes
    names = None
    dtypes = None
    parse_dates = None
    if not schema:
        return names, dtypes, parse_dates

    names = []
    dtypes = {}
    parse_dates = []

    def parse_field(f):
        name = f["name"]
        names.append(name)
        avrotype = f["type"]
        # handle 'dtype', '[null, dtype]'
        # and '[dtype, null]' case
        if type(avrotype) == list:
            if len(avrotype) == 1:
                avrotype == avrotype[0]
            elif avrotype[0] == "null":
                avrotype = avrotype[1]
            else:
                avrotype = avrotype[0]
        # convert logical types
        # TODO: do not handle time as datetime
        if avrotype in ("long", "int") and "logicalType" in f:
            if f["logicalType"].startswith("time") or \
               f["logicalType"].startswith("date"):
                parse_dates.append(name)
        else:
            dtypes[name] = pandas_mapping[avrotype]

    try:
        for f in schema["fields"]:
            parse_field(f)
    except Exception as e:
        raise ValueError("cannot convert avro_schema: %s" % e)

    return names, dtypes, parse_dates


# ////////////////////////////////////////////
test_schema1 = None
test_schema2 = """\
{
    "name": "foo",
    "type": "record",
    "namespace": "foo",
    "doc": "foo",
    "fields": [
        {
            "name": "orderid",
            "type": "string",
            "primaryKey": true
        },
        {
            "name": "dt",
            "type": "long",
            "logicalType": "timestamp-millis"
        },
        {
            "name": "userid",
            "type": "string"
        },
        {
            "name": "email",
            "type": "string"
        },
        {
            "name": "productid",
            "type": "string"
        },
        {
            "name": "amount",
            "type": "int"
        },
        {
            "name": "currency",
            "type": "string"
        },
        {
            "name": "price",
            "type": "float"
        }
    ]
}"""

test_schema3 = {
    "fields": [{
        "name": "orderid",
        "type": "string",
        "primaryKey": True
    }, {
        "name": "dt",
        "type": "long",
        "logicalType": "timestamp-millis"
    }]
}

if __name__ == "__main__":
    import io

    def check(test_schema):
        names, dtypes, parse_dates = to_readcsv_params(test_schema)
        print("names:      ", names)
        print("dtypes:     ", dtypes)
        print("parse_dates:", parse_dates)
        #df = pd.read_csv(io.StringIO(""), header=-1, names=names, dtype=dtypes, parse_dates=parse_dates)
        df = pd.read_csv(io.StringIO(
            "o001,2019-01-01 00:00:01,u001,bla@mail.tld,p001,2,EUR,10.12"),
                         header=-1,
                         names=names,
                         dtype=dtypes,
                         parse_dates=parse_dates)
        df_stringify_names(df)
        pqio = io.BytesIO()
        df.to_parquet(pqio)
        pqio.seek(0)
        df2 = pd.read_parquet(pqio)
        print(df2.dtypes)

    check(test_schema1)
    check(test_schema2)
    #check(test_schema3)
