# Alex Cross, June 2022
# Supervisor: Dr. James Robar, NSHA/Dalhousie University

import cv2 #OpenCV
import numpy as np # Numpy (numerical analysis)
from openpyxl import Workbook  # Excel library

PI = 3.15159265

wb = Workbook()
ws = wb.active
ws.title = 'Cardiac phantom'
ws.append(['Frame', 'X value (pixels)', 'Z value (pixels)', 'X value (mm)', 'Z value (mm)', 'Ellipse Height', 'Time'])

PIX_TO_MM_RATIO = 96.8 # Ratio of pixels -> millimeters without height 

#lower = np.array ([50,100,100]) #minimum HSV values for "red" 
#upper = np.array ([5, 255, 255]) #maximum HSV values for "red"
lower = np.array([100,100,0]) # Minimum HSV value for blue
upper = np.array([140,255,255]) # Maximum HSV value for blue

count = 0 # Frame Counter

cap = cv2.VideoCapture('June28.mp4') #Load video

length = cap.get(cv2.CAP_PROP_FRAME_COUNT) #Get total frame count of video
if(cap.isOpened() == False): #Check that video is working 
    print("ERROR!")  # If the video doesn't open, error mes

font = cv2.FONT_HERSHEY_SIMPLEX

# =============================================================================
#width = cap.get(3)
#height = cap.get(4)
# 
#print(width) # Width (of video frame)
#print(height) # Height (of video frame)
# print(length)  # Total number of video frames
# =============================================================================

# Function to rescale frames to a more manageable size
def rescale(frame, percent = 100):
    scale_percent = 40
    width = int(frame.shape[1] * scale_percent/100)
    height = int(frame.shape[0] * scale_percent/100)
    dim = (width, height)
    return cv2.resize(frame, dim) 

# Main loop for program
while True:
    
    # Read each frame individually from the video
    ret, img = cap.read()
    count+=1 
    if not ret:
        break # When the last frame of the video is reached, break out of program
   
    roi = img[120:1420, 0:1080] #Limit the area of interest (y1:y2, x1:x2)
    
    imgBlur = cv2.GaussianBlur(roi, (7, 7), 1) #Blur (reduction of noise)
    
    image = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV) # Convert from blue-green-red to hue-sat-val
    mask = cv2.inRange(image, lower, upper) # Mask all colours except for red
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find objects in the mask

    c = max(contours, key = cv2.contourArea) # Focus on the biggest contour (hopefully the center of the object)
    cv2.drawContours(mask, [c], -1, (255, 0, 255), 5) # Draw the biggest contour
    
    ellipse = cv2.fitEllipse(c) # Fit an ellipse to the largest contour
    cv2.ellipse(mask, ellipse, (255,0,255), 15)
    x,y = ellipse[0]
    print("Ellipse center: " + str(ellipse[0])) # Print the first array value (which is an x,y tuple of the center of the ellipse)
    
    minAxis, majAxis = ellipse[1] # (minor axis, major axis) is a tuple from the ellipse function
    rotAngle = ellipse[2] # Rotation angle is the 3rd spot in the output array from the ellipse function call
    
    # This loop converts angle from deg-> rad and thne computes the vertical corresponding distance using the major axis length.
    if rotAngle < 170:
        rotAngle_rad = rotAngle * PI/180
    else:
        rotAngle_rad = (180 - rotAngle)*PI/180
    actual_Height = majAxis * np.cos(rotAngle_rad)
    actual_Length = minAxis * np.cos(rotAngle_rad)
    
    print("Frame: " + str(count))                     # Debugging
    #print("Actual height" + str(actual_Height))     # Debugging
    #print("Maj axis:  " + str(majAxis))             # Debugging
    #print("Rotation angle: " + str(rotAngle))       # Debugging    
    
    cv2.circle(mask, (int(x), int(y)), 20, (0,255,255), -1) # Draw circle at the center of ellipse (and also the model)

    ws.append([count, x, y, x*PIX_TO_MM_RATIO/actual_Height, y*PIX_TO_MM_RATIO/actual_Height, actual_Height, count/30]) # Use the computed height of the ellipse and the x,y coordinates of the ellipse center to track motion
    cv2.putText(mask, "Frame: "  + str(count), (100, 100), font, 1, (255, 255, 255), 3)
    cv2.putText(mask, "Centroid coordinates (x,y): ( " + str(round(x,3)) + "," + str(round(y,3)) + ")", (100, 150), font, 1, (255, 255, 255), 3)
    img = rescale(roi,   percent = 80)
    image = rescale(image, percent = 80) # Re-sizing of image frames
    mask = rescale(mask, percent = 80)
        
    cv2.imshow("Original", img)  # Show original image compressed to region of interest
    cv2.imshow("HSV shift & Blurred", image) #Show HSV shifted image
    cv2.imshow("Masked & Tagged", mask) # Show masked image
   
    if cv2.waitKey(1) == ord('q'): 
        break


wb.save("Cardiac_phantom99.xlsx") # Save the excel spreadsheet 

# End of program, release capture and end all processes  

cap.release()
cv2.destroyAllWindows()
    
