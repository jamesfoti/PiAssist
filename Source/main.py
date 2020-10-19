from piassist import PiAssist
from sense_hat_extended import SenseHatExtended
import threading
from time import sleep



def main():
    pi = PiAssist() # Create new PiAssist object called "pi"
    sense_extended = SenseHatExtended() # Create new sense (modified extended version)
    sense_extended.sense.clear() # Clear anything off screen before moving on.
    th = threading.Thread(target=sense_extended.play_life, args=(.1,))
    
    while(True):
        command = pi.listen(time_limit = 5).lower() # voice input is converted to text variable called "command"
        
        if "google" in command:
            sense_extended.display_logo(animate = True) # Ligt up when rasberry pi hears user.
            sleep(1)
            
            if "exit" in command or "bye" in command or "sleep" in command:
                pi.speak("Goodbye")
                break
            elif "life" in command and "game" in command:
                th.start()
            elif "stop" in command:
                print("terminate thread!")
                sense_extended.isPlaying = False # This will cause the thread above to stop.
                
            # Process text will process any comand that is associate with this AI. For an example: playing game of life on the sense hat
            # Will not be processed by PiAssist. Commands that fall under PiAssist: crawling the web, playing music, etc...
            pi.process_text(command)
            
        sense_extended.sense.clear() # Turn lights off when command is executed.

if __name__ == "__main__":
    main()
    
            
        
    
    

    

    