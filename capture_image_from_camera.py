import cv2
from cv2 import VideoCapture, imshow, imwrite

cam_port = 0
cam = VideoCapture(cam_port)
# reading the input using the camera

inp = input("Enter person name")
# If image will detected without any error,
# show result
while True:
    result, image = cam.read()
    imshow(inp, image)
    cv2.putText(image, "Press 'q' to capture image", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        imwrite(inp + ".jpg", image)
        print("image taken")
        break

# If captured image is corrupted, moving to else part
else:
    print("No image detected. Please! try again")
