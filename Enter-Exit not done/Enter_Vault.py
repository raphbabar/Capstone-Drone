import logging
from time import sleep

#//////////////////////Vault entrance start//////////////////////
def Enter_Vault():
    
    logging.basicConfig( level=logging.DEBUG, format='%(asctime)s (%(threadName)-15s) %(message)s' )
    
    logging.debug('Vault entrance function started. The drone is ready to enter the vault')
    Entrance_centered = False
    Entrance_end = False
    drone_height = 2.0 # m

    logging.debug('Entrance_centered: %s', Entrance_centered)
    while not Entrance_centered:
        sleep(5)
        # locate the drone above the center of the entrance
        # if the center of entrance manhole circle is approximately on the center of the camera picture:
            #Entrance_centered = True
        Entrance_centered = True
        logging.debug('Entrance_centered: %s', Entrance_centered)
        
    logging.debug('Entrance_end: %s', Entrance_end)        
    while not Entrance_end:
        sleep(10)
        drone_height = 1.4
        # lower the drone to an approximate height of 1.5m above the ground
        if drone_height <= 1.5:
            Entrance_end = True
            logging.debug('Entrance_end: %s', Entrance_end)
            
    logging.debug('Vault entrance function ended. The drone is at the bottom of entrance manhole')
#//////////////////////Vault entrance ends//////////////////////