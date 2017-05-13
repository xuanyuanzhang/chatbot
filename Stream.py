import Console
import Voice
import Mobile
import threading

class Stream(object):
    def __init__(self, oInterpret):
        self.oConsole = Console.Console(oInterpret)
        self.oVoice = Voice.Voice(oInterpret)
        self.oMobile = Mobile.Mobile(oInterpret)

        self.consolethr = threading.Thread(target=self.oConsole.console)
        self.voicethr = threading.Thread(target=self.oVoice.voice)
        self.mobilethr = threading.Thread(target=self.oMobile.mobile)

    def initiate(self):
        # Launching Console Thread
        self.consolethr.start()
        print 'Console Thread successfully launched.'
        # Launching Voice Thread 
        self.voicethr.start()
        print 'Voice Thread successfully launched.'
        # Launching Mobile Thread
        self.mobilethr.start()
        print 'Mobile Thread successfully launched.'

    def terminiate(self):
        self.consolethr.join()
        self.voicethr.join()
        self.mobilethr.join()

    def addRequest(self, notif):
        self.oConsole.addRequest(notif)
        self.oVoice.addRequest(notif)
        self.oMobile.addRequest(notif)

