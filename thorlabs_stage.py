# Alex Cross, Department of Radiation Oncology, Dalhousie University/NSHA
# Supervised by Dr. James Robar

# Import libraries
import thorlabs_apt as apt
import time
import threading

 # Pull list of connected devices from APT and put into array of tuples of the form (channel, serial#)
data_list = apt.list_available_devices()

 # Pull (channel, serial) from each tuple in the array and save each serial # to a variable
chann1, serial_0 = data_list[0]
chann2, serial_1 = data_list[1]
chann3, serial_2 = data_list[2]

 # Define the three motors based off the serial numbers 
motor_0 = apt.Motor(serial_0)
motor_1 = apt.Motor(serial_1)
motor_2 = apt.Motor(serial_2)

 ## Set the velocity parameters for each motor individually (min veloc, max veloc, accel)
motor_0.set_velocity_parameters(0, 50, 50)  # X motor
motor_1.set_velocity_parameters(0, 50, 50)  # Y motor
motor_2.set_velocity_parameters(0, 50, 50)  # Z motor

 # Variables for sleep time (time between each movement)
sleep_time = 0.49
motor_0_sleep = sleep_time # X
motor_1_sleep = sleep_time # Y
motor_2_sleep = sleep_time # Z
#motor_3_sleep = xyz_delay


# One function to control each motor
def motor_0_movement(distance0, minute_multiplier): # X movement
    x = int(60*minute_multiplier) # Number of cycles for X heart motion
    for i in range(1, x+1):
        motor_0.move_by(1*distance0)
        time.sleep(motor_0_sleep)
        motor_0.move_by(-1*distance0)
        time.sleep(motor_0_sleep)
        
def motor_1_movement(distance1, minute_multiplier): # Y movement
    y = int(60*minute_multiplier) # Number of cycles for Y heart motion
    for i in range(1,y+1):
        motor_1.move_by(distance1)
        time.sleep(motor_1_sleep)
        motor_1.move_by(-1*distance1)
        time.sleep(motor_1_sleep)
 
def motor_2_movement(distance2, minute_multiplier): # Z movement
    z = int(60*minute_multiplier) # Number of cycles for Z heart motion
    for i in range (1, z + 1):
        motor_2.move_by(-1*distance2)
        time.sleep(motor_2_sleep)
        print("1", "maxima number", i) # This is when the LINAC beam should turn "ON".
        motor_2.move_by(distance2)
        print("0") # Shut off LINAC beam.
        time.sleep(motor_2_sleep)

 # def motor_3_movement(distance3): # X movement
 #     x = 10 # Number of cycles for x movement
 #     for i in range (1, x +1):
 #         motor_3.move_by(distance3)
 #         time.sleep(motor_3_sleep)
 #         motor_3.move_by(-1*distance3)
 #         time.sleep(motor_3_sleep)


# This block is only for if this program is ran independent of the lung motion and GUI. Otherwise, this block isn't used.
if __name__ == '__main__':
     t0 = threading.Thread(target = motor_0_movement, args = (motor_0_dist,)) # X movement
     t1 = threading.Thread(target = motor_1_movement, args = (motor_1_dist,)) # Y movement
     t2 = threading.Thread(target = motor_2_movement, args = (motor_2_dist,)) # Z movement
      
     start = time.time()
     t0.start()
     t1.start()
     t2.start()
    
     t0.join()
     t1.join()
     t2.join()
    
     end = time.time()
     print("All done! in ", end-start, "seconds")
     print("Time per cycle: ", (end-start)/60, "seconds")
     
