import socket
import json
import psutil
import random
UDP_IP = "192.168.249.10"
UDP_PORT = 3500
services=['Ticketing Service','Account Service', 'Inventory Service','Shipping Service' ] 
MESSAGE = {
    "serviceName": services[random.randint(0, 3)],
    "Timestamp": int(psutil.boot_time()),
    "CPU": psutil.cpu_percent(),
    "RAM": {
        "Total": psutil.virtual_memory().total// (2**30),
        "Free": psutil.virtual_memory().free// (2**30)
    },
    "Disk": {
        "Total": psutil.disk_usage('/').total// (2**30),
        "Free": psutil.disk_usage('/').free// (2**30)
    },
}

# convert into JSON:
MESSAGE = json.dumps(MESSAGE)

print("UDP target IP: ", UDP_IP)
print("UDP target port: ", UDP_PORT)
print("message:", MESSAGE)



sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.sendto(MESSAGE.encode(), (UDP_IP, UDP_PORT))