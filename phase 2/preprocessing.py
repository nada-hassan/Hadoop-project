import os
import json
import time

folder_name = 'health_data'
for file_dir in os.listdir(folder_name):


    file_name = folder_name +"/" +file_dir

    with open(file_name, 'r') as file :
        filedata = file.read()

    # Replace the target string
    filedata = filedata.replace("'",'"')
    filedata = filedata.replace("}{",'}\n{')

    file.close()
    # Write the file out again
    with open(file_name, 'w') as file:
         file.write(filedata)

    file.close()

    with open(file_name,'r') as f:
        firstline = f.readline().rstrip()
        firstobj = json.loads(firstline)
        date = firstobj['Timestamp']
        datetime = time.strftime('%m-%d-%Y', time.localtime(date))
        os.rename(file_name, datetime+".json")

    f.close()
        



