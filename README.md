# Hadoop-project
Building a system that can handle massive amounts of data in an efficient, distributed, and reliable manner.
## Phase 1
### Components 
#### 1- Monitor:
- Libraries: socket, threads, time, date time, hdfs,os
- Logic:
  
  1 - capacity buffer of 50 messages once full move its data to temp buffer
  
  2- the capacity buffer will be ready again to receive requests from any clients
  
  3- create file and move for it the temp buffer data
  
  4- connect to hdfs  in another thread and upload the created file with today date if not exists otherwise append for the existing one 
  
 #### 2- Client: 
- Libraries : socket , json , psutil , random
- Testing logic :
   
     1- get the current state of the client from cpu, ram, disk, time stamp

     2- create json object of these data

     3- connect to the socket and send the message data

### Extra software modules used
- hdfs 
- zookeeper
- google cloud
------------------------------------------------------------------
