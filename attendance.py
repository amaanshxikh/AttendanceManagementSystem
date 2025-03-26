import tkinter as tk
from tkinter import *
from tkinter import ttk
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.font as font
import pyttsx3
import threading

# Try to import ttkthemes, with a fallback if not available
try:
    from ttkthemes import ThemedStyle
    THEMED_STYLE_AVAILABLE = True
except ImportError:
    THEMED_STYLE_AVAILABLE = False

# project module
# import show_attendance
import takeImage
import trainImage
import automaticAttedance

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

# Paths
haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage1"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# Create main window
window = tk.Tk()
window.title("Attendify - Attendance System")
window.geometry("1280x720")
window.configure(background="#1c1c1c")

# Create custom fonts
title_font = font.Font(family="Verdana", size=30, weight="bold")
heading_font = font.Font(family="Verdana", size=24, weight="bold")
subheading_font = font.Font(family="Verdana", size=18, weight="bold")
normal_font = font.Font(family="Verdana", size=14)
button_font = font.Font(family="Verdana", size=16)

# Style configuration
if THEMED_STYLE_AVAILABLE:
    style = ThemedStyle(window)
    style.set_theme("equilux")  # Modern dark theme
else:
    style = ttk.Style()

# Configure custom styles
style.configure('TFrame', background='#1c1c1c')
style.configure('Card.TFrame', background='#2c2c2c', relief=RAISED, borderwidth=2)
style.configure('TLabel', background='#1c1c1c', foreground='yellow', font=normal_font)
style.configure('Header.TLabel', font=heading_font, foreground='yellow', background='#1c1c1c')
style.configure('SubHeader.TLabel', font=subheading_font, foreground='yellow', background='#1c1c1c')
style.configure('TButton', font=button_font, background='#333333', foreground='black')
style.configure('Accent.TButton', background='#ffd700', foreground='black')
style.configure('TEntry', font=normal_font, fieldbackground='#333333', foreground='black')
style.configure('TProgressbar', background='yellow')

# Function for error screen
def err_screen():
    sc1 = tk.Toplevel(window)
    sc1.geometry("400x150")
    sc1.title("Warning!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)
    
    # Center the window
    position_x = int((window.winfo_screenwidth()/2) - (400/2))
    position_y = int((window.winfo_screenheight()/2) - (150/2))
    sc1.geometry(f"+{position_x}+{position_y}")
    
    # Error label
    ttk.Label(
        sc1,
        text="Enrollment & Name required!",
        style='Header.TLabel',
    ).pack(pady=20)
    
    # OK button
    ttk.Button(
        sc1,
        text="OK",
        command=sc1.destroy,
        style='Accent.TButton',
    ).pack(pady=10)

# Validation function for enrollment input
def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

# Create a splash screen
def show_splash():
    splash = tk.Toplevel(window)
    splash.title("")
    splash.geometry("500x300")
    splash.overrideredirect(True)
    splash.configure(background="#1c1c1c")
    
    # Center the splash screen
    position_x = int((window.winfo_screenwidth()/2) - (500/2))
    position_y = int((window.winfo_screenheight()/2) - (300/2))
    splash.geometry(f"+{position_x}+{position_y}")
    
    # Logo
    try:
        logo = Image.open("UI_Image/0001.png")
        logo = logo.resize((100, 100), Image.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo)
        
        logo_label = tk.Label(splash, image=logo_img, bg="#1c1c1c")
        logo_label.image = logo_img
        logo_label.pack(pady=20)
    except:
        # If logo not found, just show the title
        pass
    
    # Title
    title = tk.Label(splash, text="Attendify", font=title_font, bg="#1c1c1c", fg="yellow")
    title.pack(pady=10)
    
    # Progress bar
    progress = ttk.Progressbar(splash, orient="horizontal", length=400, mode="determinate")
    progress.pack(pady=20)
    
    # Update progress
    def update_progress():
        for i in range(101):
            progress["value"] = i
            splash.update()
            time.sleep(0.02)
        splash.destroy()
    
    # Start after a short delay
    splash.after(200, update_progress)
    
    # Voice welcome
    threading.Thread(target=lambda: text_to_speech("Welcome to Attendify")).start()
    
    return splash

# Create card frame
def create_card_frame(parent):
    card = ttk.Frame(parent, style='Card.TFrame')
    return card

# ======= MAIN LAYOUT =======
# Main container
main_container = ttk.Frame(window)
main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Header frame
header_frame = ttk.Frame(main_container)
header_frame.pack(fill=X, pady=10)

# Load logo
try:
    logo = Image.open("UI_Image/0001.png")
    logo = logo.resize((60, 60), Image.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo)
    
    logo_label = ttk.Label(header_frame, image=logo_img, background="#1c1c1c")
    logo_label.image = logo_img
    logo_label.pack(side=LEFT, padx=10)
except:
    # If logo can't be loaded, skip it
    pass

# Title
title_label = ttk.Label(header_frame, text="Attendify", style='Header.TLabel')
title_label.pack(side=LEFT, padx=10)

# Welcome message
welcome_frame = ttk.Frame(main_container)
welcome_frame.pack(fill=X, pady=20)

welcome_label = ttk.Label(
    welcome_frame, 
    text="Welcome to Attendify", 
    font=title_font, 
    foreground="yellow", 
    background="#1c1c1c"
)
welcome_label.pack()

# Cards container
cards_frame = ttk.Frame(main_container)
cards_frame.pack(fill=BOTH, expand=True, pady=20)

# Create a single-column for just the Register card
cards_frame.columnconfigure(0, weight=1)
cards_frame.rowconfigure(0, weight=1)

# Register Student Card - centered
register_card = create_card_frame(cards_frame)
register_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Try to load register image
try:
    ri = Image.open("UI_Image/register.png")
    ri = ri.resize((150, 150), Image.LANCZOS)
    r_img = ImageTk.PhotoImage(ri)
    
    register_img_label = ttk.Label(register_card, image=r_img, background="#2c2c2c")
    register_img_label.image = r_img
    register_img_label.pack(pady=20)
except:
    # If image can't be loaded, show a placeholder
    register_label = ttk.Label(register_card, text="Register", font=heading_font, background="#2c2c2c", foreground="yellow")
    register_label.pack(pady=20)

register_title = ttk.Label(register_card, text="Register Students", font=subheading_font, background="#2c2c2c", foreground="yellow")
register_title.pack(pady=10)

# COMMENTED OUT: Take Attendance Card
# attendance_card = create_card_frame(cards_frame)
# attendance_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
# 
# # Try to load attendance image
# try:
#     ai = Image.open("UI_Image/attendance.png")
#     ai = ai.resize((150, 150), Image.LANCZOS)
#     a_img = ImageTk.PhotoImage(ai)
#     
#     attendance_img_label = ttk.Label(attendance_card, image=a_img, background="#2c2c2c")
#     attendance_img_label.image = a_img
#     attendance_img_label.pack(pady=20)
# except:
#     # If image can't be loaded, show a placeholder
#     attendance_label = ttk.Label(attendance_card, text="Attendance", font=heading_font, background="#2c2c2c", foreground="yellow")
#     attendance_label.pack(pady=20)
# 
# attendance_title = ttk.Label(attendance_card, text="Take Attendance", font=subheading_font, background="#2c2c2c", foreground="yellow")
# attendance_title.pack(pady=10)

# COMMENTED OUT: View Attendance Card
# view_card = create_card_frame(cards_frame)
# view_card.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
# 
# # Try to load view image
# try:
#     vi = Image.open("UI_Image/verifyy.png")
#     vi = vi.resize((150, 150), Image.LANCZOS)
#     v_img = ImageTk.PhotoImage(vi)
#     
#     view_img_label = ttk.Label(view_card, image=v_img, background="#2c2c2c")
#     view_img_label.image = v_img
#     view_img_label.pack(pady=20)
# except:
#     # If image can't be loaded, show a placeholder
#     view_label = ttk.Label(view_card, text="View", font=heading_font, background="#2c2c2c", foreground="yellow")
#     view_label.pack(pady=20)
# 
# view_title = ttk.Label(view_card, text="View Attendance", font=subheading_font, background="#2c2c2c", foreground="yellow")
# view_title.pack(pady=10)

# Button frame
button_frame = ttk.Frame(main_container)
button_frame.pack(fill=X, pady=20)

# Function to show register UI
def TakeImageUI():
    ImageUI = tk.Toplevel(window)
    ImageUI.title("Register Student")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1c1c1c")
    ImageUI.resizable(0, 0)
    
    # Center the window
    position_x = int((window.winfo_screenwidth()/2) - (780/2))
    position_y = int((window.winfo_screenheight()/2) - (480/2))
    ImageUI.geometry(f"+{position_x}+{position_y}")
    
    # Main frame
    main_frame = ttk.Frame(ImageUI)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)
    
    # Header
    header_label = ttk.Label(main_frame, text="Register Your Face", style='Header.TLabel')
    header_label.pack(pady=10)
    
    # Instructions
    instructions_label = ttk.Label(main_frame, text="Enter the details", style='SubHeader.TLabel')
    instructions_label.pack(pady=10)
    
    # Form frame
    form_frame = ttk.Frame(main_frame)
    form_frame.pack(fill=BOTH, expand=True, pady=20)
    
    # Enrollment number
    enrollment_frame = ttk.Frame(form_frame)
    enrollment_frame.pack(fill=X, pady=10)
    
    enrollment_label = ttk.Label(enrollment_frame, text="Enrollment No:", width=15)
    enrollment_label.pack(side=LEFT, padx=10)
    
    enrollment_var = tk.StringVar()
    enrollment_entry = ttk.Entry(
        enrollment_frame, 
        textvariable=enrollment_var, 
        width=20, 
        font=normal_font,
        validate="key"
    )
    enrollment_entry["validatecommand"] = (enrollment_entry.register(testVal), "%P", "%d")
    enrollment_entry.pack(side=LEFT, padx=10)
    
    # Name
    name_frame = ttk.Frame(form_frame)
    name_frame.pack(fill=X, pady=10)
    
    name_label = ttk.Label(name_frame, text="Name:", width=15)
    name_label.pack(side=LEFT, padx=10)
    
    name_var = tk.StringVar()
    name_entry = ttk.Entry(
        name_frame, 
        textvariable=name_var, 
        width=20, 
        font=normal_font
    )
    name_entry.pack(side=LEFT, padx=10)
    
    # Notification
    notification_frame = ttk.Frame(form_frame)
    notification_frame.pack(fill=X, pady=10)
    
    notification_label = ttk.Label(notification_frame, text="Notification:", width=15)
    notification_label.pack(side=LEFT, padx=10)
    
    message = ttk.Label(notification_frame, text="", width=40, background="#333333", foreground="yellow")
    message.pack(side=LEFT, padx=10, pady=10, ipady=5)
    
    # Button frame
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=X, pady=20)
    
    # Functions for buttons
    def take_image():
        l1 = enrollment_var.get()
        l2 = name_var.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        enrollment_var.set("")
        name_var.set("")
    
    def train_image():
        # Show progress
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=X, pady=10)
        
        progress = ttk.Progressbar(progress_frame, orient="horizontal", length=300, mode="indeterminate")
        progress.pack(pady=10)
        progress.start()
        
        # Run training in a separate thread
        def training_thread():
            trainImage.TrainImage(
                haarcasecade_path,
                trainimage_path,
                trainimagelabel_path,
                message,
                text_to_speech,
            )
            progress.stop()
            progress_frame.destroy()
        
        thread = threading.Thread(target=training_thread)
        thread.daemon = True
        thread.start()
    
    # Take image button
    take_image_btn = ttk.Button(
        button_frame,
        text="Take Image",
        command=take_image,
        style='Accent.TButton',
    )
    take_image_btn.pack(side=LEFT, padx=10, fill=X, expand=True)
    
    # Train image button
    train_image_btn = ttk.Button(
        button_frame,
        text="Train Image",
        command=train_image,
        style='Accent.TButton',
    )
    train_image_btn.pack(side=LEFT, padx=10, fill=X, expand=True)

# Create buttons
register_btn = ttk.Button(
    register_card,
    text="Register a new student",
    command=TakeImageUI,
    style='Accent.TButton',
)
register_btn.pack(pady=10, padx=20, fill=X)

# COMMENTED OUT: Take Attendance button
# attendance_btn = ttk.Button(
#     attendance_card,
#     text="Take Attendance",
#     command=lambda: automaticAttedance.subjectChoose(text_to_speech),
#     style='Accent.TButton',
# )
# attendance_btn.pack(pady=10, padx=20, fill=X)

# COMMENTED OUT: View Attendance button
# view_btn = ttk.Button(
#     view_card,
#     text="View Attendance",
#     command=lambda: show_attendance.subjectchoose(text_to_speech),
#     style='Accent.TButton',
# )
# view_btn.pack(pady=10, padx=20, fill=X)

# Exit button at the bottom
exit_frame = ttk.Frame(main_container)
exit_frame.pack(fill=X, pady=20)

exit_btn = ttk.Button(
    exit_frame,
    text="EXIT",
    command=window.quit,
    style='TButton',
)
exit_btn.pack(side=BOTTOM, pady=10, padx=20)

# Add hover effects
def add_hover_effect(widget):
    widget.bind("<Enter>", lambda e: widget.configure(background="#3c3c3c"))
    widget.bind("<Leave>", lambda e: widget.configure(background="#2c2c2c"))

# Apply hover effects to register card only
add_hover_effect(register_card)

# COMMENTED OUT: Hover effects for other cards
# add_hover_effect(attendance_card)
# add_hover_effect(view_card)

# Show splash screen before showing the main window
window.withdraw()  # Hide main window
splash = show_splash()
window.after(2500, lambda: [window.deiconify(), window.lift()])  # Show main window after splash

# Run the app
window.mainloop()