## **Serverless computing**

Earlier in this module, you learned about Amazon EC2, a service that lets you run virtual servers in the cloud. If you have applications that you want to run in Amazon EC2, you must do the following:

1. Provision instances (virtual servers).
    
2. Upload your code.
    
3. Continue to manage the instances while your application is running.
    

![](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1729144800/tW2Dcb9QndJGxmx9l0Aohg/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/CPE%20Digital%20-%20Serverless%20computing.png)

Comparison between computing with virtual servers (thinking about servers and code) and serverless computing (thinking only about code).

The term “serverless” means that your code runs on servers, but you do not need to provision or manage these servers. With serverless computing, you can focus more on innovating new products and features instead of maintaining servers.

Another benefit of serverless computing is the flexibility to scale serverless applications automatically. Serverless computing can adjust the applications' capacity by modifying the units of consumptions, such as throughput and memory. 

An AWS service for serverless computing is **AWS Lambda**.

## **AWS Lambda**

[**AWS Lambda**(opens in a new tab)](https://aws.amazon.com/lambda) is a service that lets you run code without needing to provision or manage servers. 

While using AWS Lambda, you pay only for the compute time that you consume. Charges apply only when your code is running. You can also run code for virtually any type of application or backend service, all with zero administration. 

For example, a simple Lambda function might involve automatically resizing uploaded images to the AWS Cloud. In this case, the function triggers when uploading a new image. 

### **How AWS Lambda works**

![Process depicting how AWS Lambda works. Process described in number list in the text.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1729144800/tW2Dcb9QndJGxmx9l0Aohg/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/CPE%20Digital%20-%20How%20AWS%20Lambda%20works.png)

1. You upload your code to Lambda. 
    
2. You set your code to trigger from an event source, such as AWS services, mobile applications, or HTTP endpoints.
    
3. Lambda runs your code only when triggered.
    
4. You pay only for the compute time that you use. In the previous example of resizing images, you would pay only for the compute time that you use when uploading new images. Uploading the images triggers Lambda to run code for the image resizing function.
    

In AWS, you can also build and run **containerized** applications.

## **Containers**

**Containers** provide you with a standard way to package your application's code and dependencies into a single object. You can also use containers for processes and workflows in which there are essential requirements for security, reliability, and scalability.

To review an example on how containers work, choose the arrow buttons.

Step 1

## One host with multiple containers

![Example of a container that includes apps, bins/libs, an operating system, and a server.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1729144800/tW2Dcb9QndJGxmx9l0Aohg/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/CPE%20Digital%20-%20Containers%201.png)

Suppose that a company’s application developer has an environment on their computer that is different from the environment on the computers used by the IT operations staff. The developer wants to ensure that the application’s environment remains consistent regardless of deployment, so they use a containerized approach. This helps to reduce time spent debugging applications and diagnosing differences in computing environments.

1. 1
2. 2

Step 2

## Tens of hosts with hundreds of containers

![Example of scaling up to tens of hosts with hundreds of containers.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1729144800/tW2Dcb9QndJGxmx9l0Aohg/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/CPE%20Digital%20-%20Containers%202.png)

When running containerized applications, it’s important to consider scalability. Suppose that instead of a single host with multiple containers, you have to manage tens of hosts with hundreds of containers. Alternatively, you have to manage possibly hundreds of hosts with thousands of containers. At a large scale, imagine how much time it might take for you to monitor memory usage, security, logging, and so on.

1. 1
2. 2

## Summary

Container orchestration services help you to deploy, manage, and scale your containerized applications. Next, you will learn about two services that provide container orchestration: Amazon Elastic Container Service and Amazon Elastic Kubernetes Service.

START AGAIN

1. 1
2. 2

## **Amazon Elastic Container Service (Amazon ECS)**

[**Amazon Elastic Container Service (Amazon ECS)**(opens in a new tab)](https://aws.amazon.com/ecs/) is a highly scalable, high-performance container management system that enables you to run and scale containerized applications on AWS. 

Amazon ECS supports Docker containers. [Docker(opens in a new tab)](https://www.docker.com/) is a software platform that enables you to build, test, and deploy applications quickly. AWS supports the use of open-source Docker Community Edition and subscription-based Docker Enterprise Edition. With Amazon ECS, you can use API calls to launch and stop Docker-enabled applications.

## **Amazon Elastic Kubernetes Service (Amazon EKS)**

[**Amazon Elastic Kubernetes Service (Amazon EKS)**(opens in a new tab)](https://aws.amazon.com/eks/) is a fully managed service that you can use to run Kubernetes on AWS. 

[Kubernetes(opens in a new tab)](https://kubernetes.io/) is open-source software that enables you to deploy and manage containerized applications at scale. A large community of volunteers maintains Kubernetes, and AWS actively works together with the Kubernetes community. As new features and functionalities release for Kubernetes applications, you can easily apply these updates to your applications managed by Amazon EKS.

## **AWS Fargate**

[**AWS Fargate**(opens in a new tab)](https://aws.amazon.com/fargate/) is a serverless compute engine for containers. It works with both Amazon ECS and Amazon EKS. 

When using AWS Fargate, you do not need to provision or manage servers. AWS Fargate manages your server infrastructure for you. You can focus more on innovating and developing your applications, and you pay only for the resources that are required to run your containers.

To learn about additional services and solutions, visit [Compute on AWS(opens in a new tab)](https://aws.amazon.com/products/compute).