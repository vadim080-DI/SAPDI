
def on_input(msg):
    """
    Simple operator to transform a message. Operator can be used to:
    1) change/add/remove the message attributes
    2) change the message body
    """
    body = msg.body
    attr = msg.attributes
    
    attr.update({"msgtransform.done": True})
    api.send("output", api.Message(body, attr))

api.set_port_callback("input", on_input)
