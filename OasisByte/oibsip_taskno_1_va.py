import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

# Set up the Text-to-Speech engine
engine = pyttsx3.init()

# Set up the Speech Recognition
recognizer = sr.Recognizer()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def process_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}")
    elif "search" in command:
        search_query = command.replace("search", "").strip()
        speak(f"Searching the web for {search_query}")
        search_web(search_query)
    else:
        speak("I'm sorry, I didn't understand that command.")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def main():
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        process_command(command)
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

if __name__ == "__main__":
    main()
