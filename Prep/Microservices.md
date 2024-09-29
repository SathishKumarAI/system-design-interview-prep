[Microservices](https://www.ibm.com/topics/microservices) are loosely coupled, independently deployable application components that incorporate their own stack—including their own database and database model—and communicate with each other over a network. As you can run microservices on both cloud servers and on-premises data centers, they have become highly popular for [hybrid](https://www.ibm.com/topics/hybrid-cloud) and [multicloud](https://www.ibm.com/topics/multicloud) applications.

Understanding the CAP theorem can help you choose the best database when designing a microservices-based application running from multiple locations. For example, if the ability to quickly iterate the data model and scale horizontally is essential to your application, but you can tolerate eventual (as opposed to strict) consistency, an AP database like Cassandra or [Apache CouchDB](https://www.ibm.com/topics/couchdb) can meet your requirements and simplify your deployment. On the other hand, if your application depends heavily on data consistency—as in an eCommerce application or a payment service—you might opt for a relational database like PostgreSQL.

Microservices, or microservices architecture, is a [cloud-native](https://www.ibm.com/topics/cloud-native) architectural approach in which a single application is composed of many loosely coupled and independently deployable smaller components or services.

Microservices typically:  

- Have their own technology stack, inclusive of the database and data management model.  
    
- Communicate with one another over a combination of [representational state transfer (REST) APIs](https://www.ibm.com/topics/rest-apis), event streaming and [message brokers](https://www.ibm.com/topics/message-brokers).  
    
- Are organized by business capability, with the line separating services often referred to as a bounded context.

While much of the discussion about microservices has revolved around architectural definitions and characteristics, their value can be more commonly understood through fairly simple business and organizational benefits:

- Code can be updated more easily—new features or functionality can be added without touching the entire application.  
    
- Teams can use different stacks and different programming languages for different components.  
    
- Components can be scaled independently of one another, reducing the waste and cost associated with having to scale entire applications because a single feature might be facing too much load.

**What microservices are not**

Microservices might also be understood in contrast with two preceding application architectures: monolithic architecture and [service-oriented architecture (SOA)](https://www.ibm.com/topics/soa).

The difference between microservices and monolithic architecture is that microservices compose a single application from many smaller, loosely coupled services as opposed to the monolithic approach of a large, tightly coupled application.

[The differences between microservices and SOA](https://www.ibm.com/blog/soa-vs-microservices/) can be a bit less clear. While technical contrasts can be drawn between microservices and SOA, especially around the role of the [enterprise service bus](https://www.ibm.com/topics/esb), it’s easier to consider the difference as one of scope. SOA was an enterprise-wide effort to standardize the way all web services in an organization talk to and integrate with each other, whereas microservices architecture is application-specific.