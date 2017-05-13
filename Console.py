import threading
import Message
from Queue import PriorityQueue

class Console(object):
    def __init__(self, oInterpret):
        self.oInterpret = oInterpret
        self.requests = PriorityQueue()
        MAX = 10
        self.clearance = MAX
        
    def addRequest(self, request):
        self.requests.put((request.getPriority(),
                                request))

    def console(self):       
        ThreadInput = threading.Thread(target=self.cueInput)
        ThreadOutput = threading.Thread(target=self.cueOutput)
        ThreadInput.start()
        ThreadOutput.start()
        ThreadInput.join()
        ThreadOutput.join()

    def cueInput(self):
        _input = ''
        while 1:
            _input = raw_input("")
            request = Message.Message(_input, self.clearance, 5)
            self.addRequest(request)
    def cueOutput(self):
        while 1:
            while not self.requests.empty():
                res = self.oInterpret.interpret(self.requests.get()[1])
                # res = self.oInterpret.test(request, 'console')
                if res == None:
                    continue
                print res
        


