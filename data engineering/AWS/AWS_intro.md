Infrastructure, like data centers and networking connectivity, still exists as the foundation of every cloud application. In AWS, this physical infrastructure makes up the AWS Global Infrastructure, in the form of Regions and Availability Zones.
[[]]
## 

## **Regions**

![The AWS Cloud spans 93 Availability Zones within 29 geographic Regions around the world](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1721077200/mnuxQ5FmLJof3wWrO9Ia1w/tincan/7b5246b3e4dcf41ee9510fd1863163b18f6b0358/assets/IvaJxtpsoS4aZO4y_dwdwrOZ6lWRw96bM.jpg)

Regions are geographic locations worldwide where AWS hosts its data centers. AWS Regions are named after the location where they reside. For example, in the United States, the Region in Northern Virginia is called the Northern Virginia Region, and the Region in Oregon is called the Oregon Region. AWS has Regions in Asia Pacific, China, Europe, the Middle East, North America, and South America. And we continue to expand to meet our customers' needs.

Each AWS Region is associated with a geographical name and a Region code.

Here are examples of Region codes:

- **us-east-1** is the first Region created in the eastern US area. The geographical name for this Region is N. Virginia.
- **ap-northeast-1** is the first Region created in the northeast Asia Pacific area. The geographical name for this Region is Tokyo.

! [A dropdown view of AWS Regions in the AWS Management Console.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1721077200/mnuxQ5FmLJof3wWrO9Ia1w/tincan/7b5246b3e4dcf41ee9510fd1863163b18f6b0358/assets/FVqj2WTva3l2DZEw_UB1vzpgv31Y9lgIX.jpg)

Within the AWS Console, you can select an available region from the dropdown menu

### 

**Choosing the right AWS Region**

AWS Regions are independent from one another. Without explicit customer consent and authorization, data is not replicated from one Region to another. When you decide which AWS Region to host your applications and workloads, consider four main aspects: latency, price, service availability, and compliance.

To learn about a category, choose the appropriate tab.

`
- LATENCY
- PRICING
- SERVICE & AVAILABILITY
- DATA COMPLIANCE`

If your application is sensitive to latency (the delay between a request for data and the response), choose a Region that is close to your user base. This helps prevent long wait times for your customers. Synchronous applications such as gaming, telephony, WebSockets, and Internet of Things (IoT) are significantly affected by high latency. Asynchronous workloads, such as ecommerce applications, can also suffer from user connectivity delays.

! [](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1721077200/mnuxQ5FmLJof3wWrO9Ia1w/tincan/7b5246b3e4dcf41ee9510fd1863163b18f6b0358/assets/WLOCofUcy6YguQFk_zDXx48iu1f1XRHjL.png)

## Availability Zones

Inside every Region is a cluster of Availability Zones. An [[Availability Zone]] consists of one or more data centers with redundant power, networking, and connectivity. These data centers operate in discrete facilities in undisclosed locations. They are connected using redundant high-speed and low-latency links.  
  
Availability Zones also have code names. Because they are located inside Regions, they can be addressed by appending a letter to the end of the Region code name. Here are examples of Availability Zone codes:

- **us-east-1a** is an Availability Zone in us-east-1 (N. Virginia Region).
- **sa-east-1b** is an Availability Zone in sa-east-1 (São Paulo Region).

Therefore, if you see that a resource exists in us-east-1c, you can infer that the resource is located in Availability Zone c of the us-east-1 Region.

![Within a Region, an Availability Zone consists of one or more data centers.] (https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1721077200/mnuxQ5FmLJof3wWrO9Ia1w/tincan/7b5246b3e4dcf41ee9510fd1863163b18f6b0358/assets/x1mfH4qAkD-4TwYA_goM0jOy5I9qYZ-kE.png)

## ****Scope of AWS services****

Depending on the AWS service that you use, your resources are either deployed at the Availability Zone, Region, or Global level. Each service is different, so you must understand how the scope of a service might affect your application architecture.  
  
When you operate a Region-scoped service, you only need to select the Region that you want to use. If you are not asked to specify an individual Availability Zone to deploy the service in, this is an indicator that the service operates on a Region-scope level. For Region-scoped services, AWS automatically performs actions to increase data durability and availability.  
  
On the other hand, some services ask you to specify an Availability Zone. With these services, you are often responsible for increasing the data durability and high availability of these resources.

## ****Maintaining resiliency****

To keep your application available, you must maintain high availability and [resiliency](Tags\resiliency.md). A well-known best practice for cloud architecture is to use Region-scoped, managed services. These services come with availability and resiliency built in. When that is not possible, make sure your workload is replicated across multiple Availability Zones. At a minimum, you should use two Availability Zones. That way, if an Availability Zone fails, your application will have infrastructure up and running in a second Availability Zone to take over the traffic.

![Replicate your workload across multiple Availability Zones to maintain high availability and resiliency.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1721077200/mnuxQ5FmLJof3wWrO9Ia1w/tincan/7b5246b3e4dcf41ee9510fd1863163b18f6b0358/assets/dhozItxyf5VCYnL9_hoflaaUCH5jvaJMM.png)

## **Edge locations  **

Edge locations are global locations where content is cached. For example, if your media content is in London and you want to share video files with your customers in Sydney, you could have the videos cached in an edge location closest to Sydney. This would make it possible for your customers to access the cached videos more quickly than accessing them from London. Currently, there are over 400+ edge locations globally.

Amazon CloudFront delivers your content through a worldwide network of edge locations. When a user requests content that is being served with CloudFront, the request is routed to the location that provides the lowest latency. So that content is delivered with the best possible performance. CloudFront speeds up the distribution of your content by routing each user request through the AWS backbone network to the edge location that can best serve your content.

![Cache your content in an edge location closest to your customers.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1721077200/mnuxQ5FmLJof3wWrO9Ia1w/tincan/7b5246b3e4dcf41ee9510fd1863163b18f6b0358/assets/XwzRSOJ7v49YBXYC_6wjg5Qmcv-Jg7jd4.png)
