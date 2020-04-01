try:
  api
except Exception as e:
  from pyop_api_mock import API
  api = API()
  api.config.rating_range="1,2"

# //////////////////////////////////////////////////////////////////

import pandas as pd
import io
import json
from operators.com.sap.ariba.recsys_collabfilter1.recommender import RecSys
#from operators.com.sap.ariba.recsys_collabfilter1.recommender_mock import RecSys

def parse_df(data, fmt):
    """
    Parses input string/bytes to a pandas data frame.
    """
    fmt = fmt.lower()
    if fmt == "parquet":
        bio = io.BytesIO(data)
        df = pd.read_parquet(bio)
        return df
    elif fmt == "csv":
        if type(data) == bytes:
            data = data.decode("utf-8", "ignore")
        sio = io.StringIO(data)
        df = pd.read_csv(sio)
        return df
    else:
        raise ValueError("format %s not supported!" % f)

model = None

train_data = []

def on_train(msg):
    rating = [int(n.strip()) for n in api.config.rating_range.split(",",2)]
    data = json.loads(msg.body)
    train_data.extend(data)

    train = False
    if "recsys.dotrain" in msg.attributes and msg.attributes["recsys.dotrain"]:
        train = True

    if train:
        df = pd.DataFrame(train_data, columns=["uid","iid","rating"]) 
        # switch to json input: [{"uid": "U111", "iid": "I111", "rating": 2}, ...]
        # alternative input:    [["U111", "I111", 2], ...]
        # collect triples in operator
        #df = parse_df(msg.body, "csv")
        #df = df.iloc[:,[2,4,5]]

        global model
        model = RecSys(rating) 
        model.init(df)

        # Fit only when cb.train=True header set.
        # Make configurable as property to train after each batch or not.
        model.fit()
        api.send("outmodel", model.dumps())


def on_predict(msg):
    """
    Input:

        msg.body (json): [{"uid": "U111", "num": 5}, {"uid": "U112"}, ...]
                         ["U111", "U112", ...]

        msg.attributes:  recsys.number => number of recommendations

    Output:

        msg.body (json): { "error": true, "message": "model not available" }
                         { "error": false, result: [{"uid": "U111", items: [{"iid": "H1", "weight": 1}, ...]}, ...]}
    """

    def send_error(message):
        api.send("outpred", api.Message(json.dumps({"error": True, "message": message}), msg.attributes))

    def send_result(result):
        api.send("outpred", api.Message(json.dumps({"error": False, "result": result}), msg.attributes))

    if not model:
        send_error("invalid state: no model loaded yet")
        return

    try:
        num = 10
        if "recsys.number" in msg.attributes:
            num = int(msg.attributes["recsys.number"])

        data = msg.body
        if type(data) == bytes:
            data = data.decode("utf-8", "ignore")

        api.logger.info("prediction input: %s..." % data[:100])

        if not data:
            send_error("no input provided")
            return

        uidarr = []
        try:
            uidarr = json.loads(data)
        except Exception as e:
            send_error("invalid input: %s" % e)
            return

        uids = []
        if uidarr == []:
            send_error("invalid input: empty uid list")
            return
        elif type(uidarr) == str:
            send_error("invalid input: not an input list")
            return
        elif type(uidarr[0]) == dict:
            uids = uidarr
        elif type(uidarr[0]) == str:
            for uid in uidarr:
                uids.append({"uid": uid})
        else:
            send_error("invalid input: wrong json structure")
            return

        api.logger.debug("parsed input: %s" % uids)

        # prepare output - return empty items list for non existing uids
        pred = []
        for obj in uids:
            try:
                uid = obj["uid"]
                unum = obj["num"] if "num" in obj else num
                api.logger.info("predicting: %s %d" % (uid, unum))
                recs = model.predict(uid, unum)
                items = [{"iid": iid, "weight": weight} for iid, weight in recs]
                pred.append({"uid": uid, "items": items})
            except ValueError as e:
                api.logger.error(e)
                pred.append({"uid": uid, "items": []})

        send_result(pred)
    except Exception as e:
        send_error("unexpected error: %s" % (str(e)))

def on_model(blob):
    global model
    if not blob:
        model = None
    else:
        model = RecSys.loads(blob)

api.set_port_callback("intrain", on_train)
api.set_port_callback("inpredict", on_predict)
api.set_port_callback("inmodel", on_model)

# //////////////////////////////////////////////////////////////////
TESTPRQ="/WORK/TASKS/teched19/teched19-ariba/solution/content/files/ariba/export/2019-01-02/part-1.parquet"
TESTCSV="/WORK/TASKS/teched19/teched19-ariba/solution/content/files/ariba/inbox/2019-01-02/part-1.csv"
TESTUSERS=["U003554", "U000554", "U002987", "U002916", "U007927"]
TESTUSERINPUT=[{"uid": uid, "num": 4} for uid in TESTUSERS]

if __name__ == "__main__" and hasattr(api, "test"):

    import sys
    import time
    #api.test.listen("outmodel", lambda x: print("OUT MODEL:", x))
    #api.test.listen("outpred", lambda x: print("OUT PREDICT:", x.body[:100]))

    # train model
    with open(TESTCSV, "rb") as fp:
        api.test.write("intrain", api.Message(fp.read()))

    outmodel = api.test.read("outmodel")
    print(len(outmodel))

    # empty/wrong input
    api.test.write("inpredict", api.Message('{dfsd$$'))
    out = api.test.read("outpred")
    print(out.body)
    api.test.write("inpredict", api.Message('[]'))
    out = api.test.read("outpred")
    print(out.body)
    api.test.write("inpredict", api.Message('"U003554"'))
    out = api.test.read("outpred")
    print(out.body)
    # non-existing users
    api.test.write("inpredict", api.Message('["U111", "U222"]'))
    out = api.test.read("outpred")
    print(out.body)
    api.test.write("inpredict", api.Message('[{"uid": "U111"}, {"uid": "U222", "num": 3}]'))
    out = api.test.read("outpred")
    print(out.body)
    # existing users
    api.test.write("inpredict", api.Message(json.dumps(TESTUSERS)))
    out = api.test.read("outpred")
    print(out.body)
    api.test.write("inpredict", api.Message(json.dumps(TESTUSERINPUT)))
    out = api.test.read("outpred")
    print(out.body)
    # unset/set model
    api.test.write("inmodel", b"")
    time.sleep(0.1)
    api.test.write("inpredict", api.Message('["U111", "U222"]'))
    out = api.test.read("outpred")
    print(out.body)
    api.test.write("inmodel", outmodel)
    time.sleep(0.1)
    api.test.write("inpredict", api.Message('["U111", "U222"]'))
    out = api.test.read("outpred")
    print(out.body)

