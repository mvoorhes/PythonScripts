'''
RVGmt.py

Generates and outputs a random youtube video url.
Uses multithreading to find a working url faster
Runs until user presses ctrl c or until it finds an actual youtube link

This code is kind of worthless for a few reasons
- While there are over 800 million videos, there are 73786976294838206464 possible combinations in base64
- With this knowledge, this algorithm has to search through over 92 billion links before it can find a good link
- It can find around 1200 links per minute, which means that it will take 77 million minutes to find a working link
- That's 1.2 million hours
- That's 53,576 days
- That's 146 years, to find 1 video, using multithreading

There are a few random video generators online that are able to get real videos with a much higher success rate. I wanna find those people and ask their secret lol
'''

from pytube import YouTube
import random
import string
import threading
import os
import time

global passwords
global complete
global t0

ID_LENGTH = 11
alphabet = string.ascii_letters + string.digits + '-' + '_'

def thread_task():
    global complete
    global passwords
    while (1):
        if complete == True:
            return
        link = "https://www.youtube.com/watch?v="
        id = ''.join(random.choices(alphabet, k=ID_LENGTH))
    
        t1 = time.time() - t0
        if t1 >= 60:
            complete = True
            continue
    
        passwords += 1
        link += id
        video = YouTube(link)
        
        try:
            video.check_availability()
            print("Link Success: ", link)
            complete = True
        except Exception:
            pass


if __name__ == '__main__':
    global complete
    global passwords
    complete = False
    passwords = 0
    
    num_threads = os.cpu_count()
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=thread_task)
        threads.append(thread)
        
    t0 = time.time()
    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()


    print("IDs = ", passwords)
    print("Done")
