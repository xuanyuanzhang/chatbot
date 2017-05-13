import socket
import threading
import Client
import hashlib  # sha384
import cryptography
import Message

class Mobile(object):
    def __init__(self, oInterpret):
        self.pass1 = hashlib.sha384('jarvis').hexdigest() # clearance 1 pwrd
        self.pass10 = hashlib.sha384('apple007').hexdigest() # clearance 10 pwrd
        self.delim = hashlib.sha384('delim').hexdigest() # delim
        self.DELIMLENGTH = len('delim') # length of delim
        self.oInterpret = oInterpret
        self.MAXCLIENTS = 2   # max number of clients
        self.MAXINTR = 10 # max number of interpreting threads
        self.clientlst = []
        self.clientthrlst = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        try:
            self.sock.bind(('',5001))
            self.sock.listen(10)
            self.Thread1 = threading.Thread(target=self.addClients)
        except socket.error as msg:
            print msg
   
    def addRequest(self, request):
        for client in self.clientlst:
            client.addRequest(request)
     
    def mobile(self):
        self.Thread1.start()
        self.Thread1.join()
        
    # Thread 1
    def addClients(self):
        while 1:
            try:
                conn, addr = self.sock.accept()            
                client = Client.Client(conn, addr[0])
                print "Client %s has connected." %(client.getAddr())
                if len(self.clientlst) < self.MAXCLIENTS:               
                    self.clientlst.append(client)
                    thread = threading.Thread(target=self.connect, args=(client,))
                    thread.start()
                    self.clientthrlst.append(thread)
                    client.updateThread(thread)
                else:
                    print 'Client %s has disconnected. Error: connection overload. Maximum clients reached.' %(client.getAddr())
                    client.sendto(cryptography.EncodeAES('max'))
                    client.close()
            except socket.error as msg:
                if msg[0] in [10053,10054,9]:  # if socket error raised
                    print 'Client %s has disconnected.' %(client.getAddr())
                client.close()
                         

    def delClient(self, client):
        self.clientlst.remove(client)
        self.clientthrlst.remove(client.getThread())
        client.close()

    # Thread 2
    def connect(self, client):
        success = self.updateClient(client)
        if success:
            ThreadInput = threading.Thread(target=self.queueInput, args=(client,))
            ThreadOutput = threading.Thread(target=self.queueOutput, args=(client,)) 
            ThreadInput.start()
            ThreadOutput.start()
            ThreadInput.join()
            ThreadOutput.join()
    def updateClient(self, client):
        success = False
        for i in range(5):
            try:
                client.sendto(cryptography.EncodeAES('password'))
                usr_ans = client.recvfrom(1024)
                if hashlib.sha384(usr_ans).hexdigest() == self.pass1:
                    client.updateClearance(1)
                    success = True
                    client.sendto(cryptography.EncodeAES('clearance1'))
                    break
                elif hashlib.sha384(usr_ans).hexdigest() == self.pass10:
                    client.updateClearance(10)
                    success = True
                    client.sendto(cryptography.EncodeAES('clearance10'))
                    break
                else:
                    client.sendto(cryptography.EncodeAES('denied'))
            except socket.error as msg:
                if msg[0] in [10053,10054,9]:  # if socket error raised
                    print 'Client %s has disconnected.' %(client.getAddr())
                client.close()
                break
        if not success and i==4:
            self.delClient(client)
            print 'Client %s has disconnected. Failed attempts limit reached.' %(client.getAddr())
        elif not success and i<4: # exception
            self.delClient(client)
        return success

    def queueInput(self, client):
        _input = ''
        while 1:
            try:
                _input = client.recvfrom(1024)
                # Stage 1 (Decrypt)
                _input = cryptography.DecodeAES(_input)
                if _input == None:
                    raise socket.error(9)
                # Stage 2 (Check Delim)
                if hashlib.sha384(_input[0:self.DELIMLENGTH]).hexdigest() == self.delim:  # delim equals
                    if _input[self.DELIMLENGTH:]:
                        request = Message.Message(_input[self.DELIMLENGTH:], client.getClearance(), 5)
                        client.addRequest(request)
                    else:
                        pass
                else:
                    client.sendto('You are unauthorized. Connection aborted.') # INTRUDER ALERT
                    client.close()
                    break
            except socket.error as msg:
                if msg[0] in [10053,10054,9]:  # if socket error raised
                    print 'Client %s has disconnected.' %(client.getAddr())
                client.close()
                break
        self.delClient(client)
        client.updateLife(False)
    def queueOutput(self, client):
        while client.is_alive():
            while not client.empty():
                res = self.oInterpret.interpret(client.getRequest())
                # res = self.oInterpret.test(request, client.getAddr())  # interpret phase
                output = cryptography.EncodeAES(res)
                if output == None:
                    continue
                try:
                    client.sendto(output)
                except socket.error as msg:
                    continue
                    '''if msg[0] in [10053,10054,9]:  # if socket error raised
                        print 'Client %s has disconnected.' %(client.getAddr())
                    client.close()'''
                    
        
    
                