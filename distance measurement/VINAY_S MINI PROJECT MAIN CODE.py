import cv2

# variables
# distance from camera to object measured
known_distance = 26
# width of face in the real world or object plane
known_width =14.3
# colors
Green = (0,255,0)
Red =  (0,0,255)
White = (255,255,255)
fonts =cv2.FONT_HERSHEY_COMPLEX
cap =cv2.VideoCapture(0)
# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
# focal length finder function
def FocalLength(measured_distance, real_width, width_in_rf_image):
    focal_length = (width_in_rf_image * measured_distance)/ real_width
    return focal_length
#distance estimation function
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    distance =(real_face_width * Focal_Length)/face_width_in_frame
    return distance
def face_data(image):
    face_width = 0
    gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image,1.3,5)
    for(x,y,h,w) in faces:
        cv2.rectangle(image, (x,y), (x+w,y+h), (255,0,0), 1)
        face_width = w

    return face_width

# reading reference image from directory
ref_image =cv2.imread("ref_img.png")

ref_image_face_width = face_data(ref_image)
Focal_length_found = FocalLength(known_distance, known_width, ref_image_face_width)
print (Focal_length_found)
cv2.imshow("ref_image",ref_image)

while True:
    _, frame = cap.read()

    # calling face_data function
    face_width_in_frame =face_data(frame)
    # finding the distance by calling function distance finder
    if face_width_in_frame !=0:
        Distance = Distance_finder(Focal_length_found, known_width, face_width_in_frame)
    # Drawing Text on the screen
        cv2.putText(frame, f"Distance ={Distance}", (50,50), fonts,0.6, (0,255,0),2)
    cv2.imshow("final display", frame)
    if cv2.waitKey(1) == ord("q"):
        break
cap.release()
cv2.destroyAllWindows() 