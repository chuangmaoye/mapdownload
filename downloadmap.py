#!/usr/bin/env python
# coding: utf-8
import threading
import requests
import os
import math
import threading
import time
apiurl="https://api.mapbox.com/styles/v1/cyn888/cjhzwc9j34ow42rmp1gdhyc7t/tiles/256/%s/%s/%s@2x?access_token=pk.eyJ1IjoiY3luODg4IiwiYSI6ImNqaGs1bXEyeTJvbHYzNm03NXpkdGI2ZDQifQ.MGRV2RJACZe4qo5uMp1JOA"
dirmap="./map3"
downloadzoom=10
thred=100000
thrednum=0
mapzoom=[[0,0],[1,0],[3,1],[6,2],[13,5],[26,12],[52,24],[105,48],[210,97],[421,194],[843,387],[1685,776]]
print mapzoom
downloadmaps=[]

def download(zoom,xname,yname):
	try:
		downloadmaps.remove([zoom,xname,yname])
	except:
		return
	global thrednum
	global downloadmaps
	print "z:%s,x:%s,y:%s" %(zoom,xname,yname)
	zoompath="%s/%s" % (dirmap,zoom)
	iszoom=os.path.exists(zoompath)
	if not iszoom:
		try:
			os.makedirs(zoompath)
		except:
			pass
		
	xpath="%s/%s" % (zoompath,xname)
	isxname=os.path.exists(xpath)
	if not isxname:
		try:
			os.makedirs(xpath)
		except:
			pass
	imageurl=apiurl % (zoom,xname,yname)
	ypath="%s/%s.png" %(xpath,yname)
	if os.path.exists(ypath):
		try:
			pass
			#downloadmaps.remove([zoom,xname,yname])
		except:
			pass
		return
	try:
		r = requests.get(imageurl)
		with open(ypath, "wb") as code:
			code.write(r.content)
		# downloadmaps.remove([zoom,xname,yname])
	except:
		downloadmaps.append([zoom,xname,yname])
		return
	
def thremap(num):
	print num
	thred-=1
	for i in range(int(math.pow(2,num))):
			for j in range(int(math.pow(2,num))):
				download(str(num),str(i),str(j))
	thred+=1
def adddownloadmap(num):
	global thrednum
	global thred
	global downloadmaps
	print downloadmaps;
	for i in range(int(math.pow(2,num))):
			for j in range(int(math.pow(2,num))):
				# download(str(num),str(i),str(j))
				downloadmaps.append([str(num),str(i),str(j)])
				if len(downloadmaps)<thred:
					for tt in downloadmaps:
						t = threading.Thread(target=download,args=(tt[0],tt[1],tt[2]))
						# t.setDaemon(True)
						t.start()
				else:
					while len(downloadmaps)>=thred:
						time.sleep(0.1)



if __name__== '__main__':
	for k in range(downloadzoom+1):
		print k
		adddownloadmap(k)
		# t = threading.Thread(target=thremap,args=(k,))
		# # t.setDaemon(True)
		# t.start()
		
			

