## Load balancer

[[h81n9iK]]](https://github.com/donnemartin/system-design-primer/blob/master/images/h81n9iK.png)  
_[[scalable system design patterns]]_

Load balancers distribute incoming client requests to computing resources such as application servers and databases. In each case, the load balancer returns the response from the computing resource to the appropriate client. Load balancers are effective at:

- Preventing requests from going to unhealthy servers
- Preventing overloading resources
- Helping to eliminate a single point of failure

Load balancers can be implemented with hardware (expensive) or with software such as HAProxy.

Additional benefits include:

- **SSL termination** - Decrypt incoming requests and encrypt server responses so backend servers do not have to perform these potentially expensive operations
    - Removes the need to install [[X]] on each server
- **Session persistence** - Issue cookies and route a specific client's requests to same instance if the web apps do not keep track of sessions

To protect against failures, it's common to set up multiple load balancers, either in [[system design primer?tab=readme ov file#active passive]] or [[system design primer?tab=readme ov file#active active]] mode.

Load balancers can route traffic based on various metrics, including:

- Random
- Least loaded
- Session/cookies
- [[round robin vs weighted round robin lb]]
- [[system design primer?tab=readme ov file#layer 4 load balancing]]
- [[system design primer?tab=readme ov file#layer 7 load balancing]]

### Layer 4 load balancing

Layer 4 load balancers look at info at the [[system design primer?tab=readme ov file#communication]] to decide how to distribute requests. Generally, this involves the source, destination IP addresses, and ports in the header, but not the contents of the packet. Layer 4 load balancers forward network packets to and from the upstream server, performing [[]].

### Layer 7 load balancing

Layer 7 load balancers look at the [[system design primer?tab=readme ov file#communication]] to decide how to distribute requests. This can involve contents of the header, message, and cookies. Layer 7 load balancers terminate network traffic, reads the message, makes a load-balancing decision, then opens a connection to the selected server. For example, a layer 7 load balancer can direct video traffic to servers that host videos while directing more sensitive user billing traffic to security-hardened servers.

At the cost of flexibility, layer 4 load balancing requires less time and computing resources than Layer 7, although the performance impact can be minimal on modern commodity hardware.