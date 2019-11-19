from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from DisplayBoard import DisplayBoard
import RelayLib
import json
 
pnconfig = PNConfiguration()
 
pnconfig.subscribe_key = 'sub-c-d134ece0-1b94-11e9-af54-8afa0e558510' 
pubnub = PubNub(pnconfig)
 
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        print("present!")
        # handle incoming presence data
 
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            print("Connection lost!")
            # This event happens when radio / connectivity is lost
 
        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            print("Connected & Listening..")

        elif status.category == PNStatusCategory.PNReconnectedCategory:
            print("Reconnected!")
            
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            print("Decyption error!")
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
 
    def message(self, pubnub, message):
        displayBoard = DisplayBoard()
        print(message.message)
        obj = json.loads(message.message)

        if 'cmd' in obj:
            displayBoard.display_text("Welcome".center(12,' '))
            RelayLib.TriggerGate()
        else:
            code = obj.get("pin","")
            displayBoard.display_text(code.center(12,' '))
        pass  # Handle new message stored in message.message
 
 
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('Channel-jxg830lpl').execute()
