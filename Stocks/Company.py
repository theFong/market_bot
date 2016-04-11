__author__ = 'AlecFong'
class Company(object):
    # name = ""
    # price = 0
    # change = 0
    # opinion = 0
    # preopin = 0
    # lwopin = 0
    # lmopin = 0
    # score = 0

    def __init__(self, n):
        self.name = n
        self.shares = 0

    def getPrice(self):
        return self.price

    def getChange(self):
        return self.change

    def getOpinion(self):
        return self.opinion

    def getPreopin(self):
        return self.preopin

    def getName(self):
        return self.name

    def setName(self, n):
        self.name = n

    def setPrice(self, p):
        self.price = p

    def setChange(self, c):
        self.change = c

    def setOpinion(self, op):
        self.opinion = op

    def setPreopin(self, preop):
        self.preopin = preop

    def setLWopin(self, lwop):
        self.lwopin = lwop

    def setLMopin(self, lmop):
        self.lmopin = lmop

    def getScore(self):
        self.score = ((float(self.opinion)*1.75)+(float(self.preopin)*.75)+
                      (float(self.lwopin)*.35)+(float(self.lmopin)*.2))