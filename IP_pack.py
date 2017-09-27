#coding=utf8
import socket,struct,time,random
from icmp import *
#from scapy.all import *

#检验和
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
        self.Protocol=1
        self.Checksum=0
        self.Source=0
        self.Dest=0
    def ip_pack(self,source,dest):
        header=struct.pack('!BBHHHBB4s4s',(self.Version<<4)+self.Headerlength,self.DSCP,self.Totallength,self.Indentification,(self.reserved<<15)+(self.DF<<14)+(self.MF<<13)+self.offset,self.TTL,self.Protocol,socket.inet_aton(source),socket.inet_aton(dest))
       # print get_checksum(header)
        ip_header=struct.pack('!BBHHHBBH4s4s',(self.Version<<4)+self.Headerlength,self.DSCP,self.Totallength,self.Indentification,(self.reserved<<15)+(self.DF<<14)+(self.MF<<13)+self.offset,self.TTL,self.Protocol,get_checksum(header),socket.inet_aton(source),socket.inet_aton(dest))
        return ip_header
if __name__=='__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_RAW)
    host='192.168.10.199'
    port=0
    #s.bind(('3.3.3.3','1024'))
    ip_buf=IP()
    icmp=icmp_pack()
    icmp_buf=icmp.pack(20)
    #print icmp_buf
    subnet_range=sys.argv[1]
    subnet_min=subnet_range.split('-')[0].split('.')[3]
    subnet_max=subnet_range.split('-')[1]
    for i in range(int(subnet_min),int(subnet_max)):
        subnet_range==sys.argv[1]
        buf=ip_buf.ip_pack(subnet_range.split('-')[0][:-2]+'.'+str(i),'192.168.10.199')+"pppp"
        s.sendto(buf,(host,port))
