#############################################################################
# Assignment #9
# Program: Authenticate.py
# Author: Oliver Tipping
# Date: July 29, 2023
#############################################################################
import time

def check_unique_first_column(target_word):
    with open("login.txt", 'r') as file:
        for line in file:
            # Split the line by spaces and extract the first word
            first_column_word = line.strip().split()[0]
            
            # Compare the first word with the target word
            if first_column_word == target_word:
                return False  # Not allowed if there is a match
    
    return True  # Allowed if no match is found

def check_credentials(username, password):
    with open("login.txt", "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:  # Ensure there are three columns
                file_username, file_password, value = parts
                if file_username == username and file_password == password:
                    return value
    
    return None

def update_user_credentials(username, new_password, new_value):
    updated_lines = []

    if(check_unique_first_column(username) == True):
        return False
    else:
        with open("login.txt", "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:  # Ensure there are three columns
                    file_username, _, _ = parts
                    if file_username == username:
                        updated_lines.append(f"{username} {new_password} {new_value}\n")
                    else:
                        updated_lines.append(line)

        # Write the updated content back to the file
        with open("login.txt", "w") as file:
            file.writelines(updated_lines)

        return True

def delete_user_credentials(username):
    updated_lines = []

    if(check_unique_first_column(username) == True):
        return False
    else:
        with open("login.txt", "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:  # Ensure there are three columns
                    file_username, _, _ = parts
                    if file_username != username:
                        updated_lines.append(line)

        # Write the updated content back to the file
        with open("login.txt", "w") as file:
            file.writelines(updated_lines)

        return True

while True:
    with open("application.txt", "r+") as applicationfile, open("login.txt", "r+") as loginFile:
        loginCommand = applicationfile.read().split()
        if(len(loginCommand) == 5 and loginCommand[0] == "Authenticate" and loginCommand[1] == "New"):
            if(check_unique_first_column(loginCommand[2])):
                loginFile.seek(0, 2)
                loginFile.write(loginCommand[2] + " " + loginCommand[3] + " " + loginCommand[4] + "\n")
                applicationfile.seek(0)
                applicationfile.truncate()
                applicationfile.write("Authenticate Complete")
            else:
                applicationfile.seek(0)
                applicationfile.truncate()
                applicationfile.write("Authenticate Failed")

        elif(len(loginCommand) == 4 and loginCommand[0] == "Authenticate" and loginCommand[1] == "Login"):
            permissions = check_credentials(loginCommand[2],loginCommand[3])
            if(permissions == None):
                applicationfile.seek(0)
                applicationfile.truncate()
                applicationfile.write("Authenticate Failed")
            else:
                applicationfile.seek(0)
                applicationfile.truncate()
                applicationfile.write("Authenticate Complete " + permissions)

        elif(len(loginCommand) == 5 and loginCommand[0] == "Authenticate" and loginCommand[1] == "Reset"):
            if(update_user_credentials(loginCommand[2], loginCommand[3], loginCommand[4])):
                applicationfile.seek(0)
                applicationfile.truncate()
                applicationfile.write("Authenticate Complete")
            else:
                applicationfile.seek(0)
                applicationfile.truncate()
                applicationfile.write("Authenticate Failed")

        elif(len(loginCommand) == 3 and loginCommand[0] == "Authenticate" and loginCommand[1] == "Delete"):
            if(delete_user_credentials(loginCommand[2])):
                applicationfile.seek(0)
                applicationfile.truncate()
                applicationfile.write("Authenticate Complete")
            else:
                applicationfile.seek(0)
                applicationfile.truncate()
                applicationfile.write("Authenticate Failed")

    time.sleep(1)
    
