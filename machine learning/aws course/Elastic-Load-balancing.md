Properly distribute traffic:
- High Performance
- Cost Efficient
- Highly Available
- Automatically Scalable

Regional Constraint 
Decoupled Architecture 
## 

**Elastic Load Balancing**

**Elastic Load Balancing** is the AWS service that automatically distributes incoming application traffic across multiple resources, such as Amazon EC2 instances. 

A load balancer acts as a single point of contact for all incoming web traffic to your Auto Scaling group. This means that as you add or remove Amazon EC2 instances in response to the amount of incoming traffic, these requests route to the load balancer first. Then, the requests spread across multiple resources that will handle them. For example, if you have multiple Amazon EC2 instances, Elastic Load Balancing distributes the workload across the multiple instances so that no single instance has to carry the bulk of it. 

Although Elastic Load Balancing and Amazon EC2 Auto Scaling are separate services, they work together to help ensure that applications running in Amazon EC2 can provide high performance and availability. 

## 

**Example: Elastic Load Balancing**

![ELB pointing to two EC2 instances in an Auto Scaling group.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1729119600/QIMDsrFlqZxLH1Y9HaRSxg/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/CPE%20Digital%20-%20Low%20demand.png)

**Low-demand period**

Here’s an example of how Elastic Load Balancing works. Suppose that a few customers have come to the coffee shop and are ready to place their orders. 

If only a few registers are open, this matches the demand of customers who need service. The coffee shop is less likely to have open registers with no customers. In this example, you can think of the registers as Amazon EC2 instances.

![Elastic Load Balancing during a high-demand period.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1729119600/QIMDsrFlqZxLH1Y9HaRSxg/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/CPE%20Digital%20-%20High%20demand.png)

**High-demand period**

Throughout the day, as the number of customers increases, the coffee shop opens more registers to accommodate them. 

Additionally, a coffee shop employee directs customers to the most appropriate register so that the number of requests can evenly distribute across the open registers. You can think of this coffee shop employee as a load balancer.