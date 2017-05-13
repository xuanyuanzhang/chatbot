# Jarvis_6
import Stream
import threading
import Interpret
import hashlib  # using sha224
import sys
import re
import os
import subprocess
import time
import Message

# Master Operator
class Jarvis(object):    
    # Jarvis Object Instantiation
    def __init__(self):
        # Jarvis instantiation password
        self.truepass = hashlib.sha224('jarvis').hexdigest()
        # Jarvis clearance level
        self.clearance = 10
        self.wifi_dict = {'Strong':0, 'Moderate':1,'Weak':2, 'Very Weak':3, 'None':4}
        self.wifi_prev = 5    # some arbitrary number to start comparision in initialization
        self.wifi_thr = threading.Thread(target=self.ping, args=())
        self.wifi_current = 4 # initialize to no wifi
        self.state = False
        self.oInterpret = None
        self.oStream = None
        self.notifier = None

    def setup(self):
        self.state = self.password()
        if not self.state:
            sys.exit()
        self.wifi_thr.start()
            
        while 1:
            if self.wifi_current <= self.wifi_dict['Weak']:  # if connection is weak or better
                print "Creating Interpret and Stream objects..."
                # Create Interpret Object
                self.oInterpret = Interpret.Interpret()
                # Create Stream Object
                self.oStream = Stream.Stream(self.oInterpret)
                # Create Notifying Object
                self.notifier = threading.Thread(target=self.notify, args=())
                # Wifi Control on Interpret and Output
                print "Task Completed."
                break
            elif self.wifi_current == self.wifi_dict['Very Weak']: # wait until weak or better
                print 'Waiting for stronger ping status...'
                time.sleep(1)
            else:   # no wifi, then search
                print 'Searching for wifi...'
                time.sleep(1)

    def initiate(self):
        if not self.state:
            sys.exit()
        print 'Initiating objects...'
        # self.wifi_thr already started
        self.oStream.initiate()
        self.notifier.start()
    def terminate(self):
        self.wifi_thr.join()
        self.oStream.terminate()
        self.notifier.join()
    def wifi(self, mean):
        if 0 <= mean < 50:
            return self.wifi_dict['Strong']
        elif 50 <= mean < 300:
            return self.wifi_dict['Moderate']
        elif 300 <= mean < 500:
            return self.wifi_dict['Weak']
        else:
            return self.wifi_dict['Very Weak']
   
    def ping(self):
        while 1:
            avg = []       
            for i in xrange(3):
                try:
                    ping = subprocess.Popen(["ping.exe","www.google.com"], stdout = subprocess.PIPE)
                    out, error = ping.communicate()
                    if out:
                        try:
                            average = float(re.findall(r"Average = (\d+)", out)[0])
                            avg.append(average)
                            if len(avg) == 3:
                                self.wifi_current = self.wifi(sum(avg)/float(len(avg)))   # returns status of the mean of the avg
                        except:
                            self.wifi_current = self.wifi_dict['None']
                            break
                    else:
                        self.wifi_current = self.wifi_dict['None']
                        break
                except subprocess.CalledProcessError:
                    self.wifi_current = self.wifi_dict['None']
                    break
            time.sleep(10)
    def password(self):
        for i in range(5):
            usr_ans = raw_input("")
            encoded = hashlib.sha224(usr_ans).hexdigest()
            if encoded != self.truepass:
                print "Access Denied."
            else:
                os.system('cls')
                print "Access Granted."
                return True
        return False
    
    def notify(self):   # add clearance lvl distinction
        while 1:
            if self.wifi_current != self.wifi_prev and self.wifi_current>=3:    # wifi status changed and is bad
                msg = 'The ping status is %s.' %(self.wifi_dict.keys()[self.wifi_dict.values().index(self.wifi_current)])
                notif = Message.Message(msg, self.clearance, 5)         
                self.oStream.addRequest(notif)   
                self.wifi_prev = self.wifi_current
            time.sleep(5)


        
    
        
   
        
        
        