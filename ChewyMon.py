#!/usr/bin/env python

import time
import sys
import RPi.GPIO as io 
import MySQLdb as sql
import logging as log

# Logging
log.basicConfig(filename='chewymon.log', level=log.DEBUG, format='%(asctime)s.%(msecs)d - %(levelname)s - %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

# setup input
io.setmode(io.BCM) 
wheel_pin = 23 
io.setup(wheel_pin, io.IN, pull_up_down=io.PUD_UP) # activate input with PullUp

# MySQL DB connection
DbUser = ""
DbPass = ""
DbName = ""

try:
   db = sql.connect("localhost", DbUser, DbPass, DbName)
   curs = db.cursor()
   log.info("Connected to database %s", DbName) 
except:
   log.error("Can't connect to database %s...exiting", DbName)
   sys.exit(0)

# Globals
wheel_circ = 33.772121026090275 #inches
lasttime = time.time()

# Return MPH given period of single wheel turn
def getSpeed(period):
   global wheel_circ
   speed = (wheel_circ*.0568181818)/period
   return speed

# Return RPM given period of single wheel turn
def getRPM(period):
   return round(60.0/period)

log.info('Waiting for rotations...')

try:
   while True:
      io.wait_for_edge(wheel_pin, io.RISING)
      runtime = time.time()
      log.debug('Rising edge detected - %s' % runtime)
      period = (runtime - lasttime)
      if (period > 4): 
         period = 0 # zero out speed and rpm between runs
         log.info('Period greater than 4 seconds, zeroing')
      sql = "INSERT INTO rundata(runtime,speed,rpm) VALUES(%s, %s, %s)" % (runtime, getSpeed(period), getRPM(period))
      log.debug(sql)
      curs.execute(sql)
      lasttime = runtime
      db.commit()
      io.wait_for_edge(wheel_pin, io.FALLING)
      log.debug('Falling edge detected - %s' % time.time())
except KeyboardInterrupt:
   io.cleanup()
