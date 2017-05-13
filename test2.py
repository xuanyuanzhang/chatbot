import speech_recognition as sr
import unicodedata
try:
    r = sr.Recognizer()      
except:
    raise
_input = ''   
# Listen
with sr.Microphone() as source:
    while 1:     
        audio = r.listen(source)

        # recognize speech using Google Speech Recognition
        try:
            _input = r.recognize_google(audio, key='AIzaSyBFxu68PiTw4aGcckoqiA9jRXaX12cDVzI')
            _input = unicodedata.normalize('NFKD', _input).encode('ascii','ignore')
            print "You said %s." %(_input)
        except:
            continue                   