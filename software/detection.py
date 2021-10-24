# Import packages
from tflite_runtime.interpreter import Interpreter
from threading import Thread
import cv2
import numpy as np
import gpiozero

#rover = gpiozero.Robot(left=(19, 26), right=(16, 20))

class VideoStream:
    # Camera object that controls video streaming from the Picamera

    def __init__(self, resolution=(640, 480), framerate=30):
        # Initialize the PiCamera and the camera image stream
        self.stream = cv2.VideoCapture(0)
        ret = self.stream.set(cv2.CAP_PROP_FOURCC,
                              cv2.VideoWriter_fourcc(*'MJPG'))
        ret = self.stream.set(3, resolution[0])
        ret = self.stream.set(4, resolution[1])

        # Read first frame from the stream
        (self.grabbed, self.frame) = self.stream.read()

        # Variable to control when the camera is stopped
        self.stopped = False

    def start(self):
        # Start the thread that reads frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # Keep looping indefinitely until the thread is stopped
        while True:
            # If the camera is stopped, stop the thread
            if self.stopped:
                # Close camera resources
                self.stream.release()
                return

            # Otherwise, grab the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # Return the most recent frame
        return self.frame

    def stop(self):
        # Indicate that the camera and thread should be stopped
        self.stopped = True


# Define and parse input arguments

min_conf_threshold = 0.5
imW, imH = 1360, 768

# Load the label map
with open("labelmap.txt", 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# Have to do a weird fix for label map if using the COCO "starter model" from
# https://www.tensorflow.org/lite/models/object_detection/overview
# First label is '???', which has to be removed.
if labels[0] == '???':
    del(labels[0])

# Load the Tensorflow Lite model.
interpreter = Interpreter(model_path="detect.tflite")

interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
height = input_details[0]['shape'][1]
width = input_details[0]['shape'][2]

floating_model = (input_details[0]['dtype'] == np.float32)

input_mean = 127.5
input_std = 127.5

# Initialize frame rate calculation
frame_rate_calc = 1
freq = cv2.getTickFrequency()

# Initialize video stream
videostream = VideoStream(resolution=(imW, imH), framerate=30).start()
# time.sleep(1)
turn = ""
move = ""

while True:

    print(f"turning: {turn}, moving: {move}          ", end="\r")
    # Start timer (for calculating frame rate)
    t1 = cv2.getTickCount()

    # Grab frame from video stream
    frame1 = videostream.read()

    # Acquire frame and resize to expected shape [1xHxWx3]
    frame = frame1.copy()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_resized = cv2.resize(frame_rgb, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)

    # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std

    # Perform the actual detection by running the model with the image as input
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Retrieve detection results
    # Bounding box coordinates of detected objects
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[
        0]  # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[
        0]  # Confidence of detected objects

    max_conf = 0
    human_detected = False
    for i in range(len(scores)):
        if ((scores[i] > min_conf_threshold) and (scores[i] <= 1.0) and (int(classes[i]) == 0) and (scores[i] > max_conf)):
            human_detected = True
            max_conf = scores[i]
            max_id = i

    if(not human_detected):
        #rover.stop()
        turn = "not detected"
        move = "not detected"
        #cv2.imshow('Object detector', frame)
        
    else:
        # Get bounding box coordinates and draw box
        # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
        ymin = int(max(1, (boxes[max_id][0] * imH)))
        xmin = int(max(1, (boxes[max_id][1] * imW)))
        ymax = int(min(imH, (boxes[max_id][2] * imH)))
        xmax = int(min(imW, (boxes[max_id][3] * imW)))
        xcenter = (xmin+xmax)/2
        ycenter = (ymin+ymax)/2

        """
        #---------- Draw Boxes (optional) ----------#
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (10, 255, 0), 2)
        # Draw label
        # Look up object name from "labels" array using class index
        object_name = labels[int(classes[max_id])]
        label = '%s: %d%%' % (object_name, int(
            scores[max_id]*100))  # Example: 'person: 72%'
        labelSize, baseLine = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)  # Get font size
        # Make sure not to draw label too close to top of window
        label_ymin = max(ymin, labelSize[1] + 10)
        # Draw white box to put label text in
        cv2.rectangle(frame, (xmin, label_ymin-labelSize[1]-10), (xmin +
                      labelSize[0], label_ymin+baseLine-10), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, label, (xmin, label_ymin-7),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)  # Draw label text
    
        # Draw framerate in corner of frame
        cv2.putText(frame, 'FPS: {0:.2f}'.format(frame_rate_calc), (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)
    
        # All the results have been drawn on the frame, so it's time to display it.
        cv2.imshow('Object detector', frame)
    
        # Calculate framerate
        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1
        """
        #---------- Move Robot ----------#
        if (xcenter > (imW / 2 + 100)):
            turn = "right"
            move = "override"
            #rover.right()
            continue

        elif (xcenter < (imW / 2 - 100)):
            turn = "left"
            move = "override"
            #rover.left()
            continue

        else:
            turn = "none"
            #rover.stop()

        if ((ymax-ymin) * (xmax-xmin) < (1360*768/3) - 50000):
            move = "forward"
            #rover.forward()
            continue

        elif ((ymax-ymin) * (xmax-xmin) > (1360*768/3) + 50000):
            move = "backward"
            #rover.backward()
            continue

        else:
            move = "none"
            #rover.stop()


    # Press 'q' to quit
    #if cv2.waitKey(1) == ord('q'):
    #
    #     break

# Clean up
#cv2.destroyAllWindows()
videostream.stop()
