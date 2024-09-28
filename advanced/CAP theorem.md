![[Pasted image 20240925230436.png]]

In a distributed computer system, you can only support two of the following guarantees:

- [[Consistency]] - Every read receives the most recent write or an error
- [[Availability]] - Every request receives a response, without guarantee that it contains the most recent version of the information
- [[Partition Tolerance]] - The system continues to operate despite arbitrary partitioning due to network failures
```Networks aren't reliable, so you'll need to support partition tolerance. You'll need to make a software tradeoff between consistency and availability.```

#### CP - consistency and partition tolerance
[link](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#cp---consistency-and-partition-tolerance)
Waiting for a response from the partitioned node might result in a timeout error. CP is a good choice if your business needs require atomic reads and writes.
#### AP - availability and partition tolerance
[link](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#ap---availability-and-partition-tolerance)
Responses return the most readily available version of the data available on any node, which might not be the latest. Writes might take some time to propagate when the partition is resolved.

AP is a good choice if the business needs to allow for [eventual consistency](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#eventual-consistency) or when the system needs to continue working despite external errors.
### Source(s) and further reading
[link](https://github.com/donnemartin/system-design-primer?tab=readme-ov-file#sources-and-further-reading-3)

- [CAP theorem revisited](http://robertgreiner.com/2014/08/cap-theorem-revisited/)
- [A plain english introduction to CAP theorem](http://ksat.me/a-plain-english-introduction-to-cap-theorem)
- [CAP FAQ](https://github.com/henryr/cap-faq)
- [The CAP theorem](https://www.youtube.com/watch?v=k-Yaq8AHlFA)

