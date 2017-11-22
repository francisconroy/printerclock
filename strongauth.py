import os
import hashlib
import crypt

# How does it work?
# The system operates on a secure method of calculation of one time keys
# There are two pieces of information which are shared:
# a. User password
# b. Shared seed
# Login process
# Client prepares first auth hash by taking
# auth_hash = sha256(shared_seed+user_password_hash+time_stamp(UNIX_SECONDS))
# Client stores a new seed sha256(shared_seed+user_password_hash)
# Client sends auth_hash in plaintext with username (hash?)
# Server looks up username
# Server generates possible hashes to match
# server_hash = sha256(shared_seed+user_password_hash+time_stamp(UNIX_SECONDS) (range T-10s, T+10s)
# if the server matches one of the 20 hashes, the door will open
# if door will open the new shared_seed is saved as (shared_seed+user_password)

## OR
## generate hash of user password, encrypt using AES256, send to server
# Server decrypts and then compares hash to hashes stored in DB


## OR
# encrypt hash of user password + timestamp
# decrypt on server
# verify timestamp and hash





class AuthData(object):
    def __init__(self, name):
        self.username = name
        self.pin = None

    def addPin(self, pin):
        if len(str(int(pin))) >= 4:
            self.pin = int(pin)
            print("{}:Meets requirements".format(self.username))
        else:
            print("{}:Pin does not meet requirements".format(self.username))
            print("{}:Pin should be 4 or more digits".format(self.username))
            raise Exception


class ConfigFile(object):
    def __init__(self, filepath):
        self.users = []
        self.filepath = filepath
        if os.path.exists(filepath):
            with open(filepath) as openfile:
                for line in openfile:
                    splitline = line.split(',')
                    newuser = DoorUser(splitline[0])
                    newuser.addPin(splitline[1])
                    self.users.append(newuser)

    def writefile(self):
        with open(self.filepath, mode='w') as writefile:
            for user in self.users:
                writefile.write("{},{}\n".format(user.username, user.pin))

    def list_users(self):
        list = []
        for user in self.users:
            list.append(user.username)
        return list

    def list_pins(self):
        list = []
        for user in self.users:
            list.append(user.pin)
        return list

    def getuserfrompin(self, pin):
        for user in self.users:
            if user.pin == int(pin):
                return user

    def getuserfromname(self, name):
        for user in self.users:
            if user.username == name:
                return user

    def add_user(self, name, pin):
        if name not in self.list_users():
            newuser = DoorUser(name)
            try:
                newuser.addPin(pin)
            except:
                "User was not added!"
                return
            self.users.append(newuser)
            self.writefile()
        else:
            print("User is already in the database")

    def remove_user(self, name):
        self.users.remove(self.getuserfromname(name))
        self.writefile()

    def change_pin(self, name, pin):
        for user in self.users:
            if user.name == name:
                user.pin = user.addPin(pin)
            else:
                print("User is not in the list!")

    def print_users(self):
        print("USERS ARE:")
        for user in self.users:
            print (str(user.username) + ":" + str(user.pin))

    def cleardata(self):
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
        self.users = []

    def checkpin_from_dict(self, dict):
        return self.checkpin(dict['pin_num'])

    def checkpin(self, checkpin):
        if int(checkpin) in self.list_pins():
            user = self.getuserfrompin(int(checkpin))
            print("Opening door: welcome {}".format(user.username))
            return 1, user.username
        else:
            print("Sorry you aren't welcome here")
            return 0, ""


## Testing
def main():
    # configfile.cleardata()
    # configfile.print_users()
    # configfile.checkpin(7896)
    # configfile.checkpin()
    configfile = ConfigFile("userdata.txt")
    print ("Welcome to the administration interface for auth module V1.0")
    while (1):
        command = raw_input()
        if command == 'n':
            new_username = raw_input("Please enter a username:")
            new_pin = raw_input("Please enter a pin")
            configfile.add_user(new_username, new_pin)
        if command == 'r':
            user_to_remove = raw_input("Remove user:")
            configfile.remove_user(user_to_remove)
        if command == 'l':
            while (1):
                checkpin = raw_input("What's your pin?")
                if checkpin != '':
                    configfile.checkpin(checkpin)
                else:
                    break
        if command == 'e':
            break
        if command == 'list':
            configfile.print_users()
        else:
            print("You can add_new(n), list(list) or login(l)")


if __name__ == "__main__":
    main()
