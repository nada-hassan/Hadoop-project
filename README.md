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
## Phase 2
### Data-preparation
- convert the data to the shape that can be used easily 
- convert all the strings to json objects 
- rename the files with date 

### Components 
- Front-end :
          - Home Page : two date pickers in form 
          - Data analysis page: to show services analytics 
          - Back-end: get request to collect the data from the reducer with certain files that satisfies the required date range    
- map-reduce.py
           - maps the total data from all the required files to dict and send it to the reducer to make the required analysis and statistics
### Extra software modules used
- Django
- MrJob
--------------------------------------------------------------------------
## Phase 3
### Components 
#### 1- Map-Reduce job:
- libraries: mrjob, json
- flow: 
  - mapper: maps the records according to (service, time for each minute)
  - reducer: outputs service name and timestamp of minutes as key and total cpu, total ram, total disk, peak time for cpu, peak time for ram, peak time for disk, maximum cpu, maximum ram, maximum disk, total number of messages
### 2- Spark:
- queuing: store new message in csv file 
- streaming: each 30 sec change messages in csv file to rdd (key/value) then process them to be (key and total cpu, total ram, total disk, peak time for cpu, peak time for ram, peak time for disk, maximum cpu, maximum ram, maximum disk, total number of messages)
- parquet: append the output in parquet file
### 3- Scheduler: 
- libraries: os, subprocess, json, datetime, pandas, pyarrow, time, shutil, threading
- BatchView:  
    - 4 Batch views (one for each service)
    - Recomputational on the main dataset
- RealTime View:
    - within the hour update the real time by appending 
           new messages in csv file as queue
    - after one hour, create a new one and update them    
          until creating batch view
    -  once the batch view is created, incrementally 
          update one of the real times and delete the other
### 4- schema: 
   
     service  → String

     time_stamp → String

     cpu → Double

     ram → Double

     disk → Double

     max_cpu_time → String 

     max_cpu → Double

     max_ram_time → String 

     max_ram → Double

     max_disk_time → String 

     max_disk → Double

   msg_num → Integer
### Assumptions and design decisions
- Batch views partitioned on service names which gives us 4 batch views as we have 4 services and each service is sorted according to datetime
- Recomputational BatchView

