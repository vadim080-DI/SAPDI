try:
    api
except Exception as e:
    from pyop_api_mock import API
    api = API()
    api.config.encoding = "utf-8"
    api.config.in_format = "csv"
    api.config.out_format = "csv"
    api.config.in_properties = {"header": -1}
    api.config.out_properties = {}


# ///////////////////////////////////////////////////////////

import pandas as pd
import numpy as np

def on_dataframe(df, ctx):
    api.logger.info(df)

    # do something

    ctx.send(df, {"foo": "bar"})
    #api.send("output", api.Message(df))
    #ctx.done()

# //////////////////////////////////////////////////////////

def get_prop(name, default_value):
    if hasattr(api.config, name):
        return getattr(api.config, name)
    return default_value

in_format = get_prop("in_format", "CSV")
out_format = get_prop("out_format", "CSV")
in_properties = get_prop("in_properties", { "header": -1 })
out_properties = get_prop("out_properties", {})

from operators.com.sap.datatools.util.pdutil import OpContext
ctx = OpContext(api,
        on_dataframe,
        "output",
        in_format=in_format,
        out_format=out_format,
        in_properties=in_properties,
        out_properties=out_properties)

def on_input(msg):
    ctx.process(msg)

api.set_port_callback("input", on_input)


# //////////////////////////////////////////////////////////

if __name__ == "__main__" and hasattr(api, "test"):
    test_csv = "aaa,2019-01-01,3.3\nbbb,2019-01-02,6"
    for i in range(100):
        inmsg = api.Message(test_csv, {"foo": 1, "idx": i})
        api.test.write("input", inmsg)
        outmsg = api.test.read("output")
        print(outmsg.attributes["idx"])
        print(outmsg.body)
