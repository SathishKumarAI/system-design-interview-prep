# Amazon EC2 Pricing and Instance Types

## Instance Types

- **General Purpose**
- **Compute Optimized**
- **Memory Optimized**
- **Accelerated Computing**
- **Storage Optimized**

## Pricing Models

### On-Demand

- **On-Demand Instances** are ideal for short-term, irregular workloads that cannot be interrupted.
- **Key Features:**
    - No upfront costs or minimum contracts.
    - Continuous operation until manually stopped.
    - Pay only for the compute time used.
- **Use Cases:**
    - Development and testing applications.
    - Applications with unpredictable usage patterns.
- **Considerations:**
    - Not cost-effective for workloads lasting a year or more.

### Savings Plans

- AWS offers **Savings Plans** for services like Amazon EC2.
- **EC2 Instance Savings Plans:**
    - Provide cost savings (up to 72%) for hourly spend commitments over 1 or 3 years.
    - Flexible usage across instance families, sizes, OS, and tenancy within a Region.
- **Advantages:**
    - No need to specify instance type, size, or OS upfront.
    - Greater flexibility compared to Reserved Instances.
- **AWS Cost Explorer:**
    - Visualize and manage costs over time.
    - Analyze past EC2 usage (7, 30, or 60 days) and get recommendations.

### Reserved Instances

- **Reserved Instances** offer billing discounts for On-Demand Instances.
- **Types:**
    - **Standard Reserved Instances**
    - **Convertible Reserved Instances**
- **Key Features:**
    - Purchase for 1-year or 3-year terms (greater savings with 3-year).
    - Can specify Availability Zones for capacity reservation.
- **Standard Reserved Instances:**
    - Best for steady-state applications.
    - Requires specific instance type, OS, and tenancy.
- **Convertible Reserved Instances:**
    - More flexible, allowing changes to instance types and sizes.

### Spot Instances

- **Spot Instances** use unused EC2 capacity for up to 90% cost savings.
- **Best for:**
    - Batch workloads.
    - Jobs with flexible start and stop times.
- **Considerations:**
    - Can be interrupted if capacity becomes unavailable.
    - Not ideal for critical applications requiring uninterrupted operation.

### Dedicated Hosts

- **Dedicated Hosts** are physical servers fully dedicated to your use.
- **Benefits:**
    - Use existing software licenses.
    - Purchase On-Demand or as Reserved Hosts.
- **Cost:**
    - Most expensive EC2 option.

---

## Amazon EC2 Overview

- **Amazon EC2** provides secure, resizable compute capacity in the cloud.
- **Key Capabilities:**
    - Launch EC2 instances within minutes.
    - Stop/shut down instances as needed.
    - Pay by the hour/second (minimum 60 seconds).
- **Management Tools:**
    - AWS Management Console
    - AWS CLI
    - AWS SDKs

### EC2 Instance Configuration

- **Hardware Specifications:** CPU, memory, network, storage.
- **Logical Configurations:** Network location, firewall rules, OS.

---

## Amazon Machine Image (AMI)

- An AMI is a pre-configured template for an EC2 instance.
- **Contains:**
    - OS
    - Storage mapping
    - Architecture
    - Launch permissions
- **Relationship to EC2 Instances:**
    - AMI = Template
    - EC2 = Live instance of that template
- **AMI Benefits:**
    - Reusability for consistent configurations.

### Finding AMIs

- **Quick Start AMIs**
- **AWS Marketplace AMIs**
- **My AMIs**
- **Community AMIs**
- **Custom Images**

---

## EC2 Instance Types

- Combination of vCPUs, memory, network, storage, and GPUs.
- **Naming Example:** `c5n.xlarge`
    - `c` = Compute Optimized
    - `5` = 5th Generation
    - `n` = NVMe storage
    - `xlarge` = Instance size

---

## High Availability and Architecting

- Deploy instances across multiple Availability Zones.
- Use multiple smaller instances for redundancy.
- Architect for failover and high availability.

---

## Resources

- [Amazon EC2 (AWS)](https://aws.amazon.com/ec2/)
- [Amazon Machine Images (AMI) User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html)
- [Create an AMI (Linux)](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-ebs.html)
- [EC2 Image Builder](https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html)
- [Default VPCs](https://docs.aws.amazon.com/vpc/latest/userguide/default-vpc.html)
- [AWS Well-Architected Framework - Reliability Pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html?ref=wellarchitected-wp)