try:
    api
except Exception as e:
    from pyop_api_mock import API
    api = API()
    api.config.encoding = "utf-8"

# //////////////////////////////////////////////////////////////////

import pandas as pd
import numpy as np
import io
import json
import pickle
import avro2pandas as a2p

schema = None
if hasattr(api.config, "defaultAvroSchema"):
    schema = api.config.defaultAvroSchema


def on_input(msg):
    data = msg.body
    if type(data) == bytes:
        data = data.decode(api.config.encoding, "ignore")
    names, dtypes, parse_dates = a2p.read_csv_attr(schema)
    sio = io.StringIO(data)
    try:
        df = pd.read_csv(sio,
                         header=-1,
                         names=names,
                         dtype=dtypes,
                         parse_dates=parse_dates)
        df = a2p.df_stringify_names(df)
        api.logger.info(df.columns)
    except Exception as e:
        raise e
    bio = io.BytesIO()
    df.to_parquet(bio)
    bio.seek(0)
    api.send("output", api.Message(bio.read(), msg.attributes))


api.set_port_callback("input", on_input)

# //////////////////////////////////////////////////////////

if __name__ == "__main__" and hasattr(api, "test"):
    api.test.write(
        "input", api.Message("aaa,2019-01-01,3.3\nbbb,2019-01-02,6",
                             {"foo": 1}))
    pqmsg = api.test.read("output")
    print(pqmsg)
    bio = io.BytesIO(pqmsg.body)
    df = pd.read_parquet(bio)
    print(df)
