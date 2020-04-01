
function RequestController(req, resp) {
   
    // switch on the basis of the swagger operation ID...
    switch (req.opid) {
        case "my_pow_operation":
            resp.code = 200;

            // get query parameters
            var number = parseInt(req.query_param("number"));
            if(number == undefined) number = 1;

            var output = JSON.stringify([{"result": number * number}]);
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




// == Internals ========================================================

$.setPortCallback("input",onInput);

/**
 * For each incoming request, prepare the request and response message
 * and forward to RequestControl.
 */
function onInput(ctx, request_message) {
    request_body = parseBytesIfNecessary(request_message.Body);
    
    // prepare response message object
    var response_message = {};
    response_message.Attributes = {};
    response_message.Body = undefined;
    
    // copy request attributes to response
    response_message.Attributes = mergeArray(
          response_message.Attributes,
          request_message.Attributes
    );
    
    RequestController(
        RequestWrapper(request_message, request_body), 
        ResponseWrapper(response_message)
    );
}

/**
 * Wraps the access to a request message.
 * Message can still be accessed by the 'message' property.
 */
function RequestWrapper(req_msg, req_body) {
    var pget = function(p) { return req_msg.Attributes["openapi." + p] }
    var wrapper = {
        message: req_msg,
        path_param: function(name) { return pget("path_params." + name) },
        query_param: function(name) { return pget("query_params." + name) },
        body: req_body,
        method: pget("method"),
        opid: pget("operation_id"),
        path_pattern: pget("path_pattern"),
        host: pget("host"),
        remote_addr: pget("remote_addr"),
        request_uri: pget("request_uri")
    };
    return wrapper;
}

/**
 * Wraps the access to a response message.
 * Message can still be accessed by the 'message' property.
 */
function ResponseWrapper(resp_msg) {
    var wrapper = {
        message: resp_msg,
        code: 200,
        error: undefined,
        data: undefined,
        to_message: function() {
            resp_msg.Attributes["openapi.status_code"] = this.code;
            if(this.error != undefined) {
                resp_msg.Attributes["message.response.error"] = this.error;
            }
            resp_msg.Body = this.data;
            return resp_msg;
        }
    };
    return wrapper;
}

function mergeArray(array1,array2) {
  for(item in array1) {
    array2[item] = array1[item];
  }
  return array2;
}

function parseBytesIfNecessary(data) {
    // convert the body into string if it is bytes
    if (isByteArray(data)) {
        return String.fromCharCode.apply(null, data);
    }
    return data
}

function isByteArray(data) {
    switch (Object.prototype.toString.call(data)) {
        case "[object Int8Array]":
        case "[object Uint8Array]":
            return true;
        case "[object Array]":
        case "[object GoArray]":
            return data.length > 0 && typeof data[0] === 'number';
    }
    return false;
}

