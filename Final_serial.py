import numpy as np
import cv2
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import face_recognition
import os
import time
import serial
import serial.tools.list_ports
global cn
global w
global res
fullclk = True
clothclk = False
hatclk = False
pantsclk = False
ports = list(serial.tools.list_ports.comports())
ser=serial.Serial('/dev/ttyAMA0',9600,timeout=1)
resp=urlopen('http://www.weather.com.cn/weather/101020100.shtml')
soup=BeautifulSoup(resp,'html.parser')
tagDate=soup.find('ul', class_="t clearfix")
dates=tagDate.h1.string
tagToday=soup.find('p', class_="tem")
try:
    temperatureHigh=tagToday.span.string
except AttributeError as e:
    temperatureHigh=tagToday.find_next('p', class_="tem").span.string
xcoord = 0
ycoord = 0
cn = random.randint(1,2)
pn = random.randint(1,2)
hn = random.randint(1,2)
#coding=utf-8
#人脸识别类 - 使用face_recognition模块

path = "img/face_recognition"  # 模型数据图片目录
cap = cv2.VideoCapture(1)
total_face_encoding=[]
total_image_name = []
total_face_encoding = []
for fn in os.listdir(path):  #fn 表示的是文件名q
    print(path + "/" + fn)
    total_face_encoding.append(face_recognition.face_encodings(face_recognition.load_image_file(path+"/"+fn))[0])
    fn = fn[:(len(fn) - 4)]  #截取图片名（这里应该把images文件中的图片名命名为为人物名）
    total_image_name.append(fn)  #图片名字列表
#print ( total_image_name[0])
while (1):
    name="yang"
    ret, frame = cap.read()
    # 发现在视频帧所有的脸和face_enqcodings
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    # 在这个视频帧中循环遍历每个人脸
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        for i, v in enumerate(total_face_encoding):
            match = face_recognition.compare_faces(
                [v], face_encoding, tolerance=0.5)
            name = "Unknown"
            if match[0]:
                name = total_image_name[i]
                if name == 'Steven':
                    hn = 1
                    cn = 2
                    pn = 2
                if name == 'coco':
                    hn = 2
                    cn = 2
                    pn = 1
                if name == 'Emily':
                    hn = 1
                    cn = 1
                    pn = 2
                break
        # 画出一个框，框住脸
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # 画出一个带名字的标签，放在框下
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255),
                      cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0,
                    (255, 255, 255), 1)
    # 显示结果图像
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
hc = 0
cc = 0
pc = 0

cap = cv2.VideoCapture(1)
def clickdetector(event,x,y,flags,param):
    global fullclk
    global hatclk
    global clothclk
    global pantsclk
    if event==cv2.EVENT_LBUTTONDBLCLK:
        fullclk = True
    if event==cv2.EVENT_LBUTTONDOWN:
        print('mouse coords:',x,y)
        xcoord = x
        ycoord = y
        print(xcoord,ycoord)
        if 90<ycoord<190 and 380<xcoord<510:
            print (hn,cn,pn)
            if hn == 1:
                hc = 'A'
            if hn == 2:
                hc = 'B'
            if cn == 1:
                cc = 'C'
            if cn == 2:
                cc = 'D'
            if pn == 1:
                pc = 'E'
            if pn == 2:
                pc = 'F'
            print(hc,cc,pc)
            ser.write(hc.encode())
            cv2.waitKey(10)
            ser.write(cc.encode())
            cv2.waitKey(10000)
            ser.write(pc.encode())
        if 235<xcoord<375 and 340<ycoord<450:
            print('cloth')
            fullclk = 'cloth'
            xcoord = 0
            ycoord = 0
        if 245<xcoord<360 and 460<ycoord<650:
            print('pants')
            fullclk = 'pants'
            xcoord = 0
            ycoord = 0
        if 275<xcoord<340 and 260<ycoord<290:
            print('hat')
            fullclk = 'hat'
            xcoord = 0
            ycoord = 0
        if 590<xcoord<640 and 750<ycoord<800:
            print('sound')
            import voice_serial
