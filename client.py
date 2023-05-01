import socket
import time

# Chat room project made by Trevor Hileman for CS4850. 4/15/23
# You boot up this client program after launching the server and the client automatically connects to the server
# Once this client is connected to the server, all the messages you send are sent to the server, interpreted, and dealt with accordingly. 
# If the client receives "You have been logged out" or "Server is full" from the server then the connection is closed
# Developed and compiled on Python 3.11

ip = '127.0.0.1' # local host 
port = 16614 # port based on student ID number 
online = True 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # internet socket 
client.connect((ip, port)) # connect to the server 

print("My chat room client. Version One.\n\n")
print("Welcome to the chat room!\n")
print("Here are the commands: \n")
print("1. login USERNAME PASSWORD\n")
print("2. newuser USERNAME PASSWORD (username must be 3-32 characters, password must be 4-8 characters)\n")
print("3. send MESSAGE (1-256 characters) \n")
print("4. logout\n")
print("Replace the capitalized words in the command with your specific input, do NOT include the number\n")

while(online):
        message = input("> ") # gets input from user
        function = message.split(" ")

        if (function[0] == "login"):
             if len(function) != 3: # login has to be 3 words 
                print("Invalid syntax, login must command must contain 3 words")
                continue
             
             client.send(message.encode('ascii'))
        elif (function[0] == "newuser"): # new user function
             if len(function) != 3:
                print("Invalid syntax, newuser must command must contain 3 words") # new user has to be 3 words 
                continue

             elif len(message.split(" ")[1]) > 32: # username cant be longer than 32 characters 
                client.send("Username too long".encode('ascii'))
                continue
             
             elif len(message.split(" ")[1]) < 3: # username cant be shorter than 3 characters 
                client.send("Username too short".encode('ascii')) 
                continue
             
             elif len(message.split(" ")[2]) > 8: # password cant be longer than 8 characters 
                client.send("Password too long".encode('ascii'))
                continue
             
             elif len(message.split(" ")[2]) < 4: # password cant be shorter than 4 characters 
                client.send("Password too short".encode('ascii'))
                continue
             
             client.send(message.encode('ascii')) # sends the input to the server
             

        elif (function[0] == "send"): # send function
            if(len(message[1]) > 256): # message cant be over 256 chars
                print("Message cannot exceeed 256 characters")
                continue

            client.send(message.encode('ascii')) # send the message if passes all checks 

        elif (function[0] == "logout"):
             client.send(message.encode('ascii')) # sends the input to the server
             logMessage = (client.recv(1024).decode('ascii'))
             print(logMessage) # print final goodbye messagae
             client.close() # close client
             online = False # not online anymore
             break
        else: # executes if user does not use right command 
             print("Invalid syntax")
             continue
        
        serverMessage = (client.recv(1024).decode('ascii')) # decodes any messages received from server

        if serverMessage.split(" ")[0] == "Server is full": # if server is full 
            client.close() # close connection
            online = False

        print(serverMessage) # print message received from server 

client.close() # close connection

