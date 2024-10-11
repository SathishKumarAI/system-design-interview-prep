
Before proceeding with the installation, please review the following resources and choose what best suits your use case. 

> **Note:** Some resources may be outdated. Please check for updated information before proceeding.

---

## Resources

- [[]]
- [[why is pyspark so much slower on windows than on linux]]
- [[spark wsl install]]
  - Most content is derived from this repository.

---

## Prerequisites

- **WSL** (Windows Subsystem for Linux)
- **Ubuntu WSL**
- **Java**
- **Python**
- 

---

## Task List

- [ ] Enable WSL
- [ ] Install Ubuntu
- [ ] Download and Install OpenJDK 8
- [ ] Download and Install Spark

---

## Spark WSL Install: Step-by-Step Guide

### 1. Enable WSL

1. Go to _Start_ → _Control Panel_ → _Turn Windows features on or off_.
2. Check the option for **Windows Subsystem for Linux**.

### 2. Install Ubuntu

1. Go to _Start_ → _Microsoft Store_.
2. Search for **Ubuntu**.
3. Select **Ubuntu**, then click **Get** and **Launch** to install the Ubuntu terminal on your Windows system.  
   _Note:_ If the installation hangs, press _Enter_.
4. Follow the prompts to create a username and password.

### 3. Launch Ubuntu

1. Go to _Start_ → _Command Prompt_.  
2. To launch Ubuntu, type `bash` and press _Enter_.  
   Now, you have access to a Linux terminal on your Windows machine.

---

## Java Installation: OpenJDK 8 Setup

### Step 1: Remove Existing Java Versions

1. To remove existing OpenJDK packages:
   
   ```bash
   sudo apt remove openjdk-11-jdk openjdk-11-jre openjdk-21-jdk openjdk-21-jre  
   sudo apt autoremove
   ```

2. Clean up any remaining Java-related directories:
   
   ```bash
   sudo rm -rf /usr/lib/jvm/*
   ```

### Step 2: Install JDK 22

1. Download the JDK 22 package:

   ```bash
   wget https://download.oracle.com/java/22/latest/jdk-22_linux-x64_bin.tar.gz
   ```

2. Create a directory for the new JDK:

   ```bash
   sudo mkdir -p /usr/lib/jvm
   ```

3. Extract the downloaded JDK archive:

   ```bash
   sudo tar -xvzf jdk-22_linux-x64_bin.tar.gz -C /usr/lib/jvm
   ```

### Step 3: Configure Java Environment

1. Set up alternatives to configure the system to recognize the new Java installation:

   ```bash
   sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk-22.0.2/bin/java 1  
   sudo update-alternatives --install /usr/bin/javac javac /usr/lib/jvm/jdk-22.0.2/bin/javac 1
   ```

   _Note:_ Replace `jdk-22.0.2` with the actual directory name in `/usr/lib/jvm/`.

2. Set JDK 22 as the default Java version:

   ```bash
   sudo update-alternatives --set java /usr/lib/jvm/jdk-22.0.2/bin/java  
   sudo update-alternatives --set javac /usr/lib/jvm/jdk-22.0.2/bin/javac
   ```

### Step 4: Verification and Cleanup

1. Verify the installation:

   ```bash
   java --version  
   javac --version
   ```

2. Clean up the downloaded JDK archive:

   ```bash
   rm jdk-22_linux-x64_bin.tar.gz
   ```

3. Verify removal of old Java versions:

   ```bash
   sudo update-alternatives --config java  
   ls -l /usr/lib/jvm/
   ```

---

## Spark Installation

### Step 1: Download and Install Spark

1. Open a new Linux terminal and execute the following commands:

   ```bash
   mkdir Ubuntu
   cd Ubuntu
   mkdir Downloads
   cd Downloads
   wget http://apache.cs.utah.edu/spark/spark-2.3.1/spark-2.3.1-bin-hadoop2.7.tgz
   cd ..
   mkdir Programs
   tar -xvzf Downloads/spark-2.3.1-bin-hadoop2.7.tgz -C Programs
   ```

### Step 2: Configure Spark Environment

1. Open your `.bashrc` file in a text editor:

   ```bash
   nano ~/.bashrc
   ```

2. Scroll to the bottom of the file and add the following line to define the `SPARK_HOME` environment variable (replace "YOU" with your Windows username):

   ```bash
   export SPARK_HOME="/mnt/c/Users/YOU/Ubuntu/Programs/spark-2.3.1-bin-hadoop2.7"
   ```

3. Save and close the file by pressing _Ctrl+x_, then _Shift+y_, and _Enter_.
4. After Successful installation of Spark, to get into Spark Shell using SCALA command 
```
spark-shell
```
---

### Additional Java Resource

If you need more details on the Java installation process, refer to this resource:
- [[java development kit jdk 22 installation guide for wsl 455f34676b45]]

---

