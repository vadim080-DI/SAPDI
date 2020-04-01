try:
  api
except Exception as e:
  from pyop_api_mock import API
  api = API()

# //////////////////////////////////////////////////////////////////

def on_input(msg):
    api.logger.info("received message")
    if hasattr(api.config, "condition") and api.config.condition:
        match = True
        for k,v in api.config.condition.items():
            match &= k in msg.attributes and msg.attributes[k] == v
        if match:
            api.send("output", api.Message(msg.body, msg.attributes))
    else:
        api.send("output", msg)

api.set_port_callback("input", on_input)

# //////////////////////////////////////////////////////////////////

if __name__ == "__main__" and hasattr(api, "test"):
    api.config.condition = {"last": True}
    api.test.listen("output")

    api.test.write("input", api.Message("NO"))
    api.test.write("input", api.Message("YES", {"last": True}))
    api.test.write("input", api.Message("NO", {"last": False}))

    api.config.condition = {"last": True, "foo": "bar"}

    for last in (True, False, None):
        for foo in ("moo", "bar", None):
            body = "NO"
            if last and foo == "bar":
                body = "YES"
            api.test.write("input", api.Message(body, {"last": last, "foo": foo}))

    api.test.wait("output")
