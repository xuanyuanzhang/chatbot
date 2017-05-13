class Message(object):
    def __init__(self, msg, clearance, priority):
        self.msg = msg
        self.clearance = clearance # minimum
        self.priority = priority #1-5
    def getMsg(self):
        return self.msg
    def getClearance(self):
        return self.clearance
    def getPriority(self):
        return self.priority


