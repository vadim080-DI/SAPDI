class RecSys:
    def __init__(self, rating_scale=(1,5)):
        pass

    def init(self, df):
        pass

    def fit(self, model=None):
        pass

    def predict(self, userID, k=10):
        if userID != "UERR":
            return [ ["H%d" % i, i] for i in range(1,k+1) ]
        else:
            raise ValueError("user not known")

    def dumps(self):
        return b"mymodel12312312312"

    @staticmethod
    def loads(data):
        rs = RecSys()
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

def test1():
    rs = RecSys((1,2))
    rs.init(None)
    rs.fit()
    recs = rs.predict("U002885", 4)
    print(recs)

    data = rs.dumps()
    rs2 = RecSys.loads(data)
    print(rs2.predict("U002885", 4))
    try:
        print(rs2.predict("UERR", 4))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    test1()
