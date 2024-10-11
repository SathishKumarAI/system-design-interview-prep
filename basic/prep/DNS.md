## Domain name system

[[IOyLj4i]]](https://github.com/donnemartin/system-design-primer/blob/master/images/IOyLj4i.jpg)  
_[[dns security presentation issa]]_

A Domain Name System (DNS) translates a domain name such as [[]] to an IP address.

DNS is hierarchical, with a few authoritative servers at the top level. Your router or ISP provides information about which DNS server(s) to contact when doing a lookup. Lower level DNS servers cache mappings, which could become stale due to DNS propagation delays. DNS results can also be cached by your browser or OS for a certain period of time, determined by the [[Time_to_live]].

- **NS record (name server)** - Specifies the DNS servers for your domain/subdomain.
- **MX record (mail exchange)** - Specifies the mail servers for accepting messages.
- **A record (address)** - Points a name to an IP address.
- **CNAME (canonical)** - Points a name to another name or `CNAME` (example.com to [[]]) or to an `A` record.

Services such as [[]] and [[]] provide managed DNS services. Some DNS services can route traffic through various methods:


- 
	- please learn about [[Round robin_scheduling]]
	- https://en.wikipedia.org/wiki/File:RoundRobin.jpg 
-  [[load balancing algorithms]] 
    - Prevent traffic from going to servers under maintenance
    - Balance between varying cluster sizes
    - A/B testing`
- [[routing policy latency]]
- [[routing policy geo]]

### Disadvantage(s): DNS

- Accessing a DNS server introduces a slight delay, although mitigated by caching described above.
- DNS server management could be complex and is generally managed by [[472729]].
- DNS services have recently come under [[]], preventing users from accessing websites such as Twitter without knowing Twitter's IP address(es).

### Source(s) and further reading
- [[dd197427(v=ws]].aspx)
- [[Domain_Name_System]]
- [[]]