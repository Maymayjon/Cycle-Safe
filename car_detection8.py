import cv2
from carlist8 import car_list
from carcoordinates8 import car_coord


# Min Area of car box size in pixels
box_size_threashold = 5000

# TODO Add descp
retire_age = 30 # 3 seconds assuming 24 frames per second
# hide_age = 10 # Stop show boxes



list_cars = car_list(retire_age=retire_age)

# Please uncomment each file below Car Image
#img_file = 'Car_Photo.jpg'
video = cv2.VideoCapture("output.avi")
#video = cv2.VideoCapture('Dashcam_Pedestrians.mp4')


# Our pre-trained car and pedestrian classifiers
car_tracker_file = 'cars.xml'
# pedestrian_tracker_file = 'haarcascade_fullbody.xml'

# create car classifier. classifier identifies the object: person, car, etc.
car_tracker = cv2.CascadeClassifier(car_tracker_file)
while True:

    # Read the one frame in the video. video.read() returns a tuple
    (read_succesful, frame) = video.read()
  #  frame = cv2.flip(frame, 1)

    height, width, channels = frame.shape


    if read_succesful:
        # Must convert to grayscale as a valid frame, otherwise will break loop
        grayscaled_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        break

    # detect cars AND Pedestrians in the image of any scale. Data for x and y
    cars = car_tracker.detectMultiScale(grayscaled_frame)

    # Draw rectangles around the cars pulled from x and y cordinates, height width to display color red
    list_cars.increment_frame()

    for (x, y, w, h) in cars:
        ## Draw Box on Cars
        #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        box_size = w * h
        if(box_size >= box_size_threashold):
            list_cars.add_car(x,y,w,h)
    # for c in list_cars.car_coordinate_list:
    #     print(c)

    list_cars.retire_coords()

    list_cars.draw_boxes(frame, font_size=1)

    list_cars.determine_increase(width)
    # if input("hit enter for next frame") == "2":
    #     list_cars.clear_coords()




    # Display the color image with the cars and faces spotted
    # When it converts to grayscale it will compute it faster
    cv2.imshow('Car_Detector', frame)

    # Dont autoclose (Wait here in the code and listen for a key to press)
    cv2.waitKey(1)

# Trouble tracking car when car is close to camera
