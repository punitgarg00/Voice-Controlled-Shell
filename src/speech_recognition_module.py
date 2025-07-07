import speech_recognition as sr

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
    def listen_for_command(self):
        """
        Listen for audio input and convert to text
        Returns the recognized text or None if recognition fails
        """
        try:
            print("Listening...")
            with self.microphone as source:
                audio = self.recognizer.listen(source)
                
            print("Processing...")
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text.lower()
            
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
