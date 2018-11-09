import argparse
import base64
import httplib2
#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials                    
DISCOVERY_URL='https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
import pygame
import json
import picamera
import time
import cv2
import numpy as np
#import matplotlib.pyplot as plt
from scipy.stats import itemfreq
import webbrowser
import urllib2
import urllib
import re
import vlc
import pafy
import random
import Image
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
import serial


sys.setdefaultencoding('utf-8')


global path
#img=cv2.imread('/home/pi/Desktop/camera/test1.jpg')
img=Image.open('/home/pi/Desktop/camera/test1.jpg')

for_sep=[] #initiate list that saves the result from google vision api 

clock=pygame.time.Clock()

music_link=[]

#ser=serial.Serial("/dev/ttyUSB1",9600)



def find_avg_color():
    #clustering k-means centers	   
    #CALCULATE AVERAGE RGB COLOR 
    #img = cv2.imread('/home/pi/camera/cam.jpg')
    average_color = [img[:, :, i].mean() for i in range(img.shape[-1])]
    arr = np.float32(img)
    pixels = arr.reshape((-1, 3))
    n_colors = 8
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, centroids = cv2.kmeans(pixels, 5 , criteria, 10, flags)

    palette = np.uint8(centroids)
    quantized = palette[labels.flatten()]
    quantized = quantized.reshape(img.shape)
    dominant_color = palette[np.argmax(itemfreq(labels)[:, -1])]
    print(dominant_color)



def most_frequent_colour(img):

    w, h = img.size
    pixels = img.getcolors(w * h)

    most_frequent_pixel = pixels[0]

    for count, colour in pixels:
        if count > most_frequent_pixel[0]:
            most_frequent_pixel = (count, colour)


    return most_frequent_pixel




def takephoto():
    
    camera = picamera.PiCamera()
    camera.resolution = (1080,1920) #resize  resolution 
        

    camera.capture('/home/pi/Desktop/camera/test1.jpg')
#   camera.capture('/home/pi/camera/test1.jpg',resize=(320,240))#resize captured cam 
    camera.close()

def classify():

    
    global path
    #Lonely
    atmos1=['sad','gloomy','red sky at morning','afterglow','sunrise','sunset','lonely']
    #Entertain
    atmos2=['dynamic','funny',' humorous',' witty',' exciting',' amusement park','club','rock concert','stage','crowd','disco','entertain','entertainment','performance']
    #Romance
    atmos3=['romance','kiss','love','bride','wedding']
    #Happy
    atmos4=['smile','fun','smily','happiness']
    #Healing
    atmos5=['leaf','nature','sky','ocean','bird','dog like mammal','puppy','infant','child']
      
    #classify
    for i in range(0,len(for_sep)) :
        for j in range(0,len(atmos1)) :
            if for_sep[i]==atmos1[j]  :
              	path="Lonely sound" 
		return path
                #classify
        #return the path which represents the proper music's path....<- couldn't find proper atmosphere and Path
    for i in range(0,len(for_sep)) :
        for j in range(0,len(atmos2)) :
            if for_sep[i]==atmos2[j] :
		path="edm, entertain sound bgm"
                return path
    for i in range(0,len(for_sep)) :
        for j in range(0,len(atmos3)) :
            if for_sep[i]==atmos3[j] :
		path="Romance sound"
                return path
    for i in range(0,len(for_sep)) :
        for j in range(0,len(atmos4)) :
            if for_sep[i]==atmos4[j] :
		path="Happy sound"
                return path
    for i in range(0,len(for_sep)) :
        for j in range(0,len(atmos5)) :
            if for_sep[i]==atmos5[j]:
		path="Healing Sound"
                return path

    path="nice classic sound"
    return path



def play_music():


    global path

    pygame.init()
    pygame.mixer.init()
    
    
    if path=="Lonely sound":
        i=random.randint(1,11)
        print("i=",i)
        music=pygame.mixer.Sound('/home/pi/Desktop/sound/lonely/'+str(i)+'.wav')

        clock=pygame.time.Clock()
        music.play()
        time.sleep(30) #control how long the music will play
    if path=="edm, entertain sound bgm":
        i=random.randint(1,8)
        print("i=",i)
        music=pygame.mixer.Sound('/home/pi/Desktop/sound/entertain/'+str(i)+'.wav')
        clock=pygame.time.Clock()
        music.play()
        time.sleep(30) #control how long the music will play
    if path=="Romance sound":
        i=random.randint(1,12)
        print("i=",i)
        music=pygame.mixer.Sound('/home/pi/Desktop/sound/romantic/'+str(i)+'.wav')
        clock=pygame.time.Clock()
        music.play()
        time.sleep(30) #control how long the music will play
    if path=="Happy sound":
        i=random.randint(1,7)
        print("i=",i)
        music=pygame.mixer.Sound('/home/pi/Desktop/sound/happy/'+str(i)+'.wav')
        clock=pygame.time.Clock()
        music.play()
        time.sleep(30) #control how long the music will play
    if path=="Healing Sound":
        i=random.randint(1,4)
        print("i=",i)
        music=pygame.mixer.Sound('/home/pi/Desktop/sound/healing/'+str(i)+'.wav')
        clock=pygame.time.Clock()
        music.play()
        time.sleep(30) #control how long the music will play
    if path=="nice classic sound":
        i=random.randint(1,7)
        print("i=",i)
        music=pygame.mixer.Sound('/home/pi/Desktop/sound/classic/'+str(i)+'.wav')
        clock=pygame.time.Clock()
        music.play()
        time.sleep(30) #control how long the music will play







def playsound():
        pygame.init()
        pygame.mixer.init()
        
        #depedns on the object that comes from GOOGLE VISION API'S result
	music=pygame.mixer.Sound(path)

        








        music=pygame.mixer.Sound('/home/pi/Desktop/sound/cello.wav')
        clock=pygame.time.Clock()
        music.play()
        time.sleep(10) #control how long the music will play










def Play_Youtube_Audio(path):


        
        textToSearch =path
	query = urllib.quote(textToSearch)
 	url = "https://www.youtube.com/results?search_query=" + query
 	response = urllib2.urlopen(url)
 	html = response.read()
 	soup = BeautifulSoup(html,'html.parser')
 	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
     		#print 'https://www.youtube.com' + vid['href']
     		music_link.append('https://www.youtube.com' + vid['href'])












def Play_Youtube_Audio1():


    #get the text
#    msg=path

#    song = urllib.urlencode({"search_query=" : msg})
#    print("song=",song)

    # fetch the ?v=query_string
#    result = urllib.urlopen("http://www.youtube.com/results?" + song)
#    print("result=",result)

    # make the url of the first result song
#    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', result.read().decode())
#    print("search_result=",search_results)

    #print(search_results)   



#    print("i=",i)





    # make the final url of song selects the very first result from youtube result
#    url = "http://www.youtube.com/watch?v="+search_results[0]
#    url2="http://www.youtube.com/watch?v="+search_results[i]



    i=random.randint(1,5)
    url=music_link[i]
    
   # chrome_path='/home/pi/Desktop/chromedriver'
   # webbrowser.get(chrome_path).open(url)
    webbrowser.open(url)
    sleep(30)


#using selenium
'''
    driver=webdriver.Chrome('/home/pi/Desktop/chromedriver')
    driver.get(url)
    sleep(30)
    driver.close()
'''

#PhantomJs

'''

    driver = webdriver.PhantomJs(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=ANY'])
    driver.get(url)
    sleep(30)
    driver.quit()

'''




'''
    video = pafy.new(url)
    best = video.getbest()
    playurl = best.url

    Instance = vlc.Instance()
    player = Instance.media_player_new()
    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
                             
    player.play()

'''




def append_for_sep(string):
        for_sep.append(string)
        
def main():

    print("")
    print("")
    start_time=time.time()
    print("Optimize Camera for Taking picture for 5 seconds")
    print("")
    print("")
    
    takephoto() #First take a picture


    #camera shutter sound
    pygame.init()
    pygame.mixer.init()
    s=pygame.mixer.Sound('/home/pi/Desktop/Camera Click.wav')
    s.play()
    time.sleep(3)
        



    print("Finish Taking Photo")


    start_time=time.time()

    """Run a label request on a single image"""
    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('vision', 'v1', credentials=credentials,
                              discoveryServiceUrl=DISCOVERY_URL)
    print("")
    print("")
#    print (time.time() -start_time,"seconds")


    photo_file='/home/pi/Desktop/camera/test1.jpg'

    with open(photo_file,'rb') as image:
        image_content = base64.b64encode(image.read())
        service_request = service.images().annotate(body={
            'requests': [{
                'image': {
                    'content': image_content.decode('UTF-8')
                },
                'features': [{
                    'type': 'LABEL_DETECTION',
                    'maxResults': 10
                }]
            }]
        })


        #Print most ikely result
 #       response = service_request.execute()
 #       label = response['responses'][0]['labelAnnotations'][0]['description']
 #       print('Found label: %s ' % (label))


        #Print the average RGB---takes 3min
#        find_avg_color()
 #       print (time.time() -start_time,"seconds")
        print("Finish Extracting Most Frequent Colour")

        
	tup=most_frequent_colour(img)
        #for i in range(0,len(tup[1])):
        #    ser.writelines(tup[1])

    #    print(tup)
    #    print(tup[0])
    #    print(tup[1])

     #   print(type(tup[1]))

     #   print(type(tup[1][0]))

        

        r=tup[1][0]
        g=tup[1][1]
        b=tup[1][2]
        print("r: ",r,"g: ",g,"b: ",b)

#        r_hex=hex(r)
#        g_hex=hex(g)
#        b_hex=hex(b)
        
        

        

        
        #send data to Arudoino
#        ser.writelines(r_hex)
#        ser.writelines(g_hex)
#        ser.writelines(b_hex)


     #   print(tup[1][0])
     #   print(tup[1][1])
     #   print(tup[1][2])
        
        
        #print all likely result for classification And ERROR-Handling
        response = service_request.execute()

        try:
            for i in range(0,10):
                label=response['responses'][0]['labelAnnotations'][i]['description']
                append_for_sep(label)
        except (ZeroDivisionError, IndexError) :
            pass

        
        
        print("")
        print("")
        #classification 
	path=classify()
#        print (time.time() -start_time,"seconds")

        print("Finish Photo Analyze")
        for i in range(0,len(for_sep)):
            print(for_sep[i])
        print("")
        print("")
        #play the sound according to classification
#        playsound()	
        print("Found proper Atmosphere Keyword")
        print("Sound in proper Atmospere=",path)
    


#       play proper audio according to youtube


        #Using Youtube
#	Play_Youtube_Audio(path)
#	Play_Youtube_Audio1()
        print(" ")
        print(" ")
        play_music()
#       playsound()
        print(" ")
        print(" ")
        print("URLS AFTER CRWALING YOUTUBE WITH PROPER ATMOSPHERE KEYWORD")


	for i in range(0,len(music_link)):
        	print(music_link[i])
#	print (time.time() -start_time,"seconds")

        return 0



    

if __name__ == '__main__':
   # parser = argparse.ArgumentParser()
   # parser.add_argument('image_file', help='The image you\'d like to label.')
   # args = parser.parse_args()
    main()

