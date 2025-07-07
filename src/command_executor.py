
import os
import subprocess
import datetime
import random
import string
import platform
import socket
import getpass
import win32com.client as wincom
import calendar
import datetime
import sys
class CommandExecutor:
    def __init__(self, feedback_module):
        self.feedback = feedback_module

    def execute_command(self, command_key, details, args=None):
        """Execute the specified command with arguments"""
        if not command_key or not details:
            self.feedback.speak("Command not recognized.")
            return

        if args is None:
            args = {}

        #  command Mapping f
        command_map = {
            "shutdown": self._shutdown,
            "list file": self._list_file,
            "list formatted files": self._list_formatted_files,
            "list file permissions": self._list_file_permissions,
            "list hidden files": self._list_hidden_files,
            "current working directory": self._current_working_directory,
            "what is the date today": self._get_date,
            "what is the day today": self._get_day,
            "what is the time": self._get_time,
            "calendar": self._show_calendar,
            "what is the username": self._get_username,
            "create a random file": self._create_random_file,
            "go to home directory": self._go_to_home,
            "go to root directory": self._go_to_root,
            "go to my directory": self._go_to_user_home,
            "run ps": self._run_ps,
            "show network status": self._show_network,
            "open nano editor": self._open_nano,
            "open gedit editor": self._open_gedit,
            "open sublime editor": self._open_sublime,
            "what is the status and configuration of network": self._show_network_config,
            "list users": self._list_users,
            "list all users": self._list_users,
            "list user": self._list_users,
            "who created you": self._creator_info,
            "exit": self._exit_program,
            "quit": self._exit_program,
            "stop": self._exit_program,
            "manual": self._manual,
            "make a new directory": lambda: self._make_directory(args.get('dir_name')),
            "create a file": lambda: self._create_file(args.get('file_name')),
            "delete a file": lambda: self._delete_file(args.get('file_name')),
            "remove a file": lambda: self._delete_file(args.get('file_name')),
            "tell me the file type": lambda: self._get_file_type(args.get('file_name')),


        }

        try:
            if command_key in command_map:
                command_map[command_key]()
            else:
                self.feedback.speak(f"Command {command_key} is recognized but not implemented yet.")
        except Exception as e:
            self.feedback.speak(f"An error occurred: {str(e)}")



    def _show_calendar(self):
        """Display a calendar for the current month"""
        self.feedback.speak("Displaying the calendar")
       
        
        now = datetime.datetime.now()
        cal = calendar.month(now.year, now.month)
        print(cal)
        self.feedback.speak(f"Showing calendar for {now.strftime('%B %Y')}")

   
    def _shutdown(self):
        self.feedback.speak("Shutting down the PC immediately")
        subprocess.run(["shutdown", "/s", "/t", "0"])
    
    def _list_file(self):
        self.feedback.speak("Listing all files")
        result = subprocess.run(["dir"], shell=True, capture_output=True, text=True)
        print(result.stdout)
    
    def _list_formatted_files(self):
        self.feedback.speak("Listing all files in long format with permission")
        result = subprocess.run(["dir", "/q"], shell=True, capture_output=True, text=True)
        print(result.stdout)
    
    def _list_file_permissions(self):
        self.feedback.speak("Listing all files in long format with permission")
        result = subprocess.run(["icacls", "."], shell=True, capture_output=True, text=True)
        print(result.stdout)
    
    def _list_hidden_files(self):
        self.feedback.speak("Listing hidden files")
        result = subprocess.run(["dir", "/a:h"], shell=True, capture_output=True, text=True)
        print(result.stdout)
    
    def _current_working_directory(self):
        self.feedback.speak("Present Working Directory")
        result = subprocess.run(["cd"], shell=True, capture_output=True, text=True)
        print(result.stdout)
        self.feedback.speak(f"You are in {os.getcwd()}")
    
    def _get_date(self):
        self.feedback.speak("Telling the date")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        print(f"Today's date: {today}")
        self.feedback.speak(f"Today's date is {today}")
    
    def _get_day(self):
        self.feedback.speak("Telling the day")
        day = datetime.datetime.now().strftime("%A")
        print(f"Today is {day}")
        self.feedback.speak(f"Today is {day}")
    
    def _get_time(self):
        self.feedback.speak("Telling the time")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"Current time: {time}")
        self.feedback.speak(f"The current time is {time}")
    
    def _get_username(self):
        """Get and display the current username"""
        self.feedback.speak("Getting your username")
        try:
         
            username = getpass.getuser()
            print(f"Current username: {username}")
            self.feedback.speak(f"Your username is {username}")
        except Exception as e:
            print(f"Error getting username: {str(e)}")
            self.feedback.speak("Sorry, I couldn't retrieve your username")

    def _create_random_file(self):
        """Create a file with a random name and timestamp"""
        self.feedback.speak("Creating a random file")
        try:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            filename = f"random_{timestamp}_{random_str}.txt"
            
            with open(filename, 'w') as f:
                f.write(f"This is a random file created at {datetime.datetime.now()}")
            
            print(f"Created random file: {filename}")
            self.feedback.speak(f"Created random file {filename}")
        except Exception as e:
            print(f"Error creating random file: {str(e)}")
            self.feedback.speak("Sorry, I couldn't create a random file")

    def _go_to_home(self):
        """Navigate to the home directory"""
        self.feedback.speak("Going to home directory")
        try:
            os.chdir(os.path.expanduser("~"))
            print(f"Current directory: {os.getcwd()}")
            self.feedback.speak("Now in home directory")
        except Exception as e:
            print(f"Error navigating to home directory: {str(e)}")
            self.feedback.speak("Sorry, I couldn't go to the home directory")

    def _go_to_root(self):
        """Navigate to the root directory"""
        self.feedback.speak("Going to root directory")
        try:
            if platform.system() == "Windows":
             os.chdir("C:\\")
            else:
    
                os.chdir("/")
            print(f"Current directory: {os.getcwd()}")
            self.feedback.speak("Now in root directory")
        except Exception as e:
            print(f"Error navigating to root directory: {str(e)}")
            self.feedback.speak("Sorry, I couldn't go to the root directory")

    def _go_to_user_home(self):
        """Navigate to the user's home directory"""
        self.feedback.speak("Going to your home directory")
        try:
            os.chdir(os.path.expanduser("~"))
            print(f"Current directory: {os.getcwd()}")
            self.feedback.speak("Now in your home directory")
        except Exception as e:
            print(f"Error navigating to user home directory: {str(e)}")
            self.feedback.speak("Sorry, I couldn't go to your home directory")

    def _run_ps(self):
        """Display process status (equivalent to ps on Unix or tasklist on Windows)"""
        self.feedback.speak("Showing process status")
        try:
            if platform.system() == "Windows":
                result = subprocess.run(["tasklist"], shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run(["ps", "-ef"], shell=True, capture_output=True, text=True)
            print(result.stdout)
            self.feedback.speak("Process status displayed")
        except Exception as e:
            print(f"Error showing process status: {str(e)}")
            self.feedback.speak("Sorry, I couldn't show the process status")

    def _show_network(self):
        """Show network status"""
        self.feedback.speak("Showing network status")
        try:
            if platform.system() == "Windows":
                result = subprocess.run(["ipconfig"], shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run(["ifconfig"], shell=True, capture_output=True, text=True)
            print(result.stdout)
            self.feedback.speak("Network status displayed")
        except Exception as e:
            print(f"Error showing network status: {str(e)}")
            self.feedback.speak("Sorry, I couldn't show the network status")

    def _create_shortcut(self):
        """Create a shortcut (link) to a file"""
        self.feedback.speak("This function requires additional parameters. Please specify the target file and link name.")
        print("Usage: Create a link to a file or directory")
        print("Example: mklink /D LinkName TargetPath")

    def _create_file(self):
        """Create a new file"""
        self.feedback.speak("This function requires a filename. Please specify the file to create.")
        print("Usage: Create a new file")
        print("Example: echo. > filename.txt")
 

    def _open_nano(self):
        """Open the Notepad editor (equivalent of nano on Windows)"""
        self.feedback.speak("Opening Notepad")
        try:
            subprocess.Popen(["notepad.exe"])
            print("Notepad opened")
        except Exception as e:
            print(f"Error opening Notepad: {str(e)}")
            self.feedback.speak("Sorry, I couldn't open Notepad")

    def _open_gedit(self):
        """Open the Notepad editor (equivalent of gedit on Windows)"""
        self.feedback.speak("Opening Notepad (Windows equivalent of gedit)")
        try:
            subprocess.Popen(["notepad.exe"])
            print("Notepad opened")
        except Exception as e:
            print(f"Error opening Notepad: {str(e)}")
            self.feedback.speak("Sorry, I couldn't open Notepad")

    def _open_sublime(self):
        """Open Sublime Text editor"""
        self.feedback.speak("Opening Sublime Text")
        try:
            subprocess.Popen(["subl.exe"])
            print("Sublime Text opened")
        except FileNotFoundError:
            print("Sublime Text not found. Ensure it's installed and in your PATH.")
            self.feedback.speak("Sublime Text not found. Make sure it's installed properly.")
        except Exception as e:
            print(f"Error opening Sublime Text: {str(e)}")
            self.feedback.speak("Sorry, I couldn't open Sublime Text")

    def _show_network_config(self):
        """Show detailed network configuration"""
        self.feedback.speak("Showing detailed network configuration")
        try:
            if platform.system() == "Windows":
                result = subprocess.run(["netstat", "-a"], shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run(["netstat", "-tuln"], shell=True, capture_output=True, text=True)
            print(result.stdout)
            self.feedback.speak("Network configuration displayed")
        except Exception as e:
            print(f"Error showing network configuration: {str(e)}")
            self.feedback.speak("Sorry, I couldn't show the network configuration")

    def _make_directory(self, dir_name=None):
        if not dir_name:
            self.feedback.speak("This function requires a directory name. Please specify which directory to create.")
            print("Usage: Create a new directory")
            print("Example: mkdir new_directory")
            return
        try:
            os.mkdir(dir_name)
            self.feedback.speak(f"Directory '{dir_name}' created successfully.")
        except FileExistsError:
            self.feedback.speak(f"Directory '{dir_name}' already exists.")
        except Exception as e:
            self.feedback.speak(f"An error occurred: {str(e)}")

    def _list_users(self):
        """List all users on the system"""
        self.feedback.speak("Listing all users")
        try:
            if platform.system() == "Windows":
                result = subprocess.run(["net", "user"], shell=True, capture_output=True, text=True)
            else:
                result = subprocess.run(["cat", "/etc/passwd"], shell=True, capture_output=True, text=True)
            print(result.stdout)
            self.feedback.speak("Users listed")
        except Exception as e:
            print(f"Error listing users: {str(e)}")
            self.feedback.speak("Sorry, I couldn't list the users")

    def _creator_info(self):
        """Display information about the creator"""
        self.feedback.speak("I was created by an awesome developer who built me as a voice-controlled command execution system.Developers are Punit,NIkhil Jain and Sunil Rohiwal ")
  
    def _create_file(self, file_name=None):  
        if not file_name:
            self.feedback.speak("Please specify a filename.")
            return
        try:
            with open(file_name, 'w') as f:
                f.write(f"Created by voice command at {datetime.datetime.now()}")
            self.feedback.speak(f"File '{file_name}' created successfully")
        except Exception as e:
            self.feedback.speak(f"Error creating file: {str(e)}")
    

    def _exit_program(self):
        self.feedback.speak("Exiting the voice assistant. Goodbye!")
        print("Voice assistant exited by user command.")
        sys.exit(0)
            
    def _manual(self):
        """
        Dynamically print all available voice commands supported by the system.
        """
        self.feedback.speak("Printing all available commands--")

        command_map = {
            "shutdown": self._shutdown,
            "list file": self._list_file,
            "list formatted files": self._list_formatted_files,
            "list file permissions": self._list_file_permissions,
            "list hidden files": self._list_hidden_files,
            "current working directory": self._current_working_directory,
            "what is the date today": self._get_date,
            "what is the day today": self._get_day,
            "what is the time": self._get_time,
            "calendar": self._show_calendar,
            "what is the username": self._get_username,
            "create a random file": self._create_random_file,
            "go to home directory": self._go_to_home,
            "go to root directory": self._go_to_root,
            "go to my directory": self._go_to_user_home,
            "run ps": self._run_ps,
            "show network status": self._show_network,
            "delete a file": self._delete_file,
            "create a file": self._create_file,
            "open nano editor": self._open_nano,
            "open gedit editor": self._open_gedit,
            "open sublime editor": self._open_sublime,
            "what is the status and configuration of network": self._show_network_config,
            "make a new directory": self._make_directory,
            "list users": self._list_users,
            "list all users": self._list_users,
            "list user": self._list_users,
            "who created you": self._creator_info,
            "manual": self._manual ,
            "exit"  :self._exit_program
        }

        print("\n======= Manual: List of Supported Voice Commands =======")
        for idx, cmd in enumerate(command_map.keys(), 1):
            print(f"{idx}. {cmd}")
        print("========================================================")


    def _delete_file(self, file_name=None):
        """
        Delete a file with the specified name, providing user feedback.
        """
        if not file_name:
            self.feedback.speak('Run the command like this"delete a file file_name" or "remove a file file_name"' )
            return
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                self.feedback.speak(f"File '{file_name}' deleted successfully.")
                print(f"File '{file_name}' deleted successfully.")
            except PermissionError:
                self.feedback.speak(f"Permission denied to delete the file '{file_name}'.")
                print(f"Permission denied to delete the file '{file_name}'.")
            except Exception as e:
                self.feedback.speak(f"Error occurred while deleting the file: {str(e)}")
                print(f"Error occurred while deleting the file: {str(e)}")
        else:
            self.feedback.speak(f"File '{file_name}' not found.")
            print(f"File '{file_name}' not found.")
    
        _, ext = os.path.splitext(file_name)
        if not ext:
            self.feedback.speak("No file extension found. Please provide a valid filename with extension.")
            print("No file extension found.")
            return

        try:
            result = subprocess.run(["assoc", ext], shell=True, capture_output=True, text=True)
            output = result.stdout.strip()
            if output:
                print(output)
                self.feedback.speak(f"The file type for {ext} is: {output}")
            else:
                self.feedback.speak(f"No file type association found for {ext}.")
                print(f"No file type association found for {ext}.")
        except Exception as e:
            self.feedback.speak(f"Error getting file type: {str(e)}")
            print(f"Error getting file type: {str(e)}")



