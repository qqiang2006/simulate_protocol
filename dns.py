#coding=utf8
'''
FORMAT	C TYPE	PYTHON TYPE	STANDARD SIZE	NOTES
x	pad byte	no value	 	 
c	char	string of length 1	1	 
b	signed char	integer	1	(3)
B	unsigned char	integer	1	(3)
?	_Bool	bool	1	(1)
h	short	integer	2	(3)
H	unsigned short	integer	2	(3)
i	int	integer	4	(3)
I	unsigned int	integer	4	(3)
l	long	integer	4	(3)
L	unsigned long	integer	4	(3)
q	long long	integer	8	(2), (3)
Q	unsigned long long	integer	8	(2), (3)
f	float	float	4	(4)
d	double	float	8	(4)
s	char[]	string	1 	 
p	char[]	string	 	 
P	void *	integer	 	(5), (3)
'''
import struct,random,socket,threading,time,thread
class dns_pack:
    def __init__(self):
        self.TransactionID=random.randint(1,32768)
        self.Flags=0x0100
        self.Questions=0x0001
        self.AnswerRRs=0x0000
        self.AuthorityRRs=0x0000
        self.AddtionalRRs=0x0000
        self.QTYPE=0x0001
        self.QCLASS=0x0001
    def query(self,domainname,dnserver):
        #dns封装，从上到下依次pack
        #头部
        #print time.ctime()
        header=struct.pack('!HHhhhh',self.TransactionID,self.Flags,self.Questions,self.AnswerRRs,self.AuthorityRRs,self.AddtionalRRs)
        #question,域名编码格式为按点号分片，之后字符长度加上字符，比如www.baidu.com等于3www5baidu3com
        dmp=domainname.split('.')
        body=''
        domain_length=0
        j=0#统计domain分成的label数
        for i in dmp:
            label=struct.pack('b%ds'%len(i),len(i),i)
            body+=label
            domain_length+=len(i)
            j+=1
        body+='\0'
        tail=struct.pack('!hh',self.QTYPE,self.QCLASS)
        Buf=header+body+tail
        #建立udp连接
        s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        HOST = ''
        PORT = 0
        saddr = (HOST, PORT)
        s.bind(saddr)
        s.sendto(Buf,(dnserver,53))
        print "Query" +' ' +domainname + " "+ "is ok"
        data,addr=s.recvfrom(1024)
        #print time.clock()
        #判断有answer是否为空
        if data[6:8]=='\x00\x00':
            print '域名解析失败'
        else:
            #计算域名长度，推导出Answer字段中域名解析的偏移量
            domain_offset=domain_length+j+1
            answer_offset=12+domain_offset+4
            type_offset=12+domain_offset+4+2
            #print struct.unpack('<h',data[33:35])
            if data[answer_offset+2:answer_offset+4] == '\x00\x01':#网络字节序采用bid endian存取，
                print 'this answer type is host address'
                print "Address:"+ socket.inet_ntoa(struct.unpack("4s",data[answer_offset+12:answer_offset+16])[0])
            elif data[answer_offset+2:answer_offset+4] == '\x00\x05':
                print 'this answer type is CNAME'
                cname_length=struct.unpack('!h',data[answer_offset + 10:answer_offset + 12])[0]
                if data[answer_offset+12+cname_length+2:answer_offset+12+cname_length+4] == '\x00\x01':
                    print 'this answer type is host address'
                    print "Address:" + socket.inet_ntoa(
                        struct.unpack("4s", data[answer_offset+12+cname_length+12:answer_offset+12+cname_length+16])[0])
            else:
                print '目前没考虑'

        s.close()
if __name__=='__main__':
    dns_query=dns_pack()
    domain_name=raw_input("Please input your domainname:").split(',')
    #实现并发
    threads=[]
    for i in range(int(domain_name[1])):
        t_i=threading.Thread(target=dns_query.query,args=(domain_name[0],'114.114.114.114'))
        threads.append(t_i)
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()