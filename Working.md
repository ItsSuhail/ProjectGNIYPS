## Working
+ The program has basic socket functionalities.
+ To server first listens to the IP and PORT provided by the user.
+ We may forward the port using services like ngrok.
+ When first client joins the server, the address is appended to a list called "client list", and new thread "Management Thread" is initiated which lets the user control the communication between clients
+ As new clients join, a new thread "Receiver Thread" is created to log the messages sent by the client and the outputs of requests which were sent by the user
+ The management thread creates a prompt for the user, to type in requests/commands. To execute a command on a single or more than one clients,
  the user would type in the index of clients (w.r.t to client list) and seperated by "<|>" and write the command at the end

  Example: say we have 3 clients (say A,B,C), and their addresses are appended onto client list, if I want to execute a command for opening notepad on first two clients (A and B),
          I would type:
          ```
          0<|>1<|>notepad
          ```
          here 0 and 1 represent the index of A and B in the command list

+ If we have changed the server address to a new one, we may send a request to change the address to the latest one on the client side, to continue the communication.
+ If for some reason the server gets shutdown, the client would continue to connect to the address which it would request over a URL
  Example: if we host a server, and client A is connected to it. If the server is shutdown, the client will look for the address over a URL say xyz.com, and if it receives
          an address, it would try to connect to it. So if our server gets shutdown, we may host another one, and we can write the server address over a URL (say xyz.com) so
          that the client will get the new address and would connect to it.
