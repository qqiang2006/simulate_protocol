#coding=utf8
import struct,socket,time,random
#校验和函数
def do_checksum(data):
    """  Verify the packet integritity """
    sum = 0
    max_count = (len(data) / 2) * 2
    count = 0
    while count < max_count:  # 分割数据每两比特(16bit)为一组
        val = ord(data[count + 1]) * 256 + ord(data[count])
        sum = sum + val
        sum = sum & 0xffffffff
        count = count + 2

    if max_count < len(data):  # 如果数据长度为基数,则将最后一位单独相加
        sum = sum + ord(data[len(data) - 1])
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)  # 将高16位与低16位相加直到高16位为0
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer  # 返回的是十进制整数

#icmp header
class icmp_pack:
    def __init__(self):
        self.Type='0x08'#request
        self.Code='0x00'
        self.Checksum=0
        self.Identifier=random(1,65535)
        self.Sequencenumber=1
    def pack(self,data_length):
        ping_header=struct.pack('bbHHH',self.Type,self.Code,self.Identifier,self.Sequencenumber)
        data=(data_length-8)*'p'
        data=struct.pack('d',time.time())+data
        checksum=do_checksum(data)
        ping_data=struct.pack('bbHHH',self.Type,self.Code,checksum,self.Identifier,self.Sequencenumber)
        return ping_data

#creat the socket
s=socket.socket(socket.AF_INET,socket.SOCK_RAW)
HOST = ''
PORT = 0
saddr = (HOST, PORT)
s.bind(saddr)
ping=icmp_pack()
s.sendto(ping.pack(192),('114.114.114.114',0))
data,addr=s.recvfrom(1024)
print data