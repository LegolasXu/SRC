import cv2
import numpy as np
man = cv2.imread('man.jpg')
manimg = cv2.resize(man,(300,800),interpolation=cv2.INTER_CUBIC)
imgc = cv2.imread('cloth1.jpg')
imgp = cv2.imread('pants1.jpg')
imgh = cv2.imread('hat1.jpg')
chestres = manimg[150:370,30:270]
legres = manimg[370:750,0:300]
headres = manimg[0:50,90:210]
imgcres = cv2.resize(imgc,(240,220),interpolation = cv2.INTER_CUBIC)
imgpres = cv2.resize(imgp,(300,380),interpolation = cv2.INTER_CUBIC)
imghres = cv2.resize(imgh,(120,50),interpolation = cv2.INTER_CUBIC)
rowc,colc,channelc = imgcres.shape
rowp,colp,channelp = imgpres.shape
rowh,colh,channelh = imghres.shape
roic = chestres[0:rowc, 0:colc ]
roip = legres[0:rowp,0:colp]
roih = headres[0:rowh,0:colh]
cv2.imshow('chest',chestres)
cv2.imshow('leg',legres)
cv2.imshow('head',headres)
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
cv2.imshow('maskc',maskc_inv)
cv2.imshow('maskp',maskp_inv)
cv2.imshow('maskh',maskh_inv)
chest_bg = cv2.bitwise_and(roic,roic,mask = maskc)
leg_bg = cv2.bitwise_and(roip,roip,mask = maskp)
head_bg = cv2.bitwise_and(roih,roih,mask = maskh)
imgc_fg = cv2.bitwise_and(imgcres,imgcres,mask = maskc_inv)
imgp_fg = cv2.bitwise_and(imgpres,imgpres,mask = maskp_inv)
imgh_fg = cv2.bitwise_and(imghres,imghres,mask = maskh_inv)
addedc = cv2.add(chest_bg,imgc_fg)
addedp = cv2.add(leg_bg,imgp_fg)
addedh = cv2.add(head_bg,imgh_fg)
manimg[150:370,30:270 ] = addedc[0:220,0:240]
manimg[370:750,0:300 ] = addedp[0:380,0:300]
manimg[0:50,90:210] = addedh[0:50,0:120]
cv2.imshow('res',manimg)

cv2.waitKey(0)
cv2.destroyAllWindows()
