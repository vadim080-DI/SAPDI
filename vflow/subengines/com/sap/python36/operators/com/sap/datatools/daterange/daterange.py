from dateutil.parser import parse
import datetime

def parsedelta(delta):
    v = int(delta[:-1])
    dur = delta[-1]
    if dur == "s":
        return datetime.timedelta(seconds=v)
    elif dur == "m":
        return datetime.timedelta(minutes=v)
    elif dur == "h":
        return datetime.timedelta(hours=v)
    elif dur in ("d", "D"):
        return datetime.timedelta(days=v)
    elif dur in ("w", "W"):
        return datetime.timedelta(weeks=v)
    else:
        raise ValueError("not a valid duration string")

def daterange(ds_from, ds_to=None, delta="1d", outformat="%Y-%m-%d"):
    dt_from = parse(ds_from)
    dt_to = None if not ds_to else parse(ds_to)
    delta = parsedelta(delta)

    dt_result = []
    if not dt_to:
        dt_result.append(dt_from)
    else:
        if dt_from > dt_to:
            raise ValueError("dt_from cannot be greated than dt_to")
        dt_now = dt_from
        while dt_now <= dt_to:
            dt_result.append(dt_now)
            dt_now += delta

    ds_result = [datetime.datetime.strftime(dt, outformat) for dt in dt_result]
    return ds_result

if __name__ == "__main__":
    deltas = ["1s", "100s", "1m", "100m", "1h", "100h", "1D", "100D",
            "1w", "100W"]
    for delta in deltas:
        d = parsedelta(delta)
        print(d)
    #print(parsedelta(""))
    #print(parsedelta("sdfdsf"))
    res = daterange("2019-01-01 01:02:03", "2019-04-02", "1h", "%Y-%m-%d %H:%M:%S")
    for r in res:
        print(r)
