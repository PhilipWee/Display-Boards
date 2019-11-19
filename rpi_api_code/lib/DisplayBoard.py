from lib.SerialComm import SerialComm
from datetime import datetime

def display_text(text):
    hex_string = "FF02000200"+hex(len(text))[2:].zfill(2)+toHex(text)+"78FF03"
    hex_string = bytes.fromhex(hex_string)
    SerialComm().write(hex_string)
    print(hex_string)
    return

def display_time():
    d = datetime.now().strftime('%I:%M %p').center(12,' ')
    hex_string = "FF02000200"+hex(len(d))[2:].zfill(2)+toHex(d)+"78FF03"
    hex_string = bytes.fromhex(hex_string)
    SerialComm().write(hex_string)
    #print(hex_string)
    return

def flash():
    hex_string = bytes.fromhex("FF020011000214010000010078FF03")
    SerialComm().write(hex_string)
    print(hex_string)
    return

def directshow(height=1):
    if height ==1:
        hex_string = bytes.fromhex("FF020011000014010000010078FF03")
    else:
        hex_string = bytes.fromhex("FF020011000014010000040078FF03")
    SerialComm().write(hex_string)
    print(hex_string)
    return

def toHex(text):
    convert = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])
    return convert(text)
