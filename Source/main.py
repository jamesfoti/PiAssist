from piassist import PiAssist
from sense_hat_extended import SenseHatExtended
from time import sleep
import os, sys
import threading
from threading import Thread

def main():
    pi = PiAssist() # Create new PiAssist object called "pi"
    name = "google" # We are using google b/c i can't think or come up w/ a name that gTTS can recognize easily.
    sense_extended = SenseHatExtended() # Create new sense (modified extended version)
    sense_extended.sense.clear() # Clear anything off screen before moving on.
    
    while(True):
        command = pi.listen(time_limit = 5).lower() # voice input is converted to text variable called "command"
        sense_thread = threading.Thread(target=sense_extended.play_life, args=[.1])
        
        if name in command:
            sense_extended.display_logo(animate = True) # Ligt up when rasberry pi hears user.
            sleep(1)
            
            if "exit" in command or "bye" in command or "sleep" in command:
                pi.speak("Goodbye")
                break
            elif "play game of life" in command or "game of life" in command or "play life" in command:
                print("Game of Life..")
                sense_thread.start()
            elif "stop" in command:
                sense_extended.isPlaying = False
                sense_extended.sense.clear() # Clear sense board
 
            # Process text will process any comand that is associate with this AI. For an example: playing game of life on the sense hat
            # Will not be processed by PiAssist. Commands that fall under PiAssist: crawling the web, playing music, etc...
            try:
                pi.process_text(command)
            except:
                pi.speak("Sorry, I did not understand you.")
                
        sense_extended.sense.clear() # Turn lights off when command is executed.

if __name__ == "__main__":
    main()

    
            
        
    
    

    

    