import datetime
import multiprocessing
import time
import webbrowser
import openai
import pyttsx3
import requests
import speech_recognition as sr
import smtplib
import os
import keyboard
import tkinter as tk
from tkinter import simpledialog, PhotoImage
from geopy.geocoders import Nominatim
from dotenv import load_dotenv

load_dotenv()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
volume = engine.getProperty('volume')    
engine.setProperty('volume',50.0)

openai.api_key = os.getenv('openai_key')
gmail_pass = os.getenv('gmail_pass_env')
gmail_id = os.getenv('gmail_id_env')

# Function to speak text
def _speak(text):
        
        engine.say(text)
        engine.runAndWait()

def speak(text):       
        p = multiprocessing.Process(target=_speak, args=(text,))
        p.start()
        while p.is_alive():
            if keyboard.is_pressed('esc'):
                p.terminate()
            else:
                continue
        p.join()

# Function to get user input through speech
def get_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=10)

        try:
            command = recognizer.recognize_google(audio).lower()
            print("You said:", command)
            return command
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand. Please write the prompt.")
            command = input("Type the prompt: ")
            return command
        except sr.RequestError as e:
            speak("Error connecting to Google API: {0}".format(e))
            return ""

# Function to send an email
def send_email(receiver, subject, body):
    # Configure your email server here
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmail_id, gmail_pass)

    message = f"Subject: {subject}\n\n{body}"
    server.sendmail(gmail_id, receiver, message)

    server.quit()

# Function to get GPT response
def get_gpt_response(command):
    response = openai.Completion.create(
        engine="text-davinci-002", 
        prompt=command,
        max_tokens=50
    )

    return response.choices[0].text.strip()    

# Function to set a reminder
def set_reminder():
    speak("What would you like to be reminded about?")
    reminder_text = get_audio()

    if reminder_text:
        speak("When should I remind you?")
        reminder_time = get_audio()

        if reminder_time:
            try:
                # Parse the reminder time
                reminder_datetime = datetime.datetime.strptime(reminder_time, "%H:%M:%S")
                
                # Calculate the time difference
                current_time = datetime.datetime.now()
                time_difference = (reminder_datetime - current_time).total_seconds()

                # Schedule the reminder
                if time_difference > 0:
                    time.sleep(time_difference)
                    speak(f"Reminder: {reminder_text}")
                else:
                    speak("Invalid reminder time. Please provide a future time.")
            except ValueError:
                speak("Invalid time format. Please provide the time in HH:MM:SS format.")

def get_lat_lon(city):
    geolocator = Nominatim(user_agent="your_app_name")
    location = geolocator.geocode(city)

    if location:
        return location.latitude, location.longitude
    else:
        return None, None                

# Function to get weather information
def get_weather(city):
    api_key = os.getenv('weather_api_key')
    lat, lon = get_lat_lon(city)

    if lat is not None and lon is not None:
        weather_api_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"

        try:
            response = requests.get(weather_api_url)
            data = response.json()

            if response.status_code == 200:
                temperature = round((data["main"]["temp"])-273.15, 2)
                weather_description = data["weather"][0]["description"]
                print(temperature, weather_description)
                speak(f"The current temperature in {city} is {temperature} Celsius, and the weather is {weather_description}.")
            else:
                speak("Sorry, I couldn't retrieve weather information for that city.")
        except Exception as e:
             print("Error fetching weather data:", e)
             speak("Sorry, there was an error fetching weather information.")

# Function to execute commands
def execute_command(command):
    if "hello" in command:
        speak('Hello! How can I assist you today?')

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak("The current time is " + current_time)

    elif "open Google" in command:
        webbrowser.open("https://www.google.com")

    elif "tell me the weather" in command:
        speak("Sure, I can provide weather information. What city are you interested in?")
        city = get_audio()
        if city:
            get_weather(city)

    elif "search" in command:
        speak("What would you like me to search for?")
        search_query = get_audio()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")

    elif "send email" in command:
        speak("Who is the recipient?")
        recipient = simpledialog.askstring("Recipient", "Enter the recipient's email:")
        if recipient:
            speak("What is the subject of the email?")
            subject = simpledialog.askstring("Subject", "Enter the email subject:")
            speak("What should I say in the email?")
            body = simpledialog.askstring("Body", "Enter the email body:")
            send_email(recipient, subject, body)
            speak("Email sent successfully.")

    elif "set a reminder" in command:
        set_reminder()

    elif "play music" in command:
        music_dir = "C:\\Users\\YourUsername\\Music"
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))

    elif "exit" in command:
        speak("Goodbye!")
        root.destroy() 
        exit()

    else:
        try:
            speak(f"Do you want information about {command}?")
            response = get_audio()

            if response and "yes" in response:
                gpt_response = get_gpt_response(command)
                print(gpt_response)
                speak(gpt_response)
            else:
                speak("Alright, let me know if there's anything else I can help you with.")
        except Exception as e:
            print("Error:", e)
            speak("Sorry, there was an error processing your request.")

# Function to handle button click
def on_submit_click():
    user_input = entry.get()
    entry.delete(0, tk.END)  # Clear the entry field
    execute_command(user_input)

# Function to handle microphone button click
def on_mic_click():
    user_input = get_audio()
    if user_input:
        entry.insert(tk.END, user_input)
    execute_command(user_input)

# Main loop
if __name__ == "__main__":
    root = tk.Tk()
    root.title("AssistantX")

    label = tk.Label(root, text="AssistantX is ready. How can I assist you?")
    label.pack(pady=10)

    entry = tk.Entry(root, width=50)
    entry.pack(pady=10)

    submit_button = tk.Button(root, text="Submit", command=on_submit_click)
    submit_button.pack(pady=10)

    mic_icon = PhotoImage(file=r"C:\Users\Nipun Arora\Downloads\microphone.png")  # Replace with the path to your microphone icon image
    mic_button = tk.Button(root, image=mic_icon, command=on_mic_click, width=50, height=50)
    mic_button.image = mic_icon
    mic_button.pack(pady=10)

    root.mainloop()