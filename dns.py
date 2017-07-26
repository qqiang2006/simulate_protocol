#coding=utf8
import struct,random,socket
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
    def query(self,dnserver):
        req=['test','edit']
        header=struct.pack('!hhhhhh',self.TransactionID,self.Flags,self.Questions,self.AnswerRRs,self.AuthorityRRs,self.AddtionalRRs)
        for i in req:
            domain="www."+i+".com"
            dmp=domain.split('.')
            body=''
            for i in dmp:
                label=struct.pack('B%ds'%len(i),len(i),i)
                body+=label
            body+='\0'
            tail=struct.pack('!hh',self.QTYPE,self.QCLASS)
            Buf=header+body+tail
            s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            HOST = '192.168.99.151'
            PORT = 1024
            saddr = (HOST, PORT)
            s.bind(saddr)
            s.sendto(Buf,(dnserver,53))
            print "query" +' ' +domain + " "+ "is ok"
            data=s.recv(1024)
            print struct.unpack("4s", data[-4:])
            print socket.inet_ntoa(str(struct.unpack("!4s", data[-6:-2])))
            s.close()
if __name__=='__main__':
    dns_query=dns_pack()
    dns_query.query('114.114.114.114')