

class CSVUnChunk:
  def __init__(self, k):
    self._lines = []
    self._rest = ""
    self.k = k

  def add_chunk(self, chunk):
    self._rest += chunk
    try:
        idx = self._rest.rindex("\n")
        valid, rest = self._rest[:idx], self._rest[idx+1:]
        self._rest = rest

        lines = [l for l in valid.split("\n") if l.strip() != ""]
        self._lines.extend(lines)

        while len(self._lines) > self.k:
            res = self._lines[:self.k]
            self._lines = self._lines[self.k:]
            yield "\n".join(res) + "\n"
    except ValueError as e:
        pass

  def close(self):
    if self._lines:
        res = "\n".join(self._lines) + "\n"
        self._lines = []
        assert self._rest == ""
        return res
    else:
        return None

cu = CSVUnChunk(int(api.config.num_lines))
attrs = {}

def on_input(msg):
    data = msg.body
    global attrs
    attrs = msg.attributes
    if "message.error" in attrs and attrs["message.error"]:
        pass
    if type(data) == bytes:
      data = data.decode(api.config.encoding, "ignore")
    for csv in cu.add_chunk(data):
        api.send("output", api.Message(csv, attrs))

    if api.config.final_condition:
        is_final = True
        for k,v in api.config.final_condition.items():
            is_final &= k in msg.attributes and msg.attributes[k] == v
        if is_final:
            csv = cu.close()
            if csv:
                api.send("output", api.Message(csv, attrs))

api.set_port_callback("input", on_input)
