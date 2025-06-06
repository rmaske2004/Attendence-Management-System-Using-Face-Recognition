import datetime
import os
import time
import tkinter as tk
from tkinter import *
import cv2
import pandas as pd

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel\\Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails\\studentdetails.csv"
attendance_path = "Attendance"


def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        if sub.strip() == "":
            text_to_speech("Please enter the subject name!!!")
            return

        future = time.time() + 15  #for the camera capturing time adjust

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            try:
                recognizer.read(trainimagelabel_path)
            except:
                msg = "Model not found, please train model"
                Notifica.configure(text=msg, bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
                Notifica.place(x=20, y=250)
                text_to_speech(msg)
                return

            facecasCade = cv2.CascadeClassifier(haarcasecade_path)
            df = pd.read_csv(studentdetail_path)
            cam = cv2.VideoCapture(1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ["Enrollment", "Name", "Date", "Time"]
            attendance = pd.DataFrame(columns=col_names)

            while True:
                ret, im = cam.read()
                if not ret:
                    break
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = facecasCade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    if conf < 70:
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                        student_row = df[df["Enrollment"] == Id]

                        if not student_row.empty:
                            name = student_row.iloc[0]["Name"]
                            tt = f"{Id}-{name}"
                            attendance.loc[len(attendance)] = [Id, name, date, timeStamp]
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                            cv2.putText(im, tt, (x + h, y), font, 1, (255, 255, 0), 4)
                        else:
                            tt = "Unknown"
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 7)
                            cv2.putText(im, tt, (x + h, y), font, 1, (0, 0, 255), 4)
                    else:
                        tt = "Unknown"
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                        cv2.putText(im, tt, (x + h, y), font, 1, (0, 25, 255), 4)

                if time.time() > future:
                    break

                cv2.imshow("Filling Attendance...", im)
                if cv2.waitKey(30) & 0xFF == 27:
                    break

            cam.release()
            cv2.destroyAllWindows()

            if attendance.empty:
                text_to_speech("No faces recognized. Attendance not filled.")
                Notifica.configure(text="No faces recognized!", bg="black", fg="red", width=33, font=("times", 15, "bold"))
                Notifica.place(x=20, y=250)
                return

            attendance = attendance.drop_duplicates(["Enrollment"], keep="first")
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            Hour, Minute, Second = timeStamp.split(":")
            path = os.path.join(attendance_path, sub)
            os.makedirs(path, exist_ok=True)
            fileName = f"{path}/{sub}_{date}_{Hour}-{Minute}-{Second}.csv"
            attendance.to_csv(fileName, index=False)

            msg = f"Attendance Filled Successfully for {sub}"
            Notifica.configure(text=msg, bg="black", fg="yellow", width=33, relief=RIDGE, bd=5, font=("times", 15, "bold"))
            text_to_speech(msg)
            Notifica.place(x=20, y=250)

            # Display attendance CSV in Tkinter table
            import csv
            root = tk.Tk()
            root.title(f"Attendance of {sub}")
            root.configure(background="black")

            with open(fileName, newline="") as file:
                reader = csv.reader(file)
                for r, col in enumerate(reader):
                    for c, row in enumerate(col):
                        label = tk.Label(root, width=12, height=1, fg="yellow", font=("times", 15, "bold"),
                                         bg="black", text=row, relief=RIDGE)
                        label.grid(row=r, column=c)
            root.mainloop()

        except Exception as e:
            text_to_speech("No face found or error occurred.")
            print("Error:", e)
            cv2.destroyAllWindows()

    # Subject selection GUI
    subject = tk.Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    titl = tk.Label(subject, text="Enter the Subject Name", bg="black", fg="green", font=("arial", 25))
    titl.place(x=140, y=12)

    Notifica = tk.Label(subject, text="", bg="yellow", fg="black", width=33, height=2, font=("times", 15, "bold"))

    def Attf():
        sub = tx.get()
        if sub.strip() == "":
            text_to_speech("Please enter the subject name!!!")
        else:
            os.startfile(os.path.join(attendance_path, sub))

    attf = tk.Button(subject, text="Check Sheets", command=Attf, bd=7, font=("times new roman", 15),
                     bg="black", fg="yellow", height=2, width=10, relief=RIDGE,  cursor = "hand2",)
    attf.place(x=360, y=170)

    sub_lbl = tk.Label(subject, text="Enter Subject", width=10, height=2, bg="black", fg="yellow",
                       bd=5, relief=RIDGE, font=("times new roman", 15))
    sub_lbl.place(x=50, y=100)

    tx = tk.Entry(subject, width=15, bd=5, bg="black", fg="yellow", relief=RIDGE, font=("times", 30, "bold"))
    tx.place(x=190, y=100)

    fill_a = tk.Button(subject, text="Fill Attendance", command=FillAttendance, bd=7, font=("times new roman", 15),
                       bg="black", fg="yellow", height=2, width=12, relief=RIDGE,  cursor = "hand2",)
    fill_a.place(x=195, y=170)

    subject.mainloop()
