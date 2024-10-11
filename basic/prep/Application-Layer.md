[[yB5SYwm]]](https://github.com/donnemartin/system-design-primer/blob/master/images/yB5SYwm.png)  
_[[#platform_layer]]_

Separating out the web layer from the application layer (also known as platform layer) allows you to scale and configure both layers independently. Adding a new API results in adding application servers without necessarily adding additional web servers. The **single responsibility principle** advocates for small and autonomous services that work together. Small teams with small services can plan more aggressively for rapid growth.

Workers in the application layer also help enable [[system design primer?tab=readme ov file#asynchronism]].
### [Microservices](https://github.com/SathishKumar9866/system-design-interview-prep/blob/backlinks_test/Microservices.md)
Related to this discussion are [Microservices](https://github.com/SathishKumar9866/system-design-interview-prep/blob/backlinks_test/Microservices.md), which can be described as a suite of independently deployable, small, modular services. Each service runs a unique process and communicates through a well-defined, lightweight mechanism to serve a business goal. [[what are microservices]]

Pinterest, for example, could have the following microservices: user profile, follower, feed, search, photo upload, etc.
### Service Discovery
Systems such as [[index]], [[latest]], and [[introduction to apache zookeeper]] can help services find each other by keeping track of registered names, addresses, and ports. [[checks]] help verify service integrity and are often done using an [[system design primer?tab=readme ov file#hypertext transfer protocol http]] endpoint. Both Consul and Etcd have a built in [[system design primer?tab=readme ov file#key value store]] that can be useful for storing config values and other shared data.
### Disadvantage(s): application layer
- Adding an application layer with loosely coupled services requires a different approach from an architectural, operations, and process viewpoint (vs a monolithic system).
- Microservices can add complexity in terms of deployments and operations.
### Source(s) and further reading
- [[introduction to architecting systems for scale]]
- [[2016 02 13 crack the system design interview]]
- [[Service oriented_architecture]]
- [[introduction to apache zookeeper]]
- [[]]