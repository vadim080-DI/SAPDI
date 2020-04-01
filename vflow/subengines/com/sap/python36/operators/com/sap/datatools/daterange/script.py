from operators.com.sap.datatools.daterange.daterange import daterange


def get_prop(name, default_value):
    if hasattr(api.config, name) and getattr(api.config, name) != "":
        return getattr(api.config, name)
    return default_value


def gen():
    props = get_prop("rangeconfig", {"date_from": "2019-01-01", "date_to": "2019-02-01", "delta": "2d"})
    outstring = get_prop("outstring", "<DATE>")
    dates = daterange(props["date_from"], props["date_to"], props["delta"])
    n = len(dates)
    for i,dt in enumerate(dates):
        last = True if i == n-1 else False
        out = outstring.replace("<DATE>", dt)
        api.send("output", api.Message(out, {"daterange.last": last, "daterange.value": dt}))

api.add_generator(gen)

