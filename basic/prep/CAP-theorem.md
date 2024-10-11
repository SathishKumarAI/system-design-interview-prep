![[Pasted image 20240925230436.png]]

In a distributed computer system, you can only support two of the following guarantees:

- [Consistency](https://github.com/SathishKumar9866/system-design-interview-prep/blob/backlinks_test/Consistency.md) - Every read receives the most recent write or an error
- [Availability](https://github.com/SathishKumar9866/system-design-interview-prep/blob/backlinks_test/Availability.md) - Every request receives a response, without guarantee that it contains the most recent version of the information
- [[Partition Tolerance]] - The system continues to operate despite arbitrary partitioning due to network failures
```Networks aren't reliable, so you'll need to support partition tolerance. You'll need to make a software tradeoff between consistency and availability.```

#### CP - consistency and partition tolerance
[[system design primer?tab=readme ov file#cp   consistency and partition tolerance]]
Waiting for a response from the partitioned node might result in a timeout error. CP is a good choice if your business needs require atomic reads and writes.
#### AP - availability and partition tolerance
[[system design primer?tab=readme ov file#ap   availability and partition tolerance]]
Responses return the most readily available version of the data available on any node, which might not be the latest. Writes might take some time to propagate when the partition is resolved.

AP is a good choice if the business needs to allow for [[system design primer?tab=readme ov file#eventual consistency]] or when the system needs to continue working despite external errors.
### Source(s) and further reading
[[system design primer?tab=readme ov file#sources and further reading 3]]

- [[]]
- [[a plain english introduction to cap theorem]]
- [[cap faq]]
- [[watch?v=k Yaq8AHlFA]]
- [[cap theorem]]

