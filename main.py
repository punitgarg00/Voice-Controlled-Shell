# main.py
import os
import time
from src.speech_recognition_module import SpeechRecognizer
from src.command_processor import CommandProcessor
from src.command_executor import CommandExecutor
from src.feedback_module import FeedbackModule

def main():
    # Set up paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, "config", "commands_config.json")
    
    # Initialize modules
    feedback = FeedbackModule()
    speech_recognizer = SpeechRecognizer()
    command_processor = CommandProcessor(config_path)
    command_executor = CommandExecutor(feedback)
    
    feedback.speak("Voice Command System is now active. Please speak a command.")
    
    # State tracking for multi-turn interactions
    pending_command = None
    pending_details = None

    # Main loop
    while True:
        try:
            text = speech_recognizer.listen_for_command()
            
            if text:
                # Handle pending command first
                if pending_command:
                    # Create args based on pending command type
                    args = {}
                    if pending_command == "make a new directory":
                        args['dir_name'] = text.strip().replace(" ", "_")
                    elif pending_command == "create a file":
                        args['file_name'] = text.strip().replace(" ", "_")
                    
                    # Execute with captured argument
                    command_executor.execute_command(pending_command, pending_details, args)
                    pending_command = None
                    pending_details = None
                    continue
                
                # Normal command processing
                command_key, details, args = command_processor.process_command(text)
                
                if command_key:
                    # Check if command requires additional parameters
                    if command_key in ["make a new directory", "create a file"] and not args.get('dir_name') and not args.get('file_name'):
                        feedback.speak(f"Please specify the {'directory' if 'directory' in command_key else 'file'} name.")
                        pending_command = command_key
                        pending_details = details
                    else:
                        feedback.speak(f"Executing: {command_key}")
                        command_executor.execute_command(command_key, details, args)
                else:
                    feedback.speak("Command not recognized. Please try again.")
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            feedback.speak("Voice Command System shutting down.")
            break
        except Exception as e:
            feedback.speak(f"An error occurred: {str(e)}")
            continue

if __name__ == "__main__":
    main()
