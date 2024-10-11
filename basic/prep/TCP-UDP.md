### Transmission control protocol (TCP)

[[JdAsdvG]]](https://github.com/donnemartin/system-design-primer/blob/master/images/JdAsdvG.jpg)  
_[[]]_

TCP is a connection-oriented protocol over an [[Internet_Protocol]]. Connection is established and terminated using a [[Handshaking]]. All packets sent are guaranteed to reach the destination in the original order and without corruption through:

- Sequence numbers and [[Transmission_Control_Protocol#Checksum_computation]] for each packet
- [[Acknowledgement_(data_networks]]) packets and automatic retransmission

If the sender does not receive a correct response, it will resend the packets. If there are multiple timeouts, the connection is dropped. TCP also implements [[Flow_control_(data]]) and [[Network_congestion#Congestion_control]]. These guarantees cause delays and generally result in less efficient transmission than UDP.

To ensure high throughput, web servers can keep a large number of TCP connections open, resulting in high memory usage. It can be expensive to have a large number of open connections between web server threads and say, a [[]] server. [[Connection_pool]] can help in addition to switching to UDP where applicable.

TCP is useful for applications that require high reliability but are less time critical. Some examples include web servers, database info, SMTP, FTP, and SSH.

Use TCP over UDP when:

- You need all of the data to arrive intact
- You want to automatically make a best estimate use of the network throughput

### User datagram protocol (UDP)

[[yzDrJtA]]](https://github.com/donnemartin/system-design-primer/blob/master/images/yzDrJtA.jpg)  
_[[]]_

UDP is connectionless. Datagrams (analogous to packets) are guaranteed only at the datagram level. Datagrams might reach their destination out of order or not at all. UDP does not support congestion control. Without the guarantees that TCP support, UDP is generally more efficient.

UDP can broadcast, sending datagrams to all devices on the subnet. This is useful with [[Dynamic_Host_Configuration_Protocol]] because the client has not yet received an IP address, thus preventing a way for TCP to stream without the IP address.

UDP is less reliable but works well in real time use cases such as VoIP, video chat, streaming, and realtime multiplayer games.

Use UDP over TCP when:

- You need the lowest latency
- Late data is worse than loss of data
- You want to implement your own error correction

#### Source(s) and further reading: TCP and UDP
- [[]]
- [[]]
- [[difference between tcp and udp]]
- [[Transmission_Control_Protocol]]
- [[User_Datagram_Protocol]]
- [[memcache fb]]