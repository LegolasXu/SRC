import numpy as np
import serial
import serial.tools.list_ports
import cv2
import random
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
global cn
fullclk = False
clothclk = False
hatclk = False
pantsclk = False
resp=urlopen('http://www.weather.com.cn/weather/101020100.shtml')
soup=BeautifulSoup(resp,'html.parser')
tagDate=soup.find('ul', class_="t clearfix")
dates=tagDate.h1.string
tagToday=soup.find('p', class_="tem") 
try:
    temperatureHigh=tagToday.span.string
except AttributeError as e:
    temperatureHigh=tagToday.find_next('p', class_="tem").span.string
temperatureLow=tagToday.i.string
weather=soup.find('p', class_="wea").string
tagWind=soup.find('p',class_="win")
winL=tagWind.i.string
print(weather)
xcoord = 0
ycoord = 0
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
elif weather == 'rain':
    w = cv2.imread('umbrella.jpg')
    rd = cv2.imread('rd.jpg')
    w = cv2.resize(w,(100,100),interpolation=cv2.INTER_CUBIC)
    w[0:15,0:10]=rd[0:15,0:10]
    w[0:15,15:25] = rd[0:15,0:10]
    w[0:15,30:40] = rd[0:15,0:10]
    
elif weather == 'cloudy':
    w = cv2.imread('cloudy.jpg')
cn = random.randint(1,2)
pn = random.randint(1,2)
hn = random.randint(1,2)
hc = 0
cc = 0
pc = 0
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
        if 90<ycoord<180:
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
        if 230<xcoord<340 and 341<ycoord<459:
            print('cloth')
            fullclk = 'cloth'
            xcoord = 0
            ycoord = 0
        if 255<xcoord<310 and 460<ycoord<580:
            print('pants')
            fullclk = 'pants'
            xcoord = 0
            ycoord = 0
        if 260<xcoord<315 and 258<ycoord<300:
            print('hat')
            fullclk = 'hat'
            xcoord = 0
            ycoord = 0
cv2.namedWindow('result')
cv2.setMouseCallback('result',clickdetector)
def xykfullplan(cn,pn,hn):
    man = cv2.imread('man.jpg')
    pd = cv2.imread('msrc04.jpg')
    resw = cv2.resize(w,(100,100),interpolation=cv2.INTER_CUBIC)
    cf = "cloth"+str(cn)+".jpg"
    pf = "pants"+str(pn)+".jpg"
    hf = "hat"+str(hn)+".jpg"
    manimg = cv2.resize(man,(300,800),interpolation=cv2.INTER_CUBIC)
    imgc = cv2.imread(cf)
    imgp = cv2.imread(pf)
    imgh = cv2.imread(hf)
    chest = manimg[150:370,30:270]
    leg = manimg[370:750,0:300]
    head = manimg[0:50,90:210]
    imgcres = cv2.resize(imgc,(250,200),interpolation = cv2.INTER_CUBIC)
    imgpres = cv2.resize(imgp,(250,200),interpolation = cv2.INTER_CUBIC)
    imghres = cv2.resize(imgh,(250,200),interpolation = cv2.INTER_CUBIC)
    rowc,colc,channelc = imgcres.shape
    rowp,colp,channelp = imgpres.shape
    rowh,colh,channelh = imghres.shape
    chestres = cv2.resize(chest,(250,200),interpolation=cv2.INTER_CUBIC)
    legres = cv2.resize(leg,(250,200),interpolation=cv2.INTER_CUBIC)
    headres = cv2.resize(head,(250,200),interpolation=cv2.INTER_CUBIC)
    roic = chestres[0:rowc, 0:colc ]
    roip = legres[0:rowp,0:colp]
    roih = headres[0:rowh,0:colh]
    cv2.waitKey(0)
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
    finalc = cv2.resize(addedc,(280,210),interpolation=cv2.INTER_CUBIC)
    finalp = cv2.resize(addedp,(300,380),interpolation=cv2.INTER_CUBIC)
    finalh = cv2.resize(addedh,(120,50),interpolation=cv2.INTER_CUBIC)
    manimg[150:360,10:290 ] = finalc[0:210,0:280]
    manimg[370:750,0:300 ] = finalp[0:380,0:300]
    manimg[0:50,90:210] = finalh[0:50,0:120]
    manres = manimg
    pd[500:1300,365:665] = manres[0:800,0:300]
    res = cv2.resize(pd,(600,800),interpolation=cv2.INTER_CUBIC)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(res,'2019/2/'+cutdates,(100,90), font,0.5,(255,25,0),1)
    cv2.putText(res,cuttempL+'-'+cuttempH+' C',(140,215), font,0.5,(255,25,0),1)
    cv2.putText(res,'bag',(100,700), font,1,(0,0,255),2)
    cv2.putText(res,'red scarves',(100,730), font,1,(0,0,255),2)
    cv2.putText(res,'watch',(100,760), font,1,(0,0,255),2)
    res[95:195,110:210] = resw[0:100,0:100]
    pd[500:1300,365:665] = manres[0:800,0:300]
    res = pd
    res = cv2.resize(res(600,800),interpolation=cv2.INTER_CUBIC)
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
cv2.destroyAllWindows()

