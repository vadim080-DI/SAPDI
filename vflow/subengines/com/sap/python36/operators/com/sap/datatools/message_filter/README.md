Message Filter
================

This operator allows to specify a **filter condition on the header attributes** that defines which messages
gets forwarded to the output port. A typical usage of the operator is to check for a termination condition of a graph.

Configuration parameters
------------

* **Condition** (type json, default: none): This json object contains the **and**ed matches of header attributes. The full specification looks as follows:

```
{ 
  "message.attribute.p1": true,
  "message.attribute.p2": false,
  "message.attribute.p3": "foo" 
}
```

With this condition the operator will forward all messages that contains all the message attributes above including their values

Input
------------

* **input** (type: message): The input message that will be checked.

Output
------------

* **output** (type: message): The output message identical to the input message if the filter condition matches. 


<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>
