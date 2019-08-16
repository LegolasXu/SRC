import pyaudio
import wave
from aip import AipSpeech
from xpinyin import Pinyin
import requests
#from weather import *
#from nature import *
from music import *
import os
from os import system
import win32com.client
speaker = win32com.client.Dispatch("SAPI.SpVoice")
 



CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 8000
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "audio.wav"


APP_ID = '15834169'
API_KEY = 'sG4lDgskMHePrG3GjoDGLR4t'
SECRET_KEY = 'fk8FILysQEqRAt66dQX9SIThGzVrIm7e'
client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

STATE = 0
TIME_START = 0
TIME_END = 0

num = 0
    

def playVoice(fileName):
    os.system("madplay -v " + fileName)
 

def readFile(fileName):
    with open(fileName, 'rb') as fp:
        return fp.read()
    
def writeFile(fileName,result):
    with open(fileName, 'wb') as fp:
        fp.write(result)
    
def getBaiduText():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    stream.start_stream()
    print("* 开始录音......")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
 
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    
    print("* 正在识别......")
    result = client.asr(readFile('audio.wav'), 'wav', 16000, {
    'dev_pid': 1536,
})
    if result["err_no"] == 0:
        for t in result["result"]:
            return t
    else:
        print("没有识别到语音")
        getBaiduVoice("I Am sorry ,i can't hear you,MAY be you can speak loudlier ")
        speaker.Speak("I Am sorry ,i can't hear you,MAY be you can speak loudlier" )
        return ""

def getBaiduVoice(text):
    result  = client.synthesis(text, 'zh', 6, {'vol': 5, 'per':4,'spd':5})
    if not isinstance(result, dict):
        writeFile("back.mp3",result)
    playVoice("back.mp3")

def getVoiceResult():
    return baiduVoice()

def getPinYin(result):
    pin = Pinyin()
    return pin.get_pinyin(result)

def ONE(result,pinyin):
    if getPinYin("裤子") in pinyin:
        print("你好")
        getBaiduVoice("HELLO,YOUR TOURSERS ARE COMING")
        speaker.Speak("HELLO,YOUR TOURSERS ARE COMING")              

    
def TWO(result,pinyin):
    if getPinYin("风衣") in pinyin:
        print("你好")
        getBaiduVoice("HELLO,YOUR Windbreaker IS COMING")
        speaker.Speak("HELLO,YOUR Windbreaker IS COMING")              

def THREE(result,pinyin):
    if getPinYin("牛仔裤") in pinyin:
        print("你好")
        getBaiduVoice("HELLO,YOUR Jeans IS COMING")
        speaker.Speak("HELLO,YOUR Jeans IS COMING")              

def FOUR(result,pinyin):
    if getPinYin("衬衫") in pinyin:
        print("你好")
        getBaiduVoice("HELLO,YOUR SHIRT IS COMING")
        speaker.Speak("HELLO,YOUR SHIRT IS COMING")              

            
def FIVE(result,pinyin):
    if getPinYin("T恤衫") in pinyin:
        print("你好")
        getBaiduVoice("HELLO,YOUR T-SHIRT IS COMING")
        speaker.Speak("HELLO,YOUR T-SHIRT IS COMING")              

def SIX(result,pinyin): 
    if getPinYin("帽子") in pinyin:
        print("你好")
        getBaiduVoice("HELLO,YOUR HAT IS COMING")
        speaker.Speak("HELLO,YOUR HAT IS COMING")              

def SEVEN(result,pinyin):
    if getPinYin("校服") in pinyin:
        print("你好")
        getBaiduVoice("HERE YOU GO")
        speaker.Speak("HERE YOU GO")  

result = getBaiduText()
pinyin = getPinYin(result)
print("等待唤醒")
print(result)
ONE(result,pinyin)
TWO(result,pinyin)
THREE(result,pinyin)
FOUR(result,pinyin)
FIVE(result,pinyin)
SIX(result,pinyin)
SEVEN(result,pinyin)
