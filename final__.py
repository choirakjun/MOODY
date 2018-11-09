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
import requests
import RPi.GPIO as GPIO
import time
import threading


GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.IN)
GPIO.setup(16,GPIO.IN)
GPIO.setup(23,GPIO.OUT)
GPIO.output(23,False)



global ps
ps = GPIO.input(18)#First ps would be 1
global path
global url_proj
sys.setdefaultencoding('utf-8')
#img=cv2.imread('/home/pi/Desktop/camera/test1.jpg')
img=Image.open('/home/pi/Desktop/camera/test1.jpg')
for_sep=[] #initiate list that saves the result from google vision api
music_link=[]
path=''
url_proj=''
clock=pygame.time.Clock()

#    start_time=time.time()

"""Run a label request on a single image"""
credentials = GoogleCredentials.get_application_default()
service = discovery.build('vision', 'v1', credentials=credentials,discoveryServiceUrl=DISCOVERY_URL)

ser1=serial.Serial("/dev/ttyUSB2",9600)
ser2=serial.Serial("/dev/ttyUSB3",9600)


print "Ready to play"

#path -> atmosphere
#url_proj-> which music to play

def project():
    
    global url_proj
   
    
    #lonely 7
    url1=['https://m.youtube.com/watch?v=64Yo1Rz2b40','https://www.youtube.com/watch?v=GquEnoqZAK0&list=PL42HRt_UQaqrKELp5f-kVGjdtvEkI9WUe','https://www.youtube.com/watch?v=gGgEOoCIhx0','https://www.youtube.com/watch?v=RgDKpgUI3To','https://www.youtube.com/watch?v=iGpuQ0ioPrM','https://www.youtube.com/watch?v=jiChpw0ul_8','https://www.youtube.com/watch?v=g0M4vkfCoWM']
    #healing 6
    url2=['https://www.youtube.com/watch?v=TElO0g_WRBM','https://www.youtube.com/watch?v=28ji6G5hTRw','https://www.youtube.com/watch?v=pGbIOC83-So','https://www.youtube.com/watch?v=1IkY0_qONRk&t=233s','https://youtu.be/21UTRsbDrm0','https://www.youtube.com/watch?v=Wimkqo8gDZ0']
    #happy 3
    url3=['https://m.youtube.com/watch?v=JWzBK87t19U','https://www.youtube.com/watch?v=fVCegBWf-70&list=PLA6E79A3DF4C79414&index=10','https://www.youtube.com/watch?v=R5jIoLnL_nE']
    #entertain 7
    url4=['https://m.youtube.com/watch?v=4JfIe5H6ETo','https://www.youtube.com/watch?v=JX19TZp8gDQ','https://www.youtube.com/watch?v=DybzsIQUOtg','https://youtu.be/EPbI_m00Lfc','https://youtu.be/Uw0PZSQ1ZjM','https://youtu.be/uDpojAGsthw','https://m.youtube.com/watch?v=cElhIDdGz7M']
    #romance 4
    url5=['https://m.youtube.com/watch?v=dzafS2LSmzk','https://www.youtube.com/watch?v=fVCegBWf-70&list=PLA6E79A3DF4C79414&index=10','https://www.youtube.com/watch?v=gieULzynY84','https://m.youtube.com/watch?v=1IkY0_qONRk']
    #classic 3
    url6=['https://m.youtube.com/watch?v=X6dJEAs0-Gk','https://m.youtube.com/watch?v=3xHeW-Vxyeg','https://www.youtube.com/watch?v=fVCegBWf-70&list=PLA6E79A3DF4C79414&index=10']


    #Determine which youyube url to projector  

    if path=="Lonely sound":
        i=random.randint(0,6)
        url_youtube='video='+str(url1[i])
        url_proj+=('&'+url_youtube)
    elif path=="edm, entertain sound bgm":
        i=random.randint(0,6)
        url_youtube='video='+str(url4[i]) 
        url_proj+=('&'+url_youtube)
    elif path=="Romance sound":
        i=random.randint(0,3)
        url_youtube='video='+str(url5[i])
        url_proj+=('&'+url_youtube)
    elif path=="Happy sound":
        i=random.randint(0,2)
        url_youtube='video='+str(url3[i])
        url_proj+=('&'+url_youtube)
    elif path=="Healing Sound":
        i=random.randint(0,5)
        url_youtube='video='+str(url2[i])
        url_proj+=('&'+url_youtube)
    else:
        i=random.randint(0,2)
        url_youtube='video='+str(url6[i])
        url_proj+=('&'+url_youtube)

    requests.get(url_proj)
    time.sleep(120) #control how long the music will play
    requests.get('http://dev.jiam.kr:7444/team1/set?audio=null&video=null')

    

