- [[Vertical scaling]]
- [[Horizontal scaling]]
- [Caching](Caching.md)
- [[Load balancing]]
- [[Database replication]]
- [[Database partitioning]]
- 
### 7. **Clones**

Cloning refers to duplicating an entire application stack, including web servers, databases, and other components, to create multiple identical copies. This approach is often used to scale applications horizontally and provide redundancy.

#### Benefits:
	- **Fault Tolerance**: If one clone fails, traffic can be routed to another clone.u
- **Increased Capacity**: Clones can be added to handle increased traffic without changing the application architecture.

#### Challenges:
- **Data Synchronization**: Ensuring consistency and synchronization between cloned databases and services can be complex.
- **Cost**: Cloning entire application stacks can be expensive, especially when large amounts of infrastructure are required.

---

### 8. **Databases**

Databases are the backbone of most systems, providing structured storage for data. Various types of databases are used based on the requirements of the system, such as relational databases (e.g., MySQL, PostgreSQL) or NoSQL databases (e.g., MongoDB, Cassandra).

#### Relational Databases (RDBMS):
- **Structured**: Data is stored in tables with predefined schemas.
- **Transactions**: Support for ACID (Atomicity, Consistency, Isolation, Durability) properties ensures reliable transactions.
  
#### NoSQL Databases:
- **Flexibility**: No fixed schema, making it suitable for storing unstructured or semi-structured data.
- **Scalability**: Easier to scale horizontally compared to traditional relational databases.

---

### 9. **Caches**

A cache is a high-speed storage layer that temporarily stores frequently accessed data to reduce latency and database load. Caches can exist at different layers, from in-memory caching (e.g., Redis, Memcached) to browser caching.

#### Types of Caches:
- **Client-side caching**: Data is stored closer to the user (e.g., browser cache) to reduce latency.
- **Server-side caching**: Data is stored on the server side to reduce database access.

---

### 10. **Asynchronism**

Asynchronous processing refers to decoupling tasks in a system so that one task doesn’t have to wait for the completion of another. Asynchronous systems use queues, background workers, or messaging systems to handle time-consuming operations outside the main request-response cycle.

#### Benefits:
- **Improved Responsiveness**: Users don’t have to wait for long-running tasks, such as sending emails or processing large datasets.
- **Improved Scalability**: Background workers can be scaled independently of the main application.

---

### 11. **Performance vs Scalability**

Performance refers to how fast a system can respond to a request, while scalability is the ability of a system to handle growing amounts

 of work by adding resources. High-performance systems may not always be scalable and vice versa.

#### Trade-offs:
- **Performance**: Focuses on reducing latency and improving response times.
- **Scalability**: Focuses on accommodating more users or larger datasets by adding resources.

---

### 12. **Latency vs Throughput**

Latency is the time it takes for a system to respond to a request, while throughput refers to the number of requests a system can handle over time.

#### Trade-offs:
- **Low Latency**: Ensures faster response times but may reduce throughput if the system spends too much time optimizing for speed.
- **High Throughput**: Allows the system to process more requests but may increase latency if requests queue up.

---

### 13. **Availability vs Consistency (CAP Theorem)**

The CAP theorem states that in a distributed system, you can only guarantee two out of three properties: consistency, availability, and partition tolerance.

#### Trade-offs:
- **Consistency**: Ensures that all nodes in a system return the same data at any time.
- **Availability**: Ensures that every request receives a response, even if some nodes are down.
