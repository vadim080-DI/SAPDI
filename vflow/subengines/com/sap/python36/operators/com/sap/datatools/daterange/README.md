Datetime Range
================

This operator generates a list of messages with **date string** values. It is useful to generate paths (as input to read operations) or as input for data generators.
The generated messages contain header information that allow to detect the last date (i.e., to stop a graph). See details below.

Configuration parameters
------------

* **Range Config** (type json, default: none): This json object contains the range specification. The full specification looks as follows:

```
{ 
  "date_from": "2019-01-01",
  "date_to":   "2019-02-02",
  "delta":     "3d" 
}
```

The `date_from` field is optional. In this case only a single date (`date_from`) gets generated. The delta field specifies the difference between two generated day. It can be specified using the following notation:

```
2s: 2 seconds
2m: 2 minutes
2h: 2 hours
2d: 2 days
2w: 2 weeks
```

* **Output String** (type string): Specifies the string in which the date gets embedded. The notation is `any/string/<DATE>/it/can/be`. In case the parameters is empty the generated string is just `<DATE>`.


Input
------------

None

Output
------------

* **output** (type message): A message whose body is the generated date string. The message contains the following header attributes

  * *daterange.value* (string): The generated date
  * *daterange.last* (bool): Has a `true` value for the last generated date. Can be used to check for a graph termination condition.


<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>
