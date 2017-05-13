# coding: utf-8
import socket
import threading
import cryptography
import hashlib
import time
import sys

class Jarvis_Connect(object):
    def __init__(self):
        self.delim = 'delim' # delim
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        self.sock.settimeout(2)
        self._input = None
        self._output = None

    def initiate(self):
        self._input_stop = threading.Event()
        self._output_stop = threading.Event()
        self._input = threading.Thread(target=self.input_thr)
        self._output = threading.Thread(target=self.output_thr)

        self._input.start()
        self._output.start()

        self._input.join()
        self._output.join()

    def close(self):
        #encoded = cryptography.EncodeAES(self.delim + '***close***')
        #self.sock.sendall(encoded)
        self.sock.close()

    def connect(self, IP, PORT):
        success = False
        try:
            self.sock.connect((IP,PORT))
            success = True
        except:
            raise
        return success

    def input_thr(self):
        while (not self._output_stop.is_set()):
            try:
                line = raw_input("")
                encoded = cryptography.EncodeAES(self.delim+line)    
                self.sock.sendall(encoded)  # if clearance 1 granted, send encrypted(special delim + msg)

            except socket.error, e:
                if e[0] == 54:
                    print "Error: Jarvis has disconnected."
                    break
                else:
                    raise
                    break
            except:
                break
        self._input_stop.set()

    def output_thr(self):
        while (not self._input_stop.is_set()):
            try:
                res = self.sock.recv(1024)
                if res != '':   # if result is nonempty
                    try:
                        decoded = cryptography.DecodeAES(res)
                    except:
                        raise
                        decoded = "Decoding error. Message could not be retrieved."
                    print decoded
            except socket.timeout:
                pass                       
            except socket.error, e:
                if e[0] == 54:
                    print "Error: Jarvis has disconnected."
                break           
            except:
                break
        self._output_stop.set()

    def passcheck(self):
        line =''
        try:
            while 1:
                res = self.sock.recv(1024)
                decrypted = cryptography.DecodeAES(res)
                # clearance1
                if decrypted == 'clearance1':
                    print 'Access Granted to Clearance 1'
                    break       
                # clearance10    
                elif decrypted == 'clearance10':
                    print 'Access Granted to Clearance 10.'
                    break
                elif decrypted == 'password':
                    print 'Password: '
                    while not line:    
                        line = raw_input('')
                    self.sock.sendall(line)
                    line=''
                elif decrypted == 'max':
                    print 'Error: connection overload. Maximum clients reached.'
                    time.sleep(2)
                    sys.exit()
                elif decrypted == 'denied':
                    print "Access denied."
                    pass
                else:
                    time.sleep(2)
                    sys.exit()
        except socket.error as msg:
            if msg[0] in [10053,10054,9]:  # if socket error raised
                print 'Error: Jarvis has disconnected'
        except:
            time.sleep(1)
            raise

if __name__ == '__main__':
    #James iMac
    #IP = '100.8.233.176'
    #Columbia
    IP = '160.39.141.74'
    PORT = 5001
    oJarv = Jarvis_Connect()
    try:
        success = oJarv.connect(IP, PORT)
        if success:
            oJarv.passcheck()       
            oJarv.initiate()
    except KeyboardInterrupt:
        print "Interrupted"
    except:
        oJarv.close()
        time.sleep(1)
        

