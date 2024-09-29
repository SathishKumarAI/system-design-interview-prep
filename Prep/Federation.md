_[Source: Scaling up to your first 10 million users](https://www.youtube.com/watch?v=kKjm4ehYiMs)_

Federation (or functional partitioning) splits up databases by function. For example, instead of a single, monolithic database, you could have three databases: **forums**, **users**, and **products**, resulting in less read and write traffic to each database and therefore less replication lag. Smaller databases result in more data that can fit in memory, which in turn results in more cache hits due to improved cache locality. With no single central master serializing writes you can write in parallel, increasing throughput.
##### Disadvantage(s): federation
- Federation is not effective if your schema requires huge functions or tables.
- You'll need to update your application logic to determine which database to read and write.
- Joining data from two databases is more complex with a [server link](http://stackoverflow.com/questions/5145637/querying-data-by-joining-two-tables-in-two-database-on-different-servers).
- Federation adds more hardware and additional complexity.

##### Source(s) and further reading: federation
- [Scaling up to your first 10 million users](https://www.youtube.com/watch?v=kKjm4ehYiMs)









#### Graph database
[![](https://github.com/donnemartin/system-design-primer/raw/master/images/fNcl65g.png)](https://github.com/donnemartin/system-design-primer/blob/master/images/fNcl65g.png)  
_[Source: Graph database](https://en.wikipedia.org/wiki/File:GraphDatabase_PropertyGraph.png)_

> Abstraction: graph

In a graph database, each node is a record and each arc is a relationship between two nodes. Graph databases are optimized to represent complex relationships with many foreign keys or many-to-many relationships.

Graphs databases offer high performance for data models with complex relationships, such as a social network. They are relatively new and are not yet widely-used; it might be more difficult to find development tools and resources. Many graphs can only be accessed with [REST APIs](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#representational-state-transfer-rest).
##### Source(s) and further reading: graph
- [Graph database](https://en.wikipedia.org/wiki/Graph_database)
- [Neo4j](https://neo4j.com/)
- [FlockDB](https://blog.twitter.com/2010/introducing-flockdb)

#### Source(s) and further reading: NoSQL
- [Explanation of base terminology](http://stackoverflow.com/questions/3342497/explanation-of-base-terminology)
- [NoSQL databases a survey and decision guidance](https://medium.com/baqend-blog/nosql-databases-a-survey-and-decision-guidance-ea7823a822d#.wskogqenq)
- [Scalability](http://www.lecloud.net/post/7994751381/scalability-for-dummies-part-2-database)
- [Introduction to NoSQL](https://www.youtube.com/watch?v=qI_g07C_Q5I)
- [NoSQL patterns](http://horicky.blogspot.com/2009/11/nosql-patterns.html)