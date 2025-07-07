

import re
import json

class CommandProcessor:
    def __init__(self, config_path):
        self.commands = self._load_commands(config_path)
        
    def _load_commands(self, config_path):
        with open(config_path, 'r') as f:
            return json.load(f)

    def process_command(self, text):
        if not text:
            return None, None, None

        text = text.lower().strip()
        args = {}

        # Regex pattern: create directory
        dir_match = re.search(r'make a new directory (?:called |named )?(\w+)', text)
        if dir_match:
            args['dir_name'] = dir_match.group(1)
            print(f"DEBUG: Regex matched 'make a new directory', extracted dir_name = '{args['dir_name']}'")
            return "make a new directory", self.commands.get("make a new directory"), args

        # Regex pattern: create file
        file_match = re.search(r'create a file (?:called |named )?([\w\-]+\.\w+)', text)
        if file_match:
            args['file_name'] = file_match.group(1)
            print(f"DEBUG: Regex matched 'create a file', extracted file_name = '{args['file_name']}'")
            return "create a file", self.commands.get("create a file"), args
        
        match = re.match(r'(remove|delete) a file (.+)', text)
        if match:
            args['file_name'] = match.group(2).strip().replace(" ", "_")
            cmd_key = "remove a file" if "remove" in match.group(1) else "delete a file"
            return cmd_key, self.commands.get(cmd_key), args

        match = re.match(r'tell me (the )?file type( of)? (.+)', text)
        if match:
                args['file_name'] = match.group(3).strip()
                return "tell me the file type", self.commands.get("tell me the file type"), args
                # Check for exact match
                for cmd, details in self.commands.items():
                    if text == cmd.lower():
                        print(f"DEBUG: Exact match found for command '{cmd}'")
                        return cmd, details, args

        # Fuzzy matching
        best_match = None
        best_score = 0
        for cmd, details in self.commands.items():
            cmd_lower = cmd.lower()

            if cmd_lower in text:
                score = len(cmd_lower) / len(text)
                print(f"DEBUG: Partial match: '{cmd}' in text → score = {score:.2f}")
                if score > best_score:
                    best_match = cmd
                    best_score = score

            elif text in cmd_lower:
                score = len(text) / len(cmd_lower)
                print(f"DEBUG: Partial match: text in '{cmd}' → score = {score:.2f}")
                if score > best_score:
                    best_match = cmd
                    best_score = score

        if best_match and best_score > 0.9:
            print(f"DEBUG: Fuzzy match found for '{best_match}' with score = {best_score:.2f}")
            return best_match, self.commands[best_match], args

        print("DEBUG: No matching command found.")
        return None, None, None
