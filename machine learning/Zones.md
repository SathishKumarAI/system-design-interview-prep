An **Availability Zone** is a single data center or a group of data centers within a Region. Availability Zones are located tens of miles apart from each other. This is close enough to have low latency (the time between when content requested and received) between Availability Zones. However, if a disaster occurs in one part of the Region, they are distant enough to reduce the chance that multiple Availability Zones are affected.

To review an example of running Amazon EC2 instances in multiple Availability Zones, choose the arrow buttons.

Step 1

## 

Amazon EC2 instance in a single Availability Zone

![An EC2 instance is deployed only in the us-west-1a AZ.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1730322000/whZT98gF5AyYnvmt6AW92g/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/Multiple_AZ_01.png)

Suppose that you’re running an application on a single Amazon EC2 instance in the Northern California Region. The instance is running in the us-west-1a Availability Zone. If us-west-1a were to fail, you would lose your instance.

## 

Amazon EC2 instances in multiple Availability Zones

![EC2 instances are deployed in the us-west-1a and us-west-1b AZs.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1730322000/whZT98gF5AyYnvmt6AW92g/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/Multiple_AZ_02.png)

A best practice is to run applications across at least two Availability Zones in a Region. In this example, you might choose to run a second Amazon EC2 instance in us-west-1b.

## 

Availability Zone failure

![The us-west-1a AZ has failed, but an EC2 instance is still running in the us-west-1b AZ.](https://explore.skillbuilder.aws/files/a/w/aws_prod1_docebosaas_com/1730322000/whZT98gF5AyYnvmt6AW92g/tincan/fe470bc5add63f94f005d3da17a6db8131e78b9e/assets/Multiple_AZ_03.png)

If us-west-1a were to fail, your application would still be running in us-west-1b.