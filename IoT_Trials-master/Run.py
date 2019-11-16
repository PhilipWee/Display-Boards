from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from threading import Event
from lib import DisplayBoard
from lib import RelayLib
import json
import time
import TimerClasses
import os

pnconfig = PNConfiguration()
 
pnconfig.subscribe_key = 'sub-c-d134ece0-1b94-11e9-af54-8afa0e558510' 
pubnub = PubNub(pnconfig)
 
class MySubscribeCallback(SubscribeCallback):
    def __init__(self,stopTimer):
        self.stopTimer = stopTimer
        pass

    def presence(self, pubnub, presence):
        print("present!")
 
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            print("Connection lost!")
 
        elif status.category == PNStatusCategory.PNConnectedCategory:
            print("Connected & Listening..")

        elif status.category == PNStatusCategory.PNReconnectedCategory:
            print("Reconnected!")

        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            print("Decyption error!")
 
    def message(self, pubnub, message):
        print(message.message)
        try:
            obj = json.loads(message.message)

            if 'cmd' in obj:
                stopTimer.set()
                DisplayBoard.display_text("Welcome".center(12,' '))
                RelayLib.timer_relay_trigger(1,2)
                TimerClasses.EventTimer(stopTimer).start()
            else:
                if "pin" in obj:
                    code = obj.get("pin","")
                    stopTimer.set()
                    TimerClasses.EventTimer(stopTimer,False,30).start()
                    DisplayBoard.display_text(code.center(12,' '))
                elif "parking_slots_left" in obj:
                    parking_slots_left = obj.get("parking_slots_left")
                    if parking_slots_left == 0:
                        DisplayBoard.display_text("V.Park Full".center(12,' '))
                        stopTimer.set()
                    else:
                        stopTimer.clear()
        except:
            pass

def getChannel():
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir,'config.json')) as json_file:  
        config = json.load(json_file)
        channel = "sma"+config["condo_name"][0:4]+config["condo_id"]
        print(channel)
        return channel

if __name__ == "__main__" :
    stopTimerThread = Event()
    stopTimer = Event()
    realClock = TimerClasses.RealClock(stopTimerThread,stopTimer)
    realClock.start()
    DisplayBoard.directshow(1)
    pubnub.add_listener(MySubscribeCallback(stopTimer))
    pubnub.subscribe().channels(getChannel()).execute()
