import os
import tkinter as tk
from tkinter import *
import pyttsx3
from PIL import ImageTk , Image
import automaticAttedance
from takemanually import manually_fill
import show_attendance
import trainImage


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = (
    "./TrainingImageLabel/Trainner.yml"
)
trainimage_path = "/TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = (
    "./StudentDetails/studentdetails.csv"
)
attendance_path = "Attendance"

window = Tk()
window.title("Face Recognition Based Attendance System.    Developed By Rohit & Kishor ")
window.geometry("1280x720")
dialog_title = "QUIT"
dialog_text = "Are you sure want to close?"
bg_image = Image.open("UI_Image/unnamed.jpg")
bg_image = bg_image.resize((1550, 850), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
# noinspection PyTypeChecker
bg_label = Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)




def del_sc1():
    sc1.destroy()



def err_screen():

    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.iconbitmap("AMS.ico")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")

    sc1.resizable(0,0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",
        font=("Verdana", 16, "bold"),
    ).pack()
    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#1c1c1c",
        width=9,
        height=1,
        activebackground="Yellow",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)

def testVal(inStr, acttyp):
    if acttyp == "1":
        if not inStr.isdigit():
            return False
    return True


logo = Image.open("UI_Image/0001.png")
logo = logo.resize((50, 47), Image.Resampling.LANCZOS)
logo1 = ImageTk.PhotoImage(logo)

titl = tk.Label(window, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))

titl.pack(fill=X)

l1 = tk.Label(window,image=logo1, bg="#1c1c1c",)
l1.place(x=180, y=10)


titl = tk.Label(
    window, text="M.B.E.S COLLEGE OF ENGINEERING,AMBAJOGAI.", bg="#1c1c1c", fg="yellow", font=("Verdana", 26, "bold"),
)
titl.place(x=250, y=12)

a = tk.Label(
    window,
    text="Welcome to Attendance System",
    bg="#1c1c1c",
    fg="yellow",
    bd=10,
    font=("Verdana", 30, "bold"),
)
a.place(x=330, y=130)


ri = Image.open("UI_Image/register.png")
r = ImageTk.PhotoImage(ri)
# noinspection PyTypeChecker
label1 = Label(window, image=r)
label1.image = r
label1.place(x=55, y=270)

ai = Image.open("UI_Image/attendance.png")
a = ImageTk.PhotoImage(ai)
# noinspection PyTypeChecker
label2 = Label(window, image=a)

label2.image = a
label2.place(x=1095, y=270)

vi = Image.open("UI_Image/verifyy.png")
v = ImageTk.PhotoImage(vi)
# noinspection PyTypeChecker
label3 = Label(window, image=v)
label3.image = v
label3.place(x=400, y=270)

Mi = Image.open("UI_Image/Manual Attendance.jpeg")
M = ImageTk.PhotoImage(Mi)
# noinspection PyTypeChecker
label4 = Label(window, image=M)

label4.image = M
label4.place(x=750, y=270)



def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1c1c1c")

    ImageUI.resizable(0, 0)
    titl = tk.Label(ImageUI, bg="#1c1c1c", relief=RIDGE, bd=10, font=("Verdana", 30, "bold"))
    titl.pack(fill=X)

    titl = tk.Label(
        ImageUI, text="Register Your Face", bg="#1c1c1c", fg="green", font=("Verdana", 25, "bold"),
    )
    titl.place(x=200, y=12)


    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#1c1c1c",
        fg="yellow",
        bd=10,
        font=("Verdana", 24, "bold"),
    )
    a.place(x=200, y=75)


    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        width=12,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl1.place(x=90, y=130)
    txt1 = tk.Entry(
        ImageUI,
        width=17,
        bd=10,
        validate="key",
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt1.place(x=250, y=130)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl2.place(x=120, y=200)
    txt2 = tk.Entry(
        ImageUI,
        width=17,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 18, "bold"),
    )
    txt2.place(x=250, y=200)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        width=10,
        height=2,
        bg="#1c1c1c",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("Verdana", 14),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=32,
        height=2,
        bd=5,
        bg="#333333",
        fg="yellow",
        relief=RIDGE,
        font=("Verdana", 14, "bold"),
    )
    message.place(x=250, y=270)



    import image_utils


    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        image_utils.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")



    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",
        fg="yellow",
        height=2,
        width=12,
        relief = RIDGE ,
        cursor = "hand2" ,
    )
    takeImg.place(x=130, y=350)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )


    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        bd=10,
        font=("Verdana", 18, "bold"),
        bg="#333333",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
        cursor="hand2",
    )
    trainImg.place(x=360, y=350)


r = tk.Button(
    window,
    text="Register new student",
    command=TakeImageUI,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
    cursor="hand2",
)
r.place(x=45, y=520)


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


r = tk.Button(
    window,
    text="Take Attendance",
    command=automatic_attedance,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
    cursor="hand2",
)
r.place(x=395, y=520)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


r = tk.Button(
    window,
    text="View Attendance",
    command=view_attendance,
    bd=10,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
    cursor="hand2",
)
r.place(x=1090, y=520)
r = tk.Button(
    window,
    text="EXIT",
    bd=10,
    command=quit,
    font=("Verdana", 16),
    bg="black",
    fg="yellow",
    height=2,
    width=17,
    cursor="hand2",
)
r.place(x=560, y=650)

manual_button = tk.Button(
    window,
    text="Manual Attendance",
    bd=10,
    command=manually_fill,
    bg="black",
    fg="yellow",
    font=("Verdana", 16),
    width=17,
    height=2,
    cursor="hand2",
)
manual_button.place(x=745, y=520)
window.mainloop()
