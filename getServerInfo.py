from mcstatus import JavaServer
from PIL import Image
import base64

def getInfo(ip):
	try:
		status = JavaServer(ip).status().raw
		return(status)
	except:
		return None
def getImage(ip):
	try:
#		status = JavaServer(ip).status
		with open("images/image.png", "wb") as server_icon_file:
			server_icon_file.write(base64.decodebytes(JavaServer(ip).status().icon))

	except:
		img = Image.open("images/check.png")
		img.save("images/image.png")
