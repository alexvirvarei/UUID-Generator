# UUID-Generator
Implementation of a get_id() function which generates 64bit unique IDs over a netowork of up to 1024 nodes


Repository consists of 2 .py files, first being Node.py which has the implementation for the get_id() function inside the Node class and the second being test_node.py which represents the unit-testing module. 

1. "Please describe your solution to get_id and why it is correct i.e. guaranteed globally unique."
	- Each 64 bit UUID generated is formed as follows: 
		* first 10 bits are the node's id bits to ensure no two nodes will generate the same id
		* next 44 bits are the time in milliseconds passed since epoch. Epoch is usually 1 January 1970 00:00:00. This give us approximately 278 years to work with. It is presumed that the system time is the same for each node. Doing so, requests made at least 1ms apart will recieve different UUIDs.
		* last 10 bits are the bits to ensure that each millisecond up to 1024 unique IDs can be generated.

2. "Please explain how your solution achieves the desired performance i.e. 100,000 or more requests per second per node.  How did you verify this?"
	- In case of a uniform distribution of the requests 100,000/s are equal to 100/ms, since ms is the atomic time we work with here. Last 10 bits of the UUID make sure that in each specific millisecond, up to 1024 requests will get a different answer. 
	- In case the distribution is not uniform and all 100,000 requests are made in the same ms, the number will overflow. If so, the program loops untill the next millisecond so it can generate new IDs. The program can serve up to 1024000 unique IDs per second, without considering any other bottlenecking. 
	- It has been taken in consideration that it is impossible to wait for exactly 1ms to pass due to system constraints, and that is why the last part is 10 bits long instead of 8 (max 128 requests).
	- Verification has been made with the help of unit testing.

3. "Please enumerate possible failure cases and describe how your solution correctly handles each case.  How did you verify correctness?  Some example cases:"
	- Node crashes and comes back online in the same millisecond -> at startup the program sleeps for as little time as possible (still more than 1ms) so if the node already generated all 1024 UUIDs for that millisecond before the crash, and the internal state of it has been altered because of the crash, it will not try to generate the same 1024 UUIDs for the same ms, because the 44 bits of the timestamp will change.
	- Whole system crashes -> nodes are independent of each other, they don't need to communicate, so as long as each node is individually safe from crashing then the whole sytem is
	- Unexpected bugs -> functionality has been ensured by performing unit-testing on all the features a node is supposed to support. They are tested for uniqueness in a short period of time, during a reboot and between them. Also a check for an answer to 100,000 requests in under a second is performed.