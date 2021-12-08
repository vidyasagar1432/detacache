from datetime import datetime


def getCurrentTimestamp():
    return int(round(datetime.now().timestamp()))


def checkExpiredTimestamp(expire:int,initialTimestamp:int,currentTimestamp:int):
    return initialTimestamp + expire < currentTimestamp

# print(getCurrentTimestamp())

print(checkExpiredTimestamp(20,1639002240,1639002261))