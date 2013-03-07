#!/usr/bin/python
import sys
import paramiko
import string
from datetime import datetime

# Fine place for some globals
array = paramiko.SSHClient()
array.set_missing_host_key_policy(paramiko.AutoAddPolicy())

hostname = "address or ip of your array here"
arr_username = "3paradm"
arr_password = "whatever your admin password is"
iops = []

# OPERATION: "Could have done this better"
#  Sure, there is probably some elegant way to do what im doing, but it got the job done,
#  This script is provided without warrenty and so on and so forth.

def connect():
        try:
                array.connect(hostname,username=arr_username,password=arr_password)
        except (paramiko.SSHException, socket.gaierror) as sshfail:
                print "SSH-FAILED: Problem establishing connection."
                print sshfail
                sys.exit(-1)

def collect(min = 1):
  global iops

  results = dict()
  while(min > 0):
    o = get_array_iops()
    o.readline()
  # print o.readlines() # lame ghetto debugging
    at_total = False

    for line in o.readlines():    
      split = string.split(line)

      if(at_total & len(split) > 0):
        results[split[1]] = split[2]

      if(len(split) == 1):
        at_total = True 

    iops.append(results)
    min -= 1;

def get_array_iops():
  i,o,e = array.exec_command('statvv -rw -d 60 -iter 1')
  return o

def print_data():
  global iops
  print datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
  print "total,read,write"
  for result in iops:
    print result['t']+","+result['r']+","+result['w']

if __name__ == "__main__":
  connect()
  for i in range(60):
    collect()
  print_data()
  array.close()
