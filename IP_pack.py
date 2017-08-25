#coding=utf8
import socket,struct,time,random
from scapy.all import *
#校验和函数
def get_checksum(source):
    """
    return the checksum of source
    the sum of 16-bit binary one's complement
    """
    checksum = 0
    count = (len(source) / 2) * 2
    i = 0
    while i < count:
        temp = ord(source[i + 1]) * 256 + ord(source[i]) # 256 = 2^8
        checksum = checksum + temp
        checksum = checksum & 0xffffffff # 4,294,967,296 (2^32)
        i = i + 2

    if i < len(source):
        checksum = checksum + ord(source[len(source) - 1])
        checksum = checksum & 0xffffffff

    # 32-bit to 16-bit
    checksum = (checksum >> 16) + (checksum & 0xffff)
    checksum = checksum + (checksum >> 16)
    answer = ~checksum
    answer = answer & 0xffff

    # why? ans[9:16 1:8]
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer
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
        struct.pack('!',self.Version<<4+self.Headerlength,self.DSCP,self.Totallength,self.Indentification,self.)
