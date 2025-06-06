import datetime
import time
import tkinter as tk

import pandas as pd

ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Hour, Minute, Second = timeStamp.split(":")
d = {}
index = 0
def manually_fill():
    global sb
    sb = tk.Tk()
    sb.iconbitmap("AMS.ico")
    sb.title("Enter subject name...")
    sb.geometry("580x320")
    sb.configure(background="#1c1c1c")

    # noinspection PyGlobalUndefined
    def err_screen_for_subject():
        def ec_delete():
            ec.destroy()

        global ec
        ec = tk.Tk()
        ec.geometry("300x100")
        ec.iconbitmap("AMS.ico")
        ec.title("Warning!!")
        ec.configure(background="#1c1c1c")
        tk.Label(
            ec,
            text="Please enter subject name!!!",
            fg="yellow",
            bg="black",
            font=("times", 16, " bold "),
        ).pack()
        tk.Button(
            ec,
            text="OK",
            command=ec_delete,
            bd = 10,
            fg="Yellow",
            bg="#1c1c1c",
            width=9,
            height=1,
            activebackground="white",
            cursor="hand2",
            font=("times", 15, " bold "),
        ).place(x=90, y=50)

    def fill_attendance():

        ##Create table for Attendance
        global subb
        subb = SUB_ENTRY.get()

        if subb == "":
            err_screen_for_subject()
        else:
            sb.destroy()
            MFW = tk.Tk()
            MFW.iconbitmap("AMS.ico")
            MFW.title("Manually attendance of " + str(subb))
            MFW.geometry("880x470")
            MFW.configure(background="#1c1c1c")

            def del_errsc2():
                errsc2.destroy()

            def err_screen1():
                global errsc2
                errsc2 = tk.Tk()
                errsc2.geometry("330x100")
                errsc2.iconbitmap("AMS.ico")
                errsc2.title("Warning!!")
                errsc2.configure(background="#1c1c1c")
                tk.Label(
                    errsc2,
                    text="Please enter Student & Enrollment!!!",
                    fg="yellow",
                    bg="#1c1c1c",
                    font=("times", 16, " bold "),
                ).pack()
                tk.Button(
                    errsc2,
                    text="OK",
                    command=del_errsc2,
                    bd = 10,
                    fg="Yellow",
                    bg="#1c1c1c",
                    width=9,
                    height=1,
                    activebackground="white",
                    cursor="hand2",
                    font=("times", 15, " bold "),
                ).place(x=90, y=50)

            def testVal(inStr, acttyp):
                if acttyp == "1":  # insert
                    if not inStr.isdigit():
                        return False
                return True

            ENR = tk.Label(
                MFW,
                text="Enter Enrollment",
                bd = 10,
                width=15,
                height=2,
                fg="white",
                bg="#1c1c1c",
                font=("times", 15, " bold "),
            )
            ENR.place(x=30, y=100)

            STU_NAME = tk.Label(
                MFW,
                text="Enter Student name",
                bd = 10,
                width=15,
                height=2,
                fg="white",
                bg="#1c1c1c",
                font=("times", 15, " bold "),
            )
            STU_NAME.place(x=30, y=200)

            global ENR_ENTRY
            ENR_ENTRY = tk.Entry(
                MFW,
                width=20,
                validate="key",
                bg="#1c1c1c",
                fg="Yellow",
                font=("times", 23, " bold "),
            )
            ENR_ENTRY["validatecommand"] = (ENR_ENTRY.register(testVal), "%P", "%d")
            ENR_ENTRY.place(x=290, y=105)

            def remove_enr():
                ENR_ENTRY.delete(first=0, last=22)

            STUDENT_ENTRY = tk.Entry(
                MFW, width=20, bg="#1c1c1c", fg="Yellow", font=("times", 23, " bold ")
            )
            STUDENT_ENTRY.place(x=290, y=205)

            def remove_student():
                STUDENT_ENTRY.delete(first=0, last=22)

            ####get important variable

            def enter_data_DB():
                global index
                global d
                ENROLLMENT = ENR_ENTRY.get()
                STUDENT = STUDENT_ENTRY.get()
                if ENROLLMENT == "":
                    err_screen1()
                elif STUDENT == "":
                    err_screen1()
                else:
                    if index == 0:
                        d = {
                            index: {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}
                        }
                        index += 1
                        ENR_ENTRY.delete(0, "end")
                        STUDENT_ENTRY.delete(0, "end")
                    else:
                        d[index] = {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}
                        index += 1
                        ENR_ENTRY.delete(0, "end")
                        STUDENT_ENTRY.delete(0, "end")

                print(d)

            def create_csv():
                import os
                # Ensure the directory exists
                folder_path = "Attendance(Manually)"
                os.makedirs(folder_path, exist_ok=True)

                # Create DataFrame and save CSV
                df = pd.DataFrame(d).T
                csv_name = (
                        folder_path
                        + "/"
                        + subb
                        + "_"
                        + Date
                        + "_"
                        + Hour
                        + "-"
                        + Minute
                        + "-"
                        + Second
                        + ".csv"
                )
                df.to_csv(csv_name, index=False)
                O = "CSV created Successfully"
                Notifi.configure(
                    text=O,
                    bg="Green",
                    fg="white",
                    width=33,
                    font=("times", 19, "bold"),
                )
                Notifi.place(x=180, y=380)
                """import csv
                import tkinter

                root = tkinter.Tk()
                root.title("Attendance of " + subb)
                root.configure(background="snow")
                with open(csv_name, newline="") as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(
                                root,
                                width=13,
                                height=1,
                                fg="black",
                                font=("times", 13, " bold "),
                                bg="lawn green",
                                text=row,
                                relief=tkinter.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()"""

            Notifi = tk.Label(
                MFW,
                text="CSV created Successfully",
                bg="Green",
                fg="white",
                width=33,
                height=2,
                font=("times", 19, "bold"),
            )

            c1ear_enroll = tk.Button(
                MFW,
                text="Clear",
                command=remove_enr,
                bd = 10,
                fg="Yellow",
                bg="#1c1c1c",
                width=10,
                height=1,
                activebackground="yellow",
                cursor="hand2",
                font=("times", 15, " bold "),
            )
            c1ear_enroll.place(x=690, y=100)

            c1ear_student = tk.Button(
                MFW,
                text="Clear",
                command=remove_student,
                bd = 10,
                fg="Yellow",
                bg="#1c1c1c",
                width=10,
                height=1,
                activebackground="yellow",
                cursor = "hand2",
                font=("times", 15, " bold "),
            )
            c1ear_student.place(x=690, y=200)

            DATA_SUB = tk.Button(
                MFW,
                text="Enter Data",
                command=enter_data_DB,
                bd = 10,
                fg="yellow",
                bg="#1c1c1c",
                width=20,
                height=2,
                activebackground="white",
                cursor = "hand2",
                font=("times", 15, " bold "),
            )
            DATA_SUB.place(x=170, y=300)

            MAKE_CSV = tk.Button(
                MFW,
                text="Convert to CSV",
                command=create_csv,
                bd = 10,
                fg="yellow",
                bg="#1c1c1c",
                width=20,
                height=2,
                activebackground="White",
                cursor="hand2",
                font=("times", 15, " bold "),
            )
            MAKE_CSV.place(x=570, y=300)

            def attf():
                import subprocess

                subprocess.Popen(
                    r'explorer /select,"D:\Maske\MANE\Attendance-Management-system-using-face-recognition-master\Attendance(Manually)"'
                )

            attf = tk.Button(
                MFW,
                text="Check Sheets",
                command=attf,
                bd = 10,
                fg="Yellow",
                bg="#1c1c1c",
                width=12,
                height=1,
                activebackground="White",
                cursor="hand2",
                font=("times", 14, " bold "),
            )
            attf.place(x=730, y=410)

            MFW.mainloop()

    SUB = tk.Label(
        sb,
        text="Enter Subject",
        bd=10,
        width=15,
        height=2,
        fg="yellow",
        bg="#1c1c1c",
        font=("times", 15, " bold "),
    )
    SUB.place(x=30, y=100)

    global SUB_ENTRY

    global SUB_ENTRY
    SUB_ENTRY = tk.Entry(
        sb,
        width=20,
        bg="#1c1c1c",
        fg="yellow",
        font=("times", 23, " bold "),
        bd=4,
        relief=tk.GROOVE
    )
    SUB_ENTRY.place(x=250, y=105)

    fill_manual_attendance = tk.Button(
        sb,
        text="Fill Attendance",
        command=fill_attendance,
        bd = 10,
        fg="yellow",
        bg="#1c1c1c",
        width=20,
        height=2,
        activebackground="White",
        cursor="hand2",
        font=("times", 15, " bold "),
    )
    fill_manual_attendance.place(x=250, y=160)
    sb.mainloop()
