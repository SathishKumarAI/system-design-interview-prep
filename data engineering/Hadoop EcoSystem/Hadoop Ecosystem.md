Apache Spark
	- Yarn
	- Map Reduce(MR)
	- HDFS(Hadoop Distributed File System)
	- 


HDFS - Distributed Storage
MR- Distributed Processing
YARN - Resource Management

HIVE - Data warehouse tool built on top of Apache Hadoop for providing data query and analysis.

PIG- scripting lang for data manipulation

SQOOP - cmd line interface for transferring data b/w relational dB and Hadoop.

HBASE - A col oriented NoSQL database that runs on top of HDFS.

OOZIE - workflow scheduler system to manage Apache Hadoop jobs

SPARK - distributed general purpose in-memory compute engine.

Replication Factor:  default Hadoop replication factor: 3


Heart Beat: Each data node sends an heart beat to Name Node in every 3 seconds. if NN doesn't receive   10 consecutive heart beats, it assumes that the DN is dead or running slow.

Fault Tolerance : if a data node goes down the replication factor came down to < 3.
then NN will create one more copy to maintain the replication factor.

from v2 of HDFS: NN single point of failure is avoided by using secondary NN.

Two Important metadata files: 
- FS image - Snapshot of the file system at a particular time
- Edit logs - transaction logs that changes in the HDFS file system.

