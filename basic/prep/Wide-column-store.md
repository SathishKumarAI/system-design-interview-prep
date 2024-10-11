#### Wide column store

[[n16iOGk]]](https://github.com/donnemartin/system-design-primer/blob/master/images/n16iOGk.png)  
_[[sql nosql a brief history]]_

> Abstraction: nested map `ColumnFamily<RowKey, Columns<ColKey, Value, Timestamp>>`

A wide column store's basic unit of data is a column (name/value pair). A column can be grouped in column families (analogous to a SQL table). Super column families further group column families. You can access each column independently with a row key, and columns with the same row key form a row. Each value contains a timestamp for versioning and for conflict resolution.

Google introduced [[chang06bigtable]] as the first wide column store, which influenced the open-source [[]] often-used in the Hadoop ecosystem, and [[archIntro]] from Facebook. Stores such as BigTable, HBase, and Cassandra maintain keys in lexicographic order, allowing efficient retrieval of selective key ranges.

Wide column stores offer high availability and high scalability. They are often used for very large data sets.
##### Source(s) and further reading: wide column store
- [[sql nosql a brief history]]
- [[chang06bigtable]]
- [[]]
- [[archIntro]]