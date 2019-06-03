#!/usr/bin/python

import threading
import time
import sys
from Queue import Queue

exitFlag = 0
global boom 
boom = {}
boom[1] = 'one'
boom[2] = 'two'

class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
        #self.counter = counter
    def run(self):
        print "Starting " + self.name
        #print_time(self.name, self.counter, 5)
        self.smthn('some')
        print self.prop
        print "Exiting " + self.name
        
    def smthn(self,val):
        self.prop = val+" "+self.name
        
def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print "%s: %s" % (threadName, time.ctime(time.time()))
        counter -= 1


main_q = Queue(maxsize=0)
# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()




print "Exiting Main Thread"