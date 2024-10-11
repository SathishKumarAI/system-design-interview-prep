_[[watch?v=kKjm4ehYiMs]]_

Federation (or functional partitioning) splits up databases by function. For example, instead of a single, monolithic database, you could have three databases: **forums**, **users**, and **products**, resulting in less read and write traffic to each database and therefore less replication lag. Smaller databases result in more data that can fit in memory, which in turn results in more cache hits due to improved cache locality. With no single central master serializing writes you can write in parallel, increasing throughput.
##### Disadvantage(s): federation
- Federation is not effective if your schema requires huge functions or tables.
- You'll need to update your application logic to determine which database to read and write.
- Joining data from two databases is more complex with a [[querying data by joining two tables in two database on different servers]].
- Federation adds more hardware and additional complexity.

##### Source(s) and further reading: federation
- [[watch?v=kKjm4ehYiMs]]









#### Graph database
[[fNcl65g]]](https://github.com/donnemartin/system-design-primer/blob/master/images/fNcl65g.png)  
_[[File:GraphDatabase_PropertyGraph]]_

> Abstraction: graph

In a graph database, each node is a record and each arc is a relationship between two nodes. Graph databases are optimized to represent complex relationships with many foreign keys or many-to-many relationships.

Graphs databases offer high performance for data models with complex relationships, such as a social network. They are relatively new and are not yet widely-used; it might be more difficult to find development tools and resources. Many graphs can only be accessed with [[system design primer?tab=readme ov file#representational state transfer rest]].
##### Source(s) and further reading: graph
- [[Graph_database]]
- [[]]
- [[introducing flockdb]]

#### Source(s) and further reading: NoSQL
- [[explanation of base terminology]]
- [[nosql databases a survey and decision guidance ea7823a822d#]]
- [[scalability for dummies part 2 database]]
- [[watch?v=qI_g07C_Q5I]]
- [[nosql patterns]]