import speech_recognition as sr
import unicodedata
import pyaudio
import threading
import Message 
from Queue import PriorityQueue

class Voice(object):
    def __init__(self, oInterpret):
        self.oInterpret = oInterpret
        self.requests = PriorityQueue()
        MAX = 10
        self.clearance = MAX
        try:
            self.r = sr.Recognizer()      
        except:
            raise

    def addRequest(self, request):
        self.requests.put((request.getPriority(),
                            request))
 
    def voice(self):       
        ThreadInput = threading.Thread(target=self.cueInput)
        ThreadOutput = threading.Thread(target=self.cueOutput)
        ThreadInput.start()
        ThreadOutput.start()
        ThreadInput.join()
        ThreadOutput.join()

    def cueInput(self):
        _input = ''   
        # Listen
        with sr.Microphone() as self.source:
            while 1:     
                audio = self.r.listen(self.source)

                # recognize speech using Google Speech Recognition
                try:
                    _input = self.r.recognize_google(audio)
                    _input = unicodedata.normalize('NFKD', _input).encode('ascii','ignore')
                    request = Message.Message(_input, self.clearance, 5)
                    self.addRequest(request)
                except:
                    continue 
    def cueOutput(self):
        while 1:
            while not self.requests.empty():
                res = self.oInterpret.interpret(self.requests.get()[1])
                # res = self.oInterpret.test(request, 'voice')
                if res == None:
                    continue
                print res # speak it later