cv2.namedWindow('result')
cv2.setMouseCallback('result',clickdetector)
def xykfullplan(cn,pn,hn):
    ah = cv2.imread('airhorn.jpg')
    ahres = cv2.resize(ah,(50,50),interpolation = cv2.INTER_CUBIC)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(1)
    retf, framef = cap.read()
    gray = cv2.cvtColor(framef, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        res = cv2.imread('msrc04.jpg')
        cutface = framef[y:y+h,x:x+w]
        face = cv2.resize(cutface,(90,100),interpolation = cv2.INTER_CUBIC)
        temperatureLow=tagToday.i.string
        weather=soup.find('p', class_="wea").string
        tagWind=soup.find('p',class_="win")
        winL=tagWind.i.string
        cutdates = dates[0:2]
        cutwindlevel = winL[0:2]
        cuttempL = temperatureLow[0:1]
        cuttempH = temperatureHigh[0:2]
        if weather[0] == '晴':
            weather = 'clear'
        elif weather[1] == '雨' or weather[1] == '雨':
            weather = 'rain'
        elif weather[0] != '晴' and weather[0] != '雨' and weather[1] != '雨':
            weather = 'cloudy'
        if weather == 'clear':
            w = cv2.imread('sun.jpg')
            w = cv2.resize(w,(100,100),interpolation=cv2.INTER_CUBIC)
        elif weather == 'rain':
            w = cv2.imread('umbrella.jpg')
            rd = cv2.imread('rd.jpg')
            w = cv2.resize(w,(100,100),interpolation=cv2.INTER_CUBIC)
            w[0:15,0:10]=rd[0:15,0:10]
            w[0:15,15:25] = rd[0:15,0:10]
            w[0:15,30:40] = rd[0:15,0:10]
        elif weather == 'cloudy':
            w = cv2.imread('cloudy.jpg')
            w = cv2.resize(w,(100,100),interpolation=cv2.INTER_CUBIC)
        man = cv2.imread('man.jpg')
        manimg = cv2.resize(man,(300,800),interpolation=cv2.INTER_CUBIC)
        manimg[33:133,105:195] = face
        imgc = cv2.imread('cloth'+str(cn)+'.jpg.')
        imgp = cv2.imread('pants'+str(pn)+'.jpg')
        imgh = cv2.imread('hat'+str(hn)+'.jpg')
        chestres = manimg[140:380,10:290]
        legres = manimg[380:750,10:290]
        headres = manimg[0:50,80:220]
        imgcres = cv2.resize(imgc,(280,240),interpolation = cv2.INTER_CUBIC)
        imgpres = cv2.resize(imgp,(280,370),interpolation = cv2.INTER_CUBIC)
        imghres = cv2.resize(imgh,(140,50),interpolation = cv2.INTER_CUBIC)
        rowc,colc,channelc = imgcres.shape
        rowp,colp,channelp = imgpres.shape
        rowh,colh,channelh = imghres.shape
        roic = chestres[0:rowc, 0:colc ]
        roip = legres[0:rowp,0:colp]
        roih = headres[0:rowh,0:colh]
        imgcgray = cv2.cvtColor(imgcres,cv2.COLOR_BGR2GRAY)
        imgpgray = cv2.cvtColor(imgpres,cv2.COLOR_BGR2GRAY)
        imghgray = cv2.cvtColor(imghres,cv2.COLOR_BGR2GRAY)
        retc, maskc = cv2.threshold(imgcgray, 254, 255, cv2.THRESH_BINARY)
        retp, maskp = cv2.threshold(imgpgray, 254, 255, cv2.THRESH_BINARY)
        reth, maskh = cv2.threshold(imghgray, 254, 255, cv2.THRESH_BINARY)
        maskc_inv = cv2.bitwise_not(maskc)
        maskp_inv = cv2.bitwise_not(maskp)
        maskh_inv = cv2.bitwise_not(maskh)
        chest_bg = cv2.bitwise_and(roic,roic,mask = maskc)
        leg_bg = cv2.bitwise_and(roip,roip,mask = maskp)
        head_bg = cv2.bitwise_and(roih,roih,mask = maskh)
        imgc_fg = cv2.bitwise_and(imgcres,imgcres,mask = maskc_inv)
        imgp_fg = cv2.bitwise_and(imgpres,imgpres,mask = maskp_inv)
        imgh_fg = cv2.bitwise_and(imghres,imghres,mask = maskh_inv)
        addedc = cv2.add(chest_bg,imgc_fg)
        addedp = cv2.add(leg_bg,imgp_fg)
        addedh = cv2.add(head_bg,imgh_fg)
        manimg[140:380,10:290 ] = addedc[0:240,0:280]
        manimg[380:750,10:290 ] = addedp[0:370,0:280]
        manimg[0:50,80:220] = addedh[0:50,0:140]
        res[500:1300,365:665] = manimg[0:800,0:300]
        res[250:350,100:200] = w
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(res,'2019/2/'+cutdates,(100,90), font,1,(255,25,0),2)
        cv2.putText(res,cuttempL+'-'+cuttempH+' C',(100,120), font,1,(255,25,0),2)
        cv2.putText(res,'bag',(100,150), font,1,(0,0,255),2)
        cv2.putText(res,'red scarves',(100,180), font,1,(0,0,255),2)
        cv2.putText(res,'watch',(100,210), font,1,(0,0,255),2)
        res = cv2.resize(res,(640,800),interpolation=cv2.INTER_CUBIC)
        res[750:800,590:640] = ahres
        return res
    res = xykfullplan(cn,pn,hn)
    cv2.imshow('result',res)
cv2.setMouseCallback('result',clickdetector)
while True:
    if fullclk == True:
        cv2.destroyAllWindows()
        cn = random.randint(1,2)
        pn = random.randint(1,2)
        hn = random.randint(1,2)
        res = xykfullplan(cn,pn,hn)
        cv2.imshow('result',res)
        cv2.setMouseCallback('result',clickdetector)
        fullclk = False
    if fullclk == 'cloth':
        cv2.destroyAllWindows()
        cn = random.randint(1,2)
        res = xykfullplan(cn,pn,hn)
        cv2.imshow('result',res)
        cv2.setMouseCallback('result',clickdetector)
        fullclk = False
    if fullclk == 'pants':
        cv2.destroyAllWindows()
        pn = random.randint(1,2)
        res = xykfullplan(cn,pn,hn)
        cv2.imshow('result',res)
        cv2.setMouseCallback('result',clickdetector)
        fullclk = False
    if fullclk == 'hat':
        cv2.destroyAllWindows()
        hn = random.randint(1,2)
        res = xykfullplan(cn,pn,hn)
        cv2.imshow('result',res)
        cv2.setMouseCallback('result',clickdetector)
        fullclk = False
    if cv2.waitKey(10)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()