def sound_():
    
    music.play()
    clock=pygame.time.Clock()



    print("")
    print("AFTER SEND PROJECT, MUSIC IN MOODY")
    
    time.sleep(20) #control how long the music will play
    music.stop()
    requests.get('http://dev.jiam.kr:7444/team1/set?audio=null&video=null')


    
    


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
     #camera initiate

    camera = picamera.PiCamera()
    picamera.PiCamera.CAPTURE_TIMEOUT=10

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
    atmos5=['leaf','nature','sky','ocean','bird','dog like mammal','puppy','infant','child','toddler']
      
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

    global music
    global url_proj
    pygame.init()
    pygame.mixer.init()
    
    
    if path=="Lonely sound":
        i=random.randint(1,11)
        print("i=",i)
        url='/home/pi/Desktop/sound/lonely/lonely'+str(i)+'.wav'
        url_proj='http://dev.jiam.kr:7444/team1/set?audio=lonely'+str(i)+'.mp3'
        music=pygame.mixer.Sound(url)

    elif path=="edm, entertain sound bgm":
        i=random.randint(1,8)
        print("i=",i)
        url='/home/pi/Desktop/sound/entertain/'+str(i)+'.wav'
        url_proj='http://dev.jiam.kr:7444/team1/set?audio=edm'+str(i)+'.mp3'
        music=pygame.mixer.Sound(url)

    elif path=="Romance sound":
        i=random.randint(1,12)
        print("i=",i)
        url='/home/pi/Desktop/sound/romantic/romance'+str(i)+'.wav'
        url_proj='http://dev.jiam.kr:7444/team1/set?audio=romance'+str(i)+'.mp3'
        music=pygame.mixer.Sound(url)

    elif path=="Happy sound":
        i=random.randint(1,7)
        print("i=",i)
        url='/home/pi/Desktop/sound/happy/'+str(i)+'.wav'
        url_proj='http://dev.jiam.kr:7444/team1/set?audio=happy'+str(i)+'.mp3'
        music=pygame.mixer.Sound(url)

    elif path=="Healing Sound":
        i=random.randint(1,4)
        print("i=",i)
        url='/home/pi/Desktop/sound/healing/'+str(i)+'.wav'
        url_proj='http://dev.jiam.kr:7444/team1/set?audio=healing'+str(i)+'.mp3'
        music=pygame.mixer.Sound(url)
  
    else:
        i=random.randint(1,7)
        print("i=",i)
        url='/home/pi/Desktop/sound/classic/'+str(i)+'.wav'
        url_proj='http://dev.jiam.kr:7444/team1/set?audio=classisc'+str(i)+'.mp3'
        music=pygame.mixer.Sound(url)
 
 '''   

def playsound():
        pygame.init()
        pygame.mixer.init()
        
        #depedns on the object that comes from GOOGLE VISION API'S result
	music=pygame.mixer.Sound(path)

        








        music=pygame.mixer.Sound('/home/pi/Desktop/sound/cello.wav')
        clock=pygame.time.Clock()
        music.play()
        time.sleep(10) #control how long the music will play

        

'''


def result_to_arduino():

    global result
    global path
    
    if path=="Lonely sound":
        result='a'
 
    elif path=="edm, entertain sound bgm":
        result='b'

    
    elif path=="Romance sound":
        result='c'
        
    elif path=="Happy sound":
        result='d'
        
    elif path=="Healing Sound":
        result='e'
    else:
        result='f'
    
    
    ser1.writelines('abcdefabcdef')
    ser2.writelines('abcdefabcdef')
    
'''

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

'''
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

