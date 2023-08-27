from mcstatus import JavaServer
import json

server = JavaServer.lookup("matermanf.myddns.me")
#print(dir(server))
try:
	status = server.status().raw
	print(status)
except:
	print("Server Offline")


print("Server ip: {}\nVersion: {}".format(server.address.host,status["version"]["name"]))
