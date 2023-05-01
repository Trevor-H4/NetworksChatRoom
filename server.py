import socket
import threading

# Chat room project made by Trevor Hileman for CS4850. 4/15/23
# This is the server side of the program. Main is constantly listening for new connections and the thread is running the handler function. 
# The handler function takes care of all I/O of the program. It takes in the messages it receives from the client and determines what to do with them.
# The add_user function adds the username and password to the file after it checks to see if they already exists. If they do already exist, it returns 1. 
# This was developed and compiled on Python 3.11

class Clients: # clients class to make things a bit more manageable 
    clients = {}
    loggedIn = False
    clientOnline = False
    clientCount = 0

clientList = Clients() # create a new Clients object called clientList

ip = '127.0.0.1' # local host  
port = 16614 # port based on student ID number 

_user_file = open("users.txt", 'r') #open users file 
users = _user_file.readlines() # get users in var
_user_file.close() # close file 

def add_user(username, password): # this adds a user to the user file          
    _user_file = open("users.txt", 'r') # open users file 
    users = _user_file.readlines() # get users in var
    _user_file.close() # close file   

    user = "(" + username + ", " + password + ")\n" # correct formatting for user file 
    userTwo = "(" + username + ", " + password + ")"
    if user in users: # checks to see if username exists
        return 1 # return 1 if it exists 
    elif userTwo in users: # checks for username without newline
        return 1
    else:
        user = "(" + username + ", " + password + ")" # change user string back for better formatting 
        user_file = open("users.txt", 'a') # open user file for appending 
        user_file.write("\n"+user) # write the user string to the file 
        user_file.close() # close file, not needed anymore

def handler(client): # handles any input from client and sends out stuff back to client 
    while(True): # loop so server keeps running if it reaches a dead end 
        try: 
            clientMessage = (client.recv(1024).decode('ascii'))
            function = clientMessage.split(" ")[0] # sets this equal to the first word typed aka the function

            if (function == "login"): # if first word is login, this executes
                if (clientList.loggedIn == True): # cant login while already logged in
                    client.send("> User already logged in".encode('ascii'))
                    continue 

                else:
                    loginUsername = clientMessage.split(" ")[1] # if first word is login, second must be usernmae
                    loginPassword = clientMessage.split(" ")[2] # third word must be password
                    _user_file = open("users.txt", 'r') # open file for read only
                    for line in _user_file: # for loop to go through every line of file
                        if loginUsername in line: # if entered username is in current line of users.txt
                            if loginPassword in line: # if entered password is in current line of users.txt
                                print(loginUsername + " login.") # notify server succesful client login
                                clientList.loggedIn = True # change login status in class to true
                                client.send(("> Login confirmed").encode('ascii')) # let client know that login was succesful

                    if (clientList.loggedIn == False): # this would only be false if the user put in a username/password combo that didnt exist
                        client.send("> Denied. User name or password incorrect".encode('ascii'))    
                        continue

            elif (function == "newuser"): # if first word is new user, this executes 
                if (clientList.loggedIn == True): # cant create new user while logged into account
                    client.send("> User creation not allowed when logged in, please logout first".encode('ascii'))
                    continue
                else:                 
                    if len(clientMessage.split(" ")[1]) > 32: # username cant be longer than 32 characters 
                        client.send("> Username too long".encode('ascii'))
                        continue
                    elif len(clientMessage.split(" ")[1]) < 3: # username cant be shorter than 3 characters 
                        client.send("> Username too short".encode('ascii')) 
                        continue
                    elif len(clientMessage.split(" ")[2]) > 8: # password cant be longer than 8 characters 
                        client.send("> Password too long".encode('ascii'))
                        continue
                    elif len(clientMessage.split(" ")[2]) < 4: # password cant be shorter than 4 characters 
                        client.send("> Password too short".encode('ascii'))
                        continue
                    else:        
                        if add_user(clientMessage.split(" ")[1], clientMessage.split(" ")[2]) == 1: # adds user to file
                            client.send("> Denied. User account already exists".encode('ascii')) # notify client user already exists 
                            continue
                        else:
                            print("New user account created")
                            client.send("> New user account created. Please login.".encode('ascii')) # signals client that account creation successful
                            continue

            elif (function == "send"): # if first word is send, this executes 
                if (clientList.loggedIn == False): # client must be logged in to send message 
                    client.send("> Denied. Please login first.".encode('ascii'))
                    continue

                elif(len(clientMessage[1]) > 256): # message cant be over 256 chars
                    client.send("> Message cannot exceeed 256 characters".encode('ascii'))
                    continue

                else:
                    client.send(("> " + loginUsername + ": " + clientMessage[5:]).encode('ascii')) # send message to client 
                    print(loginUsername + ": " + clientMessage[5:]) # print message from client on server

            elif (function == "logout"): #if first word is logout, this executes 
                if (clientList.loggedIn == False): # client must be logged in to logout
                    client.send("> Not logged in, can't logout".encode('ascii'))
                    continue
                else: 
                    client.send(("> " + loginUsername + " left").encode('ascii'))
                    print(loginUsername + " logout.")
                    client.close() # close client connection
                    clientList.loggedIn = False # no one logged in anymore 
                    clientList.clientOnline = False # no one is online after only user logs out

            else: # in case user input doesnt follow correct format
                print("Invalid syntax received from client")
                client.send("> Invalid syntax".encode('ascii')) # let client know theyre syntax was invalid 
                continue
        except: # this is here to handle any expected errors 
            client.close()
            clientList.clientOnline = False
            clientList.loggedIn = False
            break 


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #internet socket 
    server.bind((ip, port)) # bind the server to ip and port

    print("My chat room server. Version One.\n\n")
    while True:
        server.listen() # server starts listening for new clients 
        client, address = server.accept() # accepts any client requesting to connect 

        if clientList.clientOnline == False:
            clientList.clientOnline = True
            print("Client connected.") # lets server know someone connected 
            thread = threading.Thread(target = handler,args = (client,)) # used a thread to help server stay alive if client leaves 
            thread.start()
        else: # for purpose of V1, only one client allowed at a time 
            print("Server at capacity") 
            client.send("> Server at capacity, dropping connection".encode('ascii'))
            client.close() # close client if server capacity is full 





