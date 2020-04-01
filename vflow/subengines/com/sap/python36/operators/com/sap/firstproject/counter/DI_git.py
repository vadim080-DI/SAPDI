counter = 0
def on_input(data):
    global counter
    counter += 1
    api.send('output', counter)
api.set_port_callback('input', on_input)  
