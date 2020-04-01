function RequestController(req, resp) {
    switch (req.opid) {
        case "recs":
            var obj = JSON.parse(req.body)
            if(obj["error"] == true) {
                resp.code = 500;
                resp.data = {"code": 1, "message": obj["message"]}
            } else {
                resp.code = 200;
                resp.data = obj["result"][0]
            }
            $.out1(resp.to_message());
            break;
        default:
            resp.code = 503;
            resp.error = "Unexpected operation ID";
            $.out1(resp.to_message());
            break;
    }
}
