# Input Interpreter
import threading
import wolframalpha
import wikipedia
import threading
import Queue
import unicodedata

class Interpret(object):
    # Wikipedia
    # Wolfram Q35XX4-9AG2KK3Q9L
    # last resort: Google Search API:
    # collect data from very first link: all sentences w/ highlighted words.
    # "..."\n(source1)\n"..."\n(source2)\n"
    def __init__(self):
        self.wolfram = wolframalpha.Client('Q35XX4-9AG2KK3Q9L')
        self.NUMSEN = 5
        self.queue = Queue.Queue()
    def interpret(self, msg):
        priority = msg.getPriority()
        if priority == 1:   # notification
            return msg.getMsg()
        if msg.getMsg() == '':
            return None
        else: 
            ThreadWolf = threading.Thread(target=self.checkWolfram, args=(msg,))
            ThreadWiki = threading.Thread(target=self.checkWiki, args=(msg,))
            ThreadWolf.start()
            ThreadWiki.start()
            ThreadWolf.join()
            ThreadWiki.join()
            res = ''
            lst = []
            while not self.queue.empty():
                q = self.queue.get()
                lst.append(q)
                self.queue.task_done()
            for elt in lst:
                if elt[1]=='Wolfram':
                    if 'wikipedia' not in msg.getMsg() and elt[0]!='No information':
                        res += elt[0]
                    else:
                        lst.remove(elt)
                        res += lst[0][0]
                else:
                    pass
               
            return res

    def checkWolfram(self, msg):
        res = ''       
        try:
            q = self.wolfram.query(msg.getMsg())
            for pod in q.pods:
                for sub in pod.subpods:
                    if sub.plaintext != None and pod.title != u'Input interpretation':
                        res += unicodedata.normalize('NFKD', sub.plaintext).encode('ascii','ignore')+'\n'
        except:
            pass
        if res == '':
            res = 'No information.'
        self.queue.put((res, 'Wolfram'))
    def checkWiki(self, msg):
        try:
            res = wikipedia.summary(msg.getMsg(), sentences=self.NUMSEN)
            res = unicodedata.normalize('NFKD', res).encode('ascii','ignore')
        except wikipedia.PageError:
            res = 'No information.'
        except wikipedia.DisambiguationError as e:   
            res = 'DisambiguationError: %s may refer to:\n' %(msg.getMsg(),)
            for i in e.options:
                res += unicodedata.normalize('NFKD', i).encode('ascii','ignore')+'\n'
        self.queue.put((res, 'Wiki'))
    
    def test(self, msg, addr):
        # add clearance level for each output
        # do something with input
        if msg.getPriority() == 1:
            res = msg.getMsg()
        else:
            str = msg.getMsg()
            res = 'You sent %s from %s.' %(str, addr)
            # Final output MUST be this
        return res

