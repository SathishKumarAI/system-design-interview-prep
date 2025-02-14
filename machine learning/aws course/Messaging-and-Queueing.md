## **Monolithic applications and microservices**

![Four rectangles close together in a larger square to indicate tightly coupled components as seen in monolithic applications.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1729119600/QIMDsrFlqZxLH1Y9HaRSxg/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/CPE%20Digital%20-%20Monolithic%20application.png)

Applications are made of multiple components. The components communicate with each other to transmit data, fulfill requests, and keep the application running. 

Suppose that you have an application with tightly coupled components. These components might include databases, servers, the user interface, business logic, and so on. This type of architecture can be considered a **monolithic application**. 

In this approach to application architecture, if a single component fails, other components fail, and possibly the entire application fails.

To help maintain application availability when a single component fails, you can design your application through a **microservices** approach.

![Four rectangles with distance between them connected by lines in a rectangle pattern to indicate loosely coupled components.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1729119600/QIMDsrFlqZxLH1Y9HaRSxg/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/CPE%20Digital%20-%20Microservices.png)

In a microservices approach, application components are loosely coupled. In this case, if a single component fails, the other components continue to work because they are communicating with each other. The loose coupling prevents the entire application from failing. 

When designing applications on AWS, you can take a microservices approach with services and components that fulfill different functions. 

Two services facilitate application integration: 

- **Amazon Simple Notification Service (Amazon SNS)**
- **Amazon Simple Queue Service (Amazon SQS)**

