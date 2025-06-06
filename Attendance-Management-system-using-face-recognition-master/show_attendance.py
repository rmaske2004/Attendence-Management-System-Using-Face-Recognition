import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *



def subjectchoose(text_to_speech):
    # noinspection PyTypeChecker
    def calculate_attendance():
        Subject = tx.get().strip()
        if not Subject:
            text_to_speech("Please enter the subject name.")
            return

        # Get all attendance CSVs for the subject
        filenames = glob(f"Attendance\\{Subject}\\{Subject}*.csv")
        if not filenames:
            text_to_speech("No attendance files found for this subject.")
            return

        df_list = []
        for file in filenames:
            try:
                df = pd.read_csv(file)
                if "Date" not in df.columns or "Enrollment" not in df.columns or "Name" not in df.columns:
                    print(f"File {file} is missing required columns.")
                    continue
                df["Date"] = df["Date"].astype(str).str.strip()
                df_list.append(df)
            except Exception as e:
                print(f"Error reading file {file}: {e}")

        if not df_list:
            text_to_speech("No valid attendance data found.")
            return

        # Combine all attendance records
        full_df = pd.concat(df_list , ignore_index = True)

        # Drop duplicates for the same student on the same day
        full_df.drop_duplicates(subset = ["Enrollment" , "Date"] , inplace = True)

        # Count unique dates to determine total classes held
        total_classes = full_df["Date"].nunique()

        if total_classes == 0:
            text_to_speech("No valid class dates found.")
            return

        # Group by student and count their attendance
        attendance_count = full_df.groupby(["Enrollment" , "Name"]).agg(
            Presents = ("Date" , "count") ,
            Dates_Present = ("Date" , lambda x: ', '.join(sorted(set(x))))
        ).reset_index()

        # Calculate attendance percentage
        attendance_count["Total Classes"] = 40
        attendance_count["Attendance"] = (
                                                 (attendance_count["Presents"] / 40) * 100
                                         ).round(2).astype(str)+"%"

        # Save the report
        attendance_file = f"Attendance\\{Subject}\\attendance.csv"
        attendance_count.to_csv(attendance_file , index = False)

        # Show the report in a GUI
        root = tkinter.Tk()
        root.title(f"Attendance of {Subject}")
        root.configure(background = "black")

        with open(attendance_file , newline = '' , encoding = 'utf-8') as file:
            reader = csv.reader(file)
            for r , row in enumerate(reader):
                for c , cell in enumerate(row):
                    label = tkinter.Label(
                        root ,
                        width = 20 ,
                        height = 2 ,
                        fg = "yellow" ,
                        font = ("times" , 12 , "bold") ,
                        bg = "black" ,
                        text = cell ,
                        relief = tkinter.RIDGE ,
                        anchor = "w" ,
                        justify = LEFT ,
                        wraplength = 200
                    )
                    label.grid(row = r , column = c , padx = 1 , pady = 1)
        root.mainloop()

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0 , 0)
    subject.configure(background = "black")

    titl = tk.Label(subject , bg = "black" , relief = RIDGE , bd = 10 , font = ("arial" , 30))
    titl.pack(fill = X)
    titl = tk.Label(
        subject ,
        text = "Which Subject of Attendance?" ,
        bg = "black" ,
        fg = "green" ,
        font = ("arial" , 25) ,
    )
    titl.place(x = 70 , y = 12)


    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(f"Attendance\\{sub}")

    attf = tk.Button(
        subject ,
        text = "Check Sheets" ,
        command = Attf ,
        bd = 7 ,
        font = ("times new roman" , 15) ,
        bg = "black" ,
        fg = "yellow" ,
        height = 2 ,
        width = 10 ,
        relief = RIDGE ,
        cursor="hand2",
    )
    attf.place(x = 360 , y = 170)

    sub = tk.Label(
        subject ,
        text = "Enter Subject" ,
        width = 10 ,
        height = 2 ,
        bg = "black" ,
        fg = "yellow" ,
        bd = 5 ,
        relief = RIDGE ,
        font = ("times new roman" , 15) ,
    )
    sub.place(x = 50 , y = 100)

    tx = tk.Entry(
        subject ,
        width = 15 ,
        bd = 5 ,
        bg = "black" ,
        fg = "yellow" ,
        relief = RIDGE ,
        font = ("times" , 30 , "bold") ,
    )
    tx.place(x = 190 , y = 100)

    fill_a = tk.Button(
        subject ,
        text = "View Attendance" ,
        command = calculate_attendance ,
        bd = 7 ,
        font = ("times new roman" , 15) ,
        bg = "black" ,
        fg = "yellow" ,
        height = 2 ,
        width = 12 ,
        relief = RIDGE ,
        cursor="hand2",
    )
    fill_a.place(x = 195 , y = 170)

    subject.mainloop()