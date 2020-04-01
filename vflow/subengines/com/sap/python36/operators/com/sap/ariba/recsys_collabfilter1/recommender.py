import surprise
from surprise import Reader, Dataset
import csv
import numpy as np
from sklearn.model_selection import cross_validate
import pandas as pd
import sys
import logging
from pickle import dumps, loads
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

class RecSys:
    def __init__(self, rating_scale=(1,5)):
        self.rating_scale = rating_scale
        self.reader = Reader(rating_scale=self.rating_scale)

        self.trainset = None
        self.orders = None

        self.model = None

    def init(self, df):
        s0 = time.time()
        logger.debug("processing dataframe %s..." % (str(df.shape)))
        logger.debug("computing uid/pid order set...")
        self.orders = set(np.unique(df.apply(func=lambda x: (x[0],x[1]), axis=1)))

        logger.debug("creating dataset...")
        data = Dataset.load_from_df(df, self.reader)
        self.trainset = data.build_full_trainset()

        s1 = time.time()
        logger.debug("processing dataframe done (%f secs)" % (s1-s0))

    def fit(self, model=None):
        if model == None:
            model = surprise.SVDpp()
        s0 = time.time()
        self.model = model

        logger.debug("fitting model '%s' using df %s" % (self.model.__class__.__name__, str( (self.trainset.n_users, self.trainset.n_items) ) ))

        self.model.fit(self.trainset)
        s1 = time.time()
        logger.debug("fitting model done (%f secs)" % (s1-s0))

    def predict(self, userID, k=None):
        logger.debug("prediction for '%s'" % userID)
        iuid = self.trainset.to_inner_uid(userID)
        recs = []
        for tid in range(self.trainset.n_items):
            item = self.trainset.to_raw_iid(tid)
            est = self.model.estimate(iuid, tid) 
            if type(est) == tuple:
                recs.append( (item, est[0]) )
            else:
                recs.append( (item, est) )
        recs.sort(key=lambda x: -x[1])
        recs_new = []
        for pid,score in recs:
            if (userID,pid) in self.orders:
                continue
            recs_new.append((pid,score))
        
        return recs_new[:k]

    def dumps(self):
        logger.debug("serializing recsys...")
        d = (self.trainset, self.model, self.orders, self.rating_scale)
        return dumps(d)

    @staticmethod
    def loads(data):
        logger.debug("loading recsys...")
        trainset, model, orders, rating_scale = loads(data)
        rs = RecSys(rating_scale)
        rs.trainset = trainset
        rs.model = model
        rs.orders = orders
        return rs

    def save(self, fn):
        with open(fn, "wb") as fp:
            fp.write(self.dumps())

    @staticmethod
    def read(fn):
        with open(fn, "rb") as fp:
            rs = RecSys.loads(fp.read())
            return rs

# TESTS //////////////////////////////////////////////////////////////

def load_df(fn="orders.csv", k=None):
    ks = str(k) if k else "all"
    logger.debug("loading '%s' (%s recs)" % (fn, ks))
    orders = []
    with open(fn, "r") as fp:
        reader = csv.reader(fp)
        for rec in reader:
            orders.append((rec[2], rec[4], rec[5]))
    data = np.array(orders)[:k,:]
    df = pd.DataFrame(data=data, columns=["uid", "pid", "num"])
    return df

def test1():
    df = load_df(k=1000)
    rs = RecSys((1,2))
    rs.init(df)
    rs.fit()
    recs = rs.predict("U002885", 4)
    print(recs)

    data = rs.dumps()
    rs2 = RecSys.loads(data)
    print(rs2.predict("U002885", 4))

    rs2.save("foo.pickle")
    rs3 = RecSys.read("foo.pickle")
    print(rs3.predict("U002885", 4))


def test2():
    df = load_df(k=1000)
    rs = RecSys((1,2))
    rs.init(df)
    rs.fit(model=surprise.KNNBaseline())
    recs = rs.predict("U002885", 4)
    print(recs)

_MODEL_NAME = "recmodel_v1.pickle"

def test31():
    df = load_df(k=100000)
    rs = RecSys((1,2))
    rs.init(df)
    rs.fit()
    rs.save(_MODEL_NAME)

def test32():
    rs = RecSys.read(_MODEL_NAME)
    print(rs.predict("U002885", 4))

if __name__ == "__main__":
    test1()
    #test2()
    #test31()
    #test32()
