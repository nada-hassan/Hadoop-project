from mrjob.job import MRJob
from mrjob.step import MRStep
from mrjob.protocol import JSONValueProtocol
import json
import time

class NoRatings(MRJob):
   OUTPUT_PROTOCOL = JSONValueProtocol
   def steps(self):
        return[
            MRStep(mapper=self.mapper_get_ratings,
                  reducer=self.reducer_count_ratings)
        ]
#Mapper function 
   def mapper_get_ratings(self, _, line):
           data = json.loads(line.strip())
           key =  data['serviceName']
           yield key, data


#Reducer function
   def reducer_count_ratings(self, key, values):
       values = list(values)
      
       n = len(values)
      
       cpu, ram, disk , tc, tr, td = 0,0,0,0,0,0
       max_cpu, max_ram, max_disk = -1, -1, -1

       for i in range(n):

        c  = values[i]['CPU']
        rt = values[i]['RAM']['Total']
        rf = values[i]['RAM']['Free']
        dt = values[i]['Disk']['Total']
        df = values[i]['Disk']['Free']
        r  = (rt - rf) / rt
        d  = (dt - df) / dt
        cpu  += c
        ram  += r
        disk += d

        if max_cpu < c:
                max_cpu = c
                tc = time.strftime('%H:%M:%S', time.localtime(values[i]['Timestamp']))


        if max_ram < r:
                max_ram = r
                tr =  time.strftime('%H:%M:%S', time.localtime(values[i]['Timestamp']))

        if max_disk < d:
                max_disk = d
                td =  time.strftime('%H:%M:%S', time.localtime(values[i]['Timestamp']))
        
        avg_cpu, avg_ram, avg_disk = cpu/n, ram/n, disk/n
       
       yield None,{"name":key,"cpu":avg_cpu,"ram":avg_ram,"disk":avg_disk,"cpu_time":tc,"ram_time":tr,"disk_time":td,"count":n}

        #yield None,[key,avg_cpu,avg_ram,avg_disk,tc,tr,td,n].encode()


if __name__ == "__main__":
    NoRatings.run()