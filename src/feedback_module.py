
import pyttsx3

class FeedbackModule:
    def __init__(self):
        self.engine = pyttsx3.init()
        
    def speak(self, text):
        """Use text-to-speech to speak the given text"""
        print(f"System: {text}") 
        self.engine.say(text)      # Voice feedback
        self.engine.runAndWait()
