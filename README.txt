-----------------------------------------------------
Jarvis

Structure/functionalities:

Password for initiation

Initiation sequence:
	- master thread
	- communication thread
	- interpreter
	- ping thread

Ping thread:
	- regularly checks internet connection
	- pauses all processes until internet connection returns to strong
	- notifies Master thread to propagate weak-wifi-connection message to all clients

Interpreter:
	- given a set of databases, which are mutable, it interprets messages

Master thread
	- responsible for sending emergency notification
	- highest priority messenger

Communication thread
	- starts console, voice, mobile threads for communication
	- each thread is responsible for receiving messages, using Interpreter object
	to interpret the message, and sending back the results.


Client:

Connect to server
Password for initiation
Send/receive messages

-----------------------------------------------------
All messages are encrypted
-----------------------------------------------------