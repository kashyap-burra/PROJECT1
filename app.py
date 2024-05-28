import tkinter as tk
import io
from PIL import Image, ImageTk
import requests
import base64
import customtkinter as ctk
import os
from tkinter import filedialog
import time
import speech_recognition as sr

image_data = None
start_time = None

def generate_and_display_image():
    global image_data, start_time
    prompt_text = prompt.get("1.0", "end-1c")

    url = "http://127.0.0.1:7860"
    payload = {
        "prompt": prompt_text,
        "steps": 20,
        "width": 400,
        "height": 300,
    }

    start_time = time.time()

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()

    image_data = base64.b64decode(r['images'][0])

    image = Image.open(io.BytesIO(image_data))
    photo = ImageTk.PhotoImage(image)

    lmain.configure(image=photo)
    lmain.image = photo

    end_time = time.time()
    time_taken = end_time - start_time
    time_label.configure(text=f"Time Taken : {time_taken:.2f} seconds", font=('Helvetica', 18))

def save_image():
    global image_data
    file_path = filedialog.asksaveasfilename(defaultextension=".jpg")

    if file_path:
        with open(file_path, "wb") as file:
            file.write(image_data)

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        prompt_text = recognizer.recognize_google(audio)
        print("You said:", prompt_text)
        prompt.delete("1.0", "end")
        prompt.insert("end", prompt_text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))

def clear_prompt(event):
    prompt.delete("1.0", "end")

app = tk.Tk()
app.geometry("1280x720")
app.title("Text 2 Face")

prompt_frame = tk.Frame(app)
prompt_frame.place(x=310, y=50)

prompt = tk.Text(prompt_frame, height=2, width=57, font=('Helvetica', 15))
prompt.insert("end", "Enter the description here . . .")
prompt.bind("<FocusIn>", clear_prompt)
prompt.pack(side="left")

mic_button = tk.Button(prompt_frame, text="🎤", font=('Helvetica', 18), command=speech_to_text)
mic_button.pack(side="left")

lmain = ctk.CTkLabel(app, text=" ")
lmain.place(x=300, y=200)

trigger = ctk.CTkButton(
    app,
    height=40,
    width=120,
    text="Generate",
    text_color="white",
    fg_color="blue",
    command=generate_and_display_image,
    font=('Helvetica', 18)
)
trigger.place(x=400, y=115)

save_button = ctk.CTkButton(
    app,
    height=40,
    width=120,
    text="Download",
    text_color="white",
    fg_color="blue",
    command=save_image,
    font=('Helvetica', 18)
)
save_button.place(x=730, y=115)

time_label = ctk.CTkLabel(app, height=20, width=200, text_color="black", text=" ")
time_label.place(x=520, y=165)

app.mainloop()