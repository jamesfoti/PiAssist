import speech_recognition as sr
from gtts import gTTS
import playsound
from datetime import datetime
import wikipedia
import pyjokes
import geocoder
import wolframalpha 
import json 
import requests
import os

class PiAssist:
    
    # Open Weather API info:
    api_key = "API_KEY"
    current_city_location = "San Jose" # San Jose by default
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Wolfram Alphha API info:
    wolf_api_id = "API_KEY"
    client = None # Used for wolframalpha.Client(wolf_api_id) 
    
    def __init__(self):
        print("PiAssist Initialized!")
        self.r = sr.Recognizer()
        self.mic = sr.Microphone()
        self.language = "en"
        self.current_city_location = self.get_current_city_location()
        self.client = wolframalpha.Client(self.wolf_api_id) 

    def speak(self, text):
        text = str(text) # Incase non-string is passed through.
        tts = gTTS(text = text, lang = self.language, slow = False)
        file_name = "voice.mp3"
        tts.save(file_name)
        playsound.playsound(file_name, True)

    def listen(self, time_limit = 5):
        
        said = ""
        
        with self.mic as source:
            print("Say something!")
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
        try:
            said = self.r.recognize_google(audio)
            print("You said: " + said)
            return said
        
        except:
            print("Could not understand your command.")
        
        return said
    
    def process_text(self, text):
        print("Processing Command!")
                
        if "time" in text:
            self.speak(self.get_current_time())
        elif "date" in text:
            self.speak(self.get_current_date())
        elif "weather" in text or "forecast" in text:
            self.speak("Here is a summary of today's weather.")
            self.tell_weather()
        elif "temperature" in text:
            self.speak("The temperature is " + str(self.get_temp()) + " degrees.")
        elif "who made you" in text or "who created you" in text:
            self.speak("I was created by James Foti.")
        elif "wikipedia" in text or "who is" in text:
            self.search_wikipedia(text)
        elif "what is" in text or "what's" in text or "when is" in text:
            try: self.search_wolfram(text)
            except: self.search_wikipedia(text)
        elif "calculate" in text:
            self.calculate(text)
        elif "joke" in text:
            self.tell_joke()
        elif "hello" in text:
            self.speak("Hello")
        elif "how are you" in text:
            self.speak("I am good, how are you?")
        elif "restart" in text:
            self.restart()
        elif "shutdown" in text:
            self.shutdown()
        
    def get_current_time(self):
        # For more info: https://www.guru99.com/date-time-and-datetime-classes-in-python.html
        print("Get Current Time!")
        now = datetime.now()
        return now.strftime("%I:%M:%S %p")
    
    def get_current_date(self):
        # For more info: https://www.guru99.com/date-time-and-datetime-classes-in-python.html
        print("Get Current Date!")
        now = datetime.now()
        return now.strftime("%A, %d %B, %y")
    
    def search_wikipedia(self, query):
        print("Searching Wikipedia!")
        query = query.replace("wikipedia", "") 
        results = wikipedia.summary(query, sentences = 3) 
        self.speak("According to Wikipedia, " + str(results))
        
    def search_wolfram(self, query):
        print("Getting Answer from Wolfram Alpha!")
        indx = query.lower().split().index('google') 
        query = query.split()[indx + 1:]
        res = self.client.query(' '.join(query))
        answer = next(res.results).text
        self.speak(answer)

    def calculate(self, question):
        print("Calculating via Wolfram Alpha!")
        indx = question.lower().split().index('calculate') 
        query = question.split()[indx + 1:] 
        res = self.client.query(' '.join(query)) 
        answer = next(res.results).text
        self.speak("The answer is " + answer)
    
    def tell_joke(self):
        print("Telling a Joke!")
        joke = pyjokes.get_joke()
        self.speak(joke)
        
    def get_current_city_location(self):
        # Documentatino: https://pypi.org/project/geocoder/
        print("Getting City Location!")
        g = geocoder.ip('me')
        return g.city
    
    def get_current_latlng(self):
        print("Getting Lat and Long Location!")
        g = geocoder.ip('me')
        return g.latlng
    
    def get_current_weather_data(self):
        print("Getting Weather!")
        # api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}\
        # For mor info: https://openweathermap.org/current
        latlng = self.get_current_latlng()
        lat = latlng[0]
        lon = latlng[1]
        final_url = self.base_url + "lat=" + str(lat) + "&lon=" + str(lon) + "&units=imperial" + "&appid=" + self.api_key
        
        weather_data = requests.get(final_url).json()
        return weather_data
    
    def get_temp(self):
        weather_data = self.get_current_weather_data()
        temp = weather_data['main']['temp']
        return temp
    
    def get_humudity(self):
        weather_data = self.get_current_weather_data()
        humidity = round(weather_data['main']['humidity'])
        return humidity
    
    def get_weather_description(self):
        weather_data = self.get_current_weather_data()
        description = weather_data['weather'][0]['description']
    
    def tell_weather(self):
        weather_data = self.get_current_weather_data()
        
        # Weather description:
        description = weather_data['weather'][0]['description']
        
        # Temperatures:
        temp = weather_data['main']['temp']
        feels_like = round(weather_data['main']['feels_like'])
        
        # Humudity and Pressure:
        humidity = round(weather_data['main']['humidity'])
        pressure = round(weather_data['main']['pressure'])
        
        # Wind:
        wind_speed = round(weather_data['wind']['speed'])
        wind_direction = round(weather_data['wind']['deg'])
        
        self.speak("The current forecast is " + str(description))
        self.speak("The current temperature is " + str(temp) + " degrees " + " and it feels like " + str(feels_like) + " degrees ")
        self.speak("Humidity is " + str(humidity) + " and pressure is " + str(pressure))
        self.speak("Wind speed is at about " + str(wind_speed) + "miles per hour with a direction of " + str(wind_direction) + " degrees")
        
    def restart(self):
        os.system("sudo reboot")
        
    def shutdown(self):
        os.system("sudo shutdown")