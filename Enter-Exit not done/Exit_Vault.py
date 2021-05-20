import logging
from time import sleep

#//////////////////////Vault exit start//////////////////////
def Exit_Vault():
    
    logging.basicConfig( level=logging.DEBUG, format='%(asctime)s (%(threadName)-15s) %(message)s' )
    
    print('')
    logging.debug('Vault exit function started. The drone is moving to the marker at the bottom of exit manhole')
    Floor_marker_centered = False
    Exit_end = False

    logging.debug('Floor_marker_centered: %s', Floor_marker_centered)
    while not Floor_marker_centered:
        sleep(10)
        # locate the drone above the center of the exit floor marker
        # if the center of exit floor marker is approximately on the center of the camera picture:
            #Floor_marker_centered = True
        Floor_marker_centered = True
        logging.debug('Floor_marker_centered: %s', Floor_marker_centered)
            
    logging.debug('Exit_end: %s', Exit_end)
    while not Exit_end:
        sleep(5)
        # rise the drone until it detects a manhole circle. This means the drone is above the ground
        # then operator switch the drone to manual mode and land it
        # if  drone detects a manhole while it is rising:
            # the exit procedure is done
            #Exit_end = True
        Exit_end = True
        logging.debug('Exit_end: %s', Exit_end)
    
    logging.debug('Vault exit function ended. The drone is above the exit manhole. Operator can land it manually')
#//////////////////////Vault exit ends//////////////////////