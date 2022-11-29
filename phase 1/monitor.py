import socket
import threading
import time
import os
from hdfs import InsecureClient
from datetime import datetime
UDP_IP = "192.168.249.10"
UDP_PORT = 3500

client = InsecureClient('http://host:port', user='hadoopuser')
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

# Shared Memory variables
CAPACITY = 50
buffer = []

# Declaring Semaphores
mutex = threading.Semaphore()
# empty = threading.Semaphore(CAPACITY)
# full = threading.Semaphore(0)
 
# Producer Thread Class
class Reciever(threading.Thread):
  def run(self):
    while True:
        global CAPACITY, buffer
        global mutex, empty, full
        
        recieved_messages = 0
        
        while recieved_messages < CAPACITY:
            print(len(buffer))
            mutex.acquire()
            
            data, addr = sock.recvfrom(1024)
            buffer.append(data.decode())
            
            mutex.release()
            
            time.sleep(0.3)
            
            recieved_messages += 1
 
# Consumer Thread Class
class Sender(threading.Thread):
  def run(self):
    while True: 
        global CAPACITY, buffer, in_index, out_index
        global mutex, empty, full
        
        if len(buffer) == CAPACITY:   
            mutex.acquire()
            
            batch = buffer
            buffer = []
            mutex.release()
            
            now = datetime.now()
            # convert to string
            date_str = now.strftime("%d_%m_%Y")
            f = open('/home/hadoopuser/tmplog'+ date_str+'.log', "w")
            f.write(str(batch))
            f.close()
           

            hadoop_time = datetime.now()
            start_time =  int(hadoop_time.strftime("%S"))

            os.system('/usr/local/hadoop/bin/hdfs dfs -appendToFile /home/hadoopuser/tmplog'+ date_str+'.log /' + date_str + '.log')

            hadoop_time = datetime.now()
            end_time =  int(hadoop_time.strftime("%S"))

            print("HADOOP TIME ", str(end_time - start_time))
           
            #time.sleep(1)



# Creating Threads
reciever = Reciever()
sender = Sender()
 
# while True:
# Starting Threads
sender.start()
reciever.start()
# Waiting for threads to complete
reciever.join()
sender.join()