def code():
 

    start_time=time.time()
    global path
    global for_sep
    global music_link
    global ps
    global t
    if (ps!=0) :
            
            for_sep=[] #initiate list that saves the result from google vision api
            music_link=[]
            if ps==0:
                raise ValueError
            
            print("Start Code")
            
            print("")
            print("")
        #    start_time=time.time()
            print("Optimize Camera for Taking picture for 5 seconds")
            print("")
            print("")
            
            takephoto() #First take a picture
            if ps==0:
                raise ValueError
            
            
            print("Finish Capture")
            print("")
            print("")
            requests.get('http://dev.jiam.kr:7444/team1/set?audio=Camera_Click.wav')    

            #camera shutter sound

            
            #pygame.init()
            #pygame.mixer.init()
            #s=pygame.mixer.Sound('/home/pi/Desktop/Camera Click.wav')
            #s.play()
            #time.sleep(2)
            

            print("")
            print("")
        #    print (time.time() -start_time,"seconds")

            print("Send the Data to Google vision api")
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
                if ps==0:
                    raise ValueError
            if ps==0:
                    raise ValueError
                                
            print("")
            print("")
            print("Receive Data from Google vision api")
            print("test0")
                #Print most ikely result
         #       response = service_request.execute()
         #       label = response['responses'][0]['labelAnnotations'][0]['description']
         #       print('Found label: %s ' % (label))


                #Print the average RGB---takes 3min
        #        find_avg_color()
         #       print (time.time() -start_time,"seconds")
        #        print("Finish Extracting Most Frequent Colour")

                
        #	tup=most_frequent_colour(img)
                #for i in range(0,len(tup[1])):
                #    ser.writelines(tup[1])

            #    print(tup)
            #    print(tup[0])
            #    print(tup[1])

             #   print(type(tup[1]))

             #   print(type(tup[1][0]))

                
                
         #       r=tup[1][0]
          #      g=tup[1][1]
           #     b=tup[1][2]
            #    print("r: ",r,"g: ",g,"b: ",b)

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
                
            print("test1")
                #print all likely result for classification And ERROR-Handling
            response = service_request.execute()
            print("test2")
            try:
                for i in range(0,10):
                    label=response['responses'][0]['labelAnnotations'][i]['description']
                    append_for_sep(label)
            except (ZeroDivisionError, IndexError) :
                pass
            if ps==0:
                raise ValueError

        #        print("")
        #        print("")


            print("")
            print("")
              
                #classification for atmosphere
                
                
            path=classify()
        #        print (time.time() -start_time,"seconds")
            print("Finish Photo Analyze")

            GPIO.output(23,True)
            time.sleep(1)
            GPIO.output(23,False)
                
            for i in range(0,len(for_sep)):
                print(for_sep[i])
            print("")
            if ps==0:
                raise ValueError
            print("")
                #play the sound according to classification
        #       playsound()	



            result_to_arduino()
            GPIO.output(23,True)
            time.sleep(1)
            GPIO.output(23,False)
            GPIO.output(23,True)
            time.sleep(1)
            GPIO.output(23,False)
                
            print("Sound in proper Atmospere=",path)
            print("")
            print("")
            print("Finish Send data to projector")
            print("")
            print("")
            print("Start Music")
            print (time.time() -start_time,"seconds")
                
            play_music()
            if ps==0:
                raise ValueError
            GPIO.output(23,True)
            time.sleep(1)
            GPIO.output(23,False)
            GPIO.output(23,True)
            time.sleep(1)
            GPIO.output(23,False)
            GPIO.output(23,True)
            time.sleep(1)
            GPIO.output(23,False)
            project()
            GPIO.output(23,True)
            time.sleep(1)
            GPIO.output(23,False)
            GPIO.output(23,True)
            time.sleep(1)
            GPIO.output(23,False)
            GPIO.output(23,True)
            time.sleep(1)
            GPIO.output(23,False)
            GPIO.output(23,True)
            time.sleep(1)
            GPIO.output(23,False)
            ps=0
            if ps==0:
                print("break")
                raise ValueError
                
                
            print("")
            print("")
          

            print("Sent to projector")
            print("")
          #      time.sleep(30)
            print("")
            print("")
            if ps==0:
                raise ValueError

            raise ValueError
            print("finish")



'''
         #play proper audio according to youtube
        #Using Youtube And play the proper music.


        #	Play_Youtube_Audio(path)
        #	Play_Youtube_Audio1()
'''

        #
         #       print(" ")
          #      print(" ")


                #play proper music.for 10 seconds
                
        #       playsound()
          #      print(" ")
           #     print(" ")
            #    print("URLS AFTER CRWALING YOUTUBE WITH PROPER ATMOSPHERE KEYWORD")


        #print urls from youtube
'''
                for i in range(0,len(music_link)):
                        print(music_link[i])
        #	print (time.time() -start_time,"seconds")

'''
        #        return 0


            


def append_for_sep(string):
        for_sep.append(string)


def callback_routine(channel):
    global ps
    
    try:
        code()
    except:
        print("Error detected")
        ps=1

    


def callback_routine_stop(channel):
    global ps
    ps=0
    #request proper youtube image with proper image atmosphere
    #requests.get('**********')
    ser1.writelines('f')
    ser2.writelines('f')
    ps=1
    

print("Wait for EVENT_HANDLER") 

 
GPIO.add_event_detect(16,GPIO.FALLING,callback=callback_routine_stop)
GPIO.add_event_detect(18,GPIO.FALLING,callback=callback_routine)

def main():
    try:
        while True:
            time.sleep(1)

    finally:
            finally:
        GPIO.cleanup()

    '''
    try:
        while True:

            if GPIO.input(18)==0:#if input comes
                code()

            else:
                print "push the botton"
            time.sleep(1)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()

    


    
    while True:
        time.sleep(2)

             
        try:
            print("code start")
            GPIO.wait_for_edge(16, GPIO.RISING)
            print("Falling edge detected. Here endeth the second lesson.")

        except KeyboardInterrupt:
            GPIO.cleanup()       # clean up GPIO on CTRL+C exi
    

    try:
        while True:
                        
            while True:
                if GPIO.input(18)==0:#if input comes
                    code()
            else:
                print "push the botton"
            
            
    except KeyboardInterrupt:
        GPIO.cleanup()
    '''
    
        
        
if __name__ == '__main__':
   # parser = argparse.ArgumentParser()
   # parser.add_argument('image_file', help='The image you\'d like to label.')
   # args = parser.parse_args()

    main()

