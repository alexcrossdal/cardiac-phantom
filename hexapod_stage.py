# Alex Cross, Department of Radiation Oncology, Dalhousie University/NSHA
# Supervised by Dr. James Robar

# (c)2016 Physik Instrumente (PI) GmbH & Co. KG
# Software products that are provided by PI are subject to the
# General Software License Agreement of Physik Instrumente (PI) GmbH & Co. KG
# and may incorporate and/or make use of third-party software components.
# For more information, please read the General Software License Agreement
# and the Third Party Software Note linked below.
# General Software License Agreement:
# http://www.physikinstrumente.com/download/EULA_PhysikInstrumenteGmbH_Co_KG.pdf
# Third Party Software Note:
# http://www.physikinstrumente.com/download/TPSWNote_PhysikInstrumenteGmbH_Co_KG.pdf

# Import libraries
from pipython import GCSDevice
import time

# Function definition for the main function of this script (to run the Hexapod stage)
def hexapod_controls(x,y,z,u,v,w, minutes):
    """Connect to a PIPython device."""
    # We recommend to use GCSDevice as context manager with "with".

    with GCSDevice() as pidevice:
        # Choose the interface which is appropriate to your cabling.

        pidevice.ConnectTCPIP(ipaddress='169.254.8.0') # Use the ethernet port to connect to the Hexapod
        #pidevice.ConnectUSB(serialnum='116051530')
        # pidevice.ConnectRS232(comport=1, baudrate=115200)

        # Each PI controller supports the qIDN() command which returns an
        # identification string with a trailing line feed character which
        # we "strip" away.

        #print('connected: {}'.format(pidevice.qIDN().strip()))

        # Show the version info which is helpful for PI support when there
        # are any issues.

        #if pidevice.HasqVER():
            #print('version info: {}'.format(pidevice.qVER().strip()))

        #print('done - you may now continue with the simplemove.py example...')
        
        pidevice.VLS(20) # Set velocity for all directions to 20 mm/s (mechanical maximum speed)

        start = time.time() # Starting timer
        
        for i in range(1,int(15*float(minutes))): # Cycle through the "up and down" sinusoidal movement i times
            pidevice.MOV(['X','Y','Z','U','V','W'], [-1.3*float(x)/3.1,0.4*float(y)/1.6,4*float(z)/6,float(u),float(v),float(w)]) # Parameters from literature
            pidevice.DEL(2125)
            pidevice.MOV(['X','Y','Z','U','V','W'], [1.8*float(x)/3.1,2.0*float(y)/1.6,10*float(z)/6,0,0,0]) # Parameters from literature
            pidevice.DEL(2125)
        
        end = time.time() # Ending timer
        
        print("Total time: ", end-start)
        print("Time/cycle", (end-start)/16)
        
if __name__ == '__main__':
    # To see what is going on in the background you can remove the following
    # two hashtags. Then debug messages are shown. This can be helpful if
    # there are any issues.

    #from pipython import PILogger, DEBUG, INFO, WARNING, ERROR, CRITICAL
    #PILogger.setLevel(DEBUG)
    hexapod_controls()