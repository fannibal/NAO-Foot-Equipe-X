from machine_fini import *
import time
import sys
import math
import select
from naoqi import ALProxy
import motion 

#robotIp="localhost"
robotIp="172.20.28.198"
#robotPort=11212
robotPort=9559

graphe={'IDLE':{'wait':'IDLE','go':'START'},'START':{'wait':'START','rotation':'ROTATE','stooop!!':'IDLE'},'ROTATE':{'rotation':'ROTATE','cepe_party':'WALK','stooop!!':'IDLE'},'WALK':{'cepe_party':'WALK','stooop!!':'IDLE','rotation':'ROTATE'}}

deus_ex=machina(graphe)
def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def getKey():
    #tty.setcbreak(sys.stdin.fileno())
    c='s'
    cok=False
    if isData():
        c = sys.stdin.read(1)
        cok=True
    return cok,c

def demarrage():
	motionProxy.wakeUp()
	postureProxy.goToPosture("StandInit", 0.5)
	motionProxy.setWalkArmsEnabled(True, True)
	motionProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])
	print'Initialisation'
	return 'go'

def avance():
	motionProxy.moveTo (0.2, 0, 0)
	print'Avance'
	return 'cepe_party'

def gauche():
	motionProxy.moveTo (0, 0, math.pi/4)
	print 'gauche'
	return 'rotation'

def droite():
	motionProxy.moveTo (0, 0, -math.pi/4)
	print 'droite'
	return 'rotation'

def stop():
	motionProxy.rest()
	print'STOOOOOOOOOOOOOOOOOP!!'
	return 'stooop!!' 

assignation = {'E': demarrage, 'z' : avance , 'q': gauche,'d': droite, 's': stop}

deus_ex.cur_state='IDLE'

try:
    motionProxy = ALProxy("ALMotion", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALMotion"
    print "Error was: ", e

try:
    postureProxy = ALProxy("ALRobotPosture", robotIp, robotPort)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

print 'Zzz'
while 1:

	cok,touche = getKey()
	if (cok):
		if touche in assignation :
			deus_ex.cur_event=assignation[touche]()
		else:
			deus_ex.cur_event='wait'
		deus_ex.run()
		print ' '
    		time.sleep(0.1)
	
