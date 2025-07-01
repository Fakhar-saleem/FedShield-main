import os
import time
import cv2

def verification(txt):
    # Open a connection to the webcam (you can change the index if you have multiple webcams)
    cap = cv2.VideoCapture(0)
    # Set the size of the popped-up window
    cv2.namedWindow("Live Webcam", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Live Webcam", 1280, 720)  # Adjust dimensions as needed

    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        # Create a copy of the original frame for capturing without rectangle
        frame_without_rectangle = frame.copy()

        # Draw a box with given specifications
        distance = 1.32  # Example distance in units
        coordinates = (277, 211, 428, 361)  # Example coordinates (x, y, x+w, y+h)

        # Draw the box on the frame
        cv2.rectangle(frame, (coordinates[0], coordinates[1]), (coordinates[2], coordinates[3]), (0, 255, 0), 2)

        # Display distance and coordinates on the frame
        text = f"Distance: {distance:.2f} units | Coordinates: {coordinates}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow("Live Webcam", frame)

        # Check for key presses
        key = cv2.waitKey(1) & 0xFF


        # Capture and save the image without rectangle when 'c' key is pressed
        if key == ord('c'):
            if not os.path.exists("captured_images"):
                os.makedirs("captured_images")
            files = os.listdir("captured_images")
            total_files = len(files)
            # Save the frame without rectangle as an image
            resized_frame = cv2.resize(frame_without_rectangle, (1280, 720))
            cv2.imwrite(f'captured_images\\{txt}.jpg', resized_frame)
            print("Image captured and saved!")
            cap.release()
            cv2.destroyAllWindows()
            return
        # Break the loop if 'Esc' is pressed
        elif key == 27:  # 27 corresponds to the ASCII value of the 'Esc' key
            break

    cap.release()
    cv2.destroyAllWindows()