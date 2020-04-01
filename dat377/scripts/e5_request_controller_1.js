function RequestController(req, resp) {
    switch (req.opid) {
        case "recs":
            resp.code = 200;
            var num = req.query_param("num");
            if(num == undefined || num == "") num = 10;
            else num = parseInt(num);
            var query = JSON.stringify([{"uid": req.path_param("uid"), "num": num}]);
            resp.data = query;
            $.out1(resp.to_message());
            break;
        default:
            resp.code = 503;
            resp.error = "Unexpected operation ID";
            $.out1(resp.to_message());
            break;
    }
}
