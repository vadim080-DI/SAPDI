Pandas Transform
================

This operator allows to work on structured data using the **pandas** framework. The input data gets transformed into
a pandas **data frame (df)**. The data frame can then be transformed in the **code editor** and sent to the output of
the operator. The operator takes care of serialization and un-serialization of the data frames.


Configuration parameters
------------

* **Input Format** (type enum, default: CSV): This parameters specifies the format of the input message. De-serialization is achieved using the **pandas.read\_csv**, **pandas.read\_json**, or **pandas.read\_parquet** method. Additional input format parameters can be set using the **Input Properties** parameter object. 

* **Output Format** (type enum, default: CSV): This parameters specifies the format of the output message. Serialization is achieved using the **pandas.to\_csv**, **pandas.to\_json**, or **pandas.to\_parquet** method. Additional output format parameters can be set using the **Output Properties** parameter object. 

* **Input Properties** (type object): The properties in this object allow to specify additional parsing properties of the input message. The properties are translated to parameters of the respective **pandas.read\_csv**, **pandas.read\_json**, or **pandas.read\_parquet** methods.

* **Output Properties** (type object): The properties in this object allow to specify additional formatting properties of the output message. The properties are translated to parameters of the respective **pandas.to\_csv**, **pandas.to\_json**, or **pandas.to\_parquet** methods.


Input
------------

* **input** (type message): A message whose body is a serialized data frame (CSV, JSON, or PARQUET). 


Output
------------

* **output** (type message): A message whose body is the transformed, serialized data frame  (CSV, JSON, or PARQUET)


<br>
<div class="footer">
   &copy; 2019 SAP SE or an SAP affiliate company. All rights reserved.
</div>
