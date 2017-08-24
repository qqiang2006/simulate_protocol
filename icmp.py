#coding=utf8
import struct,socket,time,random,os,sys
help_info='''
the command:python icmp.py [destination] [num]
such as:python icmp.py 8.8.8.8 4
Usage:
	destinaton - the destination of ping
	num        - the num of request
'''
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
def help():
    print help_info
#icmp header
class icmp_pack:
    def __init__(self):
        self.Type=0x08#request
        self.Code=0x00
        self.Checksum=0
        self.Identifier=my_ID = os.getpid() & 0xFFFF
        self.Sequencenumber=1
    def pack(self,data_length):
        ping_header=struct.pack('!bbHHh',self.Type,self.Code,self.Checksum,self.Identifier,self.Sequencenumber)
        data=(data_length-8)*'p'
        data=struct.pack('d',time.clock())+data
        checksum=get_checksum(ping_header+data)
        ping_data=struct.pack('!bbHHh',self.Type,self.Code,checksum,self.Identifier,self.Sequencenumber)
        return ping_data+data

#creat the socket
s=socket.socket(socket.AF_INET,socket.SOCK_RAW,1)
s.settimeout(5)
#print socket.getprotobyname('udp')
ping=icmp_pack()
if len(sys.argv)<3:
    help()
else:
    i=1
    IP_ping=sys.argv[1]
    num_ping=sys.argv[2]
    while not int(num_ping) or i<=int(num_ping):
        try:
            s.sendto(ping.pack(20),(IP_ping,0))
        except:
            print 'the socket is error'
        #received the response of the ping,include the ip header
        try:
            data,addr=s.recvfrom(1024)
            start_time=time.clock()#the time of receive the response
            print 'get reply in %f ms '% ((start_time-struct.unpack('d',data[28:36])[0])*1000)
        except:
            print "the request is timeout"
        i+=1
    s.close()
