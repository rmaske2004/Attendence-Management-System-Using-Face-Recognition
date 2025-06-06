import csv
import os

import cv2



def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    if l1.strip() == "" and l2.strip() == "":
        t = 'Please enter your Enrollment Number and Name.'
        text_to_speech(t)
        err_screen()
        return
    elif l1.strip() == "":
        t = 'Please enter your Enrollment Number.'
        text_to_speech(t)
        err_screen()
        return
    elif l2.strip() == "":
        t = 'Please enter your Name.'
        text_to_speech(t)
        err_screen()
        return

    Enrollment = l1.strip()
    Name = l2.strip()
    sampleNum = 0
    directory = f"{Enrollment}_{Name}"
    path = os.path.join(trainimage_path, directory)

    try:
        if os.path.exists(path):
            msg = "Student already exists."
            message.configure(text=msg)
            text_to_speech(msg)
            return
        else:
            os.makedirs(path)

        cam = cv2.VideoCapture(1)

        if not cam.isOpened():
            msg = "Unable to access the camera. Check the IP webcam connection."
            message.configure(text=msg)
            text_to_speech(msg)
            err_screen()
            return

        detector = cv2.CascadeClassifier(haarcasecade_path)

        while True:
            ret, img = cam.read()
            if not ret:
                message.configure(text="Failed to grab frame from camera.")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                filename = f"{Name}_{Enrollment}_{sampleNum}.jpg"
                filepath = os.path.join(path, filename)
                cv2.imwrite(filepath, gray[y:y + h, x:x + w])
                cv2.imshow("Capturing Faces", img)

            if cv2.waitKey(1) & 0xFF == ord("q") or sampleNum >= 50:
                break

        if sampleNum > 0:
            row = [Enrollment, Name]
            with open("StudentDetails/studentdetails.csv", "a+", newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)

            res = f"Images Saved for ER No: {Enrollment}, Name: {Name}"
            message.configure(text=res)
            text_to_speech(res)
        else:
            message.configure(text="No face images captured.")
            text_to_speech("No face images captured.")

    except Exception as e:
        err_msg = f"Error: {str(e)}"
        message.configure(text=err_msg)
        text_to_speech(err_msg)
        err_screen()


    finally:

        if cam is not None and cam.isOpened():
            cam.release()

