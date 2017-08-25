#coding=utf8
import socket,struct,time,random
#from scapy.all import *
class IP:
    def __init__(self):
        self.Version=4
        self.Headerlength=5
        self.DSCP=0x00
        self.Totallength=0x0028
        self.Indentification=0x64da
        self.reserved=0
        self.DF=1
        self.MF=0
        self.offset=0
        self.TTL=0x80
        self.Protocol=0x01
        self.Checksum=0
        self.Source=0
        self.Dest=0
    def ip_pack(self,source,dest):
        struct.pack('!',self.Version<<4+self.Headerlength,self.DSCP,self.Totallength,self.Indentification,self.,socket.inet_aton(self.Source),socket.inet_ntoa(self.Dest))

