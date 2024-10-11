#### Sharding

[[wU8x5Id]]](https://github.com/donnemartin/system-design-primer/blob/master/images/wU8x5Id.png)  
_[[]]_

Sharding distributes data across different databases such that each database can only manage a subset of the data. Taking a users database as an example, as the number of users increases, more shards are added to the cluster.

Similar to the advantages of [[system design primer?tab=readme ov file#federation]], sharding results in less read and write traffic, less replication, and more cache hits. Index size is also reduced, which generally improves performance with faster queries. If one shard goes down, the other shards are still operational, although you'll want to add some form of replication to avoid data loss. Like federation, there is no single central master serializing writes, allowing you to write in parallel with increased throughput.

Common ways to shard a table of users is either through the user's last name initial or the user's geographic location.
##### Disadvantage(s): sharding
- You'll need to update your application logic to work with shards, which could result in complex SQL queries.
- Data distribution can become lopsided in a shard. For example, a set of power users on a shard could result in increased load to that shard compared to others.
    - Rebalancing adds additional complexity. A sharding function based on [[the magic of consistent hashing]] can reduce the amount of transferred data.
- Joining data from multiple shards is more complex.
- Sharding adds more hardware and additional complexity.
##### Source(s) and further reading: sharding
- [[an unorthodox approach to database design the coming of the]]
- [[Shard_(database_architecture]])
- [[the magic of consistent hashing]]
