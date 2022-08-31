# Alex Cross, Department of Radiation Oncology, Dalhousie University/NSHA
# Supervised by Dr. James Robar

# Import of necessary libraries
import PySimpleGUI as sg 
from hexapod_stage import hexapod_controls
from thorlabs_stage import motor_0_movement, motor_1_movement, motor_2_movement
import threading
import time



def primary_controls():
    sg.theme('dark black 1')
    
    header_font = 'Helvetica 14 bold' 
    reg_font = 'Helvetica 10 bold'
    pad_right_col = 50
    pad_left_col = 40
    
    # Left column layout.  Each line corresponds to one line on the left side of the GUI.
    layout_l = [ [sg.Text("Heart Parameters (min, max)", font = header_font, pad = (0,40))],
              [sg.Text("X Translation (0 mm, 5 mm)", font = reg_font, pad = (pad_left_col,0))], [sg.Input('2.2', s=10, pad = (2*pad_left_col,0))],
              [sg.Text("Y Translation (0 mm, 5 mm)", font = reg_font, pad = (pad_left_col,0))], [sg.Input('1.7', s=10, pad = (2*pad_left_col,0))],
              [sg.Text("Z Translation (0 mm, 5 mm)", font = reg_font, pad = (pad_left_col,0))], [sg.Input('2.2', s=10, pad = (2*pad_left_col,0))],
              [sg.Button('Run', s = 10, size = (20,10), pad = (pad_left_col,40))]]
    
    # Right column layout.  Each line corresponds to one line on the right side the GUI.
    layout_r = [ [sg.Text("Lung Parameters (min, max)", font = header_font, pad = (17,0))],
              [sg.Text("X Translation (-6 mm, 6 mm)", font = reg_font, pad = (pad_right_col,0))], [sg.Input('-5.1', s = 10, pad = (pad_right_col,0))],
              [sg.Text("Y Translation (-6 mm, 6 mm)", font = reg_font, pad = (pad_right_col,0))], [sg.Input('-0.4', s=10, pad = (pad_right_col,0))],
              [sg.Text("Z Translation (-6 mm, 6 mm)", font = reg_font, pad = (pad_right_col,0))], [sg.Input('2.6', s=10, pad = (pad_right_col,0))],
              [sg.Text("Theta X (-5 deg, 5 deg)", font = reg_font, pad = (pad_right_col,0))], [sg.Input('-2', s=10, pad = (pad_right_col,0))],
              [sg.Text("Theta Y (-5 deg, 5 deg)", font = reg_font, pad = (pad_right_col,0))], [sg.Input('-3.6', s=10, pad = (pad_right_col,0))],
              [sg.Text("Theta Z (-5 deg, 5 deg)", font = reg_font, pad = (pad_right_col,0))], [sg.Input('-3.1', s=10, pad = (pad_right_col,(0,10)))],
              [sg.Text("RUN TIME (MINUTES)", font = header_font, pad = (17,0))], [sg.Input("1", s = 10, pad = (pad_right_col,(0,10)))],
              [ sg.Button('Quit', s = 10, size = (20,10))]]

              
    layout = [[sg.Col(layout_l,), sg.Col(layout_r)]] # The layout is comprised of the left column and the right column from above.
   
    window = sg.Window('Dynamic Cardiac Phantom Controls', layout, size = (600, 600), enable_close_attempted_event = True) # Populates the GUI frame, using the layout above to st
    
    while True:  # Main loop for the program; opens GUI and calls other functions.
    
        event, values = window.read() # Each input field is one entry in 'values' which are then assigned to variables.
        
        ## HEART PARAMETERS ##
        x_heart = values[0] # Heart X displacement parameter
        y_heart = values[1] # Heart Y displacement parameter
        z_heart = values[2] # Heart Z displacement parameter
        
        ## LUNG PARAMETERS ##
        x_lung = values[3] # Lung X displacement parameter
        y_lung = values[4] # Lung Y displacement parameter
        z_lung = values[5] # Lung Z displacement parameter
        u_lung = values[6] # Lung thetaX/U displacement parameter
        v_lung = values[7] # Lung thetaY/V displacement parameter
        w_lung = values[8] # Lung thetaZ/W displacement parameter
        minutes = values[9] # How many minutes to run for (default 1)
        
        # This next line makes a "confirmation" pop-up.
        if (event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT or event == 'Quit') and sg.popup_yes_no("Are you sure you want to quit?", font = 'Arial 14 bold') == 'Yes':
            print("Quit successfully!")
            window.close() # If you click Quit or the X at the top right, popup a confirmation and close the window/end program.
            break 
        
        # If you click Run, popup with a yes/no prompt to continue.  If you click yes, run the scripts.
        if (event == 'Run') and sg.popup_yes_no("Run in current state?", font = 'Arial 14 bold') == 'Yes':
            print("Running!")
            tx = threading.Thread(target = (motor_0_movement), args = (float(x_heart), float(minutes))) # Y direction (heart) thread
            ty = threading.Thread(target = (motor_1_movement), args = (float(y_heart), float(minutes))) # X direction (heart) thread
            tz = threading.Thread(target = (motor_2_movement), args = (float(z_heart), float(minutes))) # Z direction (heart) thread 
            t_Lung = threading.Thread(target = (hexapod_controls), args = (x_lung,y_lung,z_lung,u_lung,v_lung,w_lung,minutes)) # Hexapod thread
            
            print("Start!")
            start = time.time() # Start a timer
            
            # Initiate all threads
            tx.start()
            ty.start()
            tz.start()
            t_Lung.start()
            
            # Join all threads so that they terminate at the same time.
            tx.join()
            ty.join()
            tz.join()
            t_Lung.join()
            
            end = time.time() # End timer
            print(end-start)
            
            # Close window and exit the loop.
            window.close()
            break    
    
    ## Testing/Print of used values
    print("Heart values:|    X   |   Y   |  Z   |")
    print("             |", x_heart, "mm,", y_heart, "mm,", z_heart, "mm")
    print("------------------------------------------------")
    print("Lung values:|   X   |   Y   |  Z   |  U  |  V    |  W  |")
    print("            |",   x_lung, "mm,", y_lung, "mm,", z_lung, "mm,", u_lung, "deg,", v_lung, "deg,", w_lung, "deg")    
    print("Ran for ", minutes, "minute(s)", "percent deviation of", (100*(1 - 60*float(minutes)/(end-start)))) # Calculate % error (i.e, 3 mins vs 190 seconds is a 5.55% error)


# Structure for calling the main function (avoids syncing problems)

if __name__ == '__main__':
    primary_controls()