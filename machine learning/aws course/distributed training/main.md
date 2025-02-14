Distributed training ![[Pasted image 20241016144837.png]]

- [[distributed data parallelism]]
- Data parallelism  
	- Data parallelism is typically used when the data does not fit in a single device (one GPU, for example). With this technique, the dataset is sharded across multiple devices that contain a copy of the model.
	- At the beginning of a training step, a mini-batch is distributed equally in a non-overlapping manner across all the model replicas.
	- The replicas are then trained in parallel, and model parameters are continuously synchronized across devices. Collective communication algorithms and specialized high-performance computing (HPC) networking infrastructures are commonly used to implement parameter synchronization and efficient inter-device communication.
	[[AllReduce]]
	[[parameter server ]]
- Model parallelism
	- [[distributed model parallelism]]
	- [[Pipeline parallelism]]
		- https://explore.skillbuilder.aws/learn/course/17556/play/93188/addressing-the-challenges-of-building-language-models
		- 
	- 
	[[]]