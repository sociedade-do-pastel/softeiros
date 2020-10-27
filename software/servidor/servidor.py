import socket as soos
import databaseHandler as dh
import sys
import json

class Servidor:
    def __init__(self, port=8080, DA=""):
        self.SocketTuple = (DA, port)
        self.isTCP = True
        self.isIPV4 = True
        self.run = True
        self.UserTableName = "Usuarios"
        self.RoomsTableName = "Salinhas"
        self.DefaultUser = "Jooj"
        self.MaximumClients = 2

    def parseString(self, StringToParse):
        # first we load a json object
        try:
            JasonObject = json.loads(StringToParse)
        # if it was an invalid object
        except json.JSONDecodeError:
            JasonObject = None
        return JasonObject
    
    def makeResponse(self, QueryToResolveInJason):
        print(QueryToResolveInJason)
        return json.dumps(QueryToResolveInJason)
    
    def serverSocket(self):
        with soos.socket(soos.AF_INET if self.isIPV4 else soos.AF_INET6,
                         soos.SOCK_STREAM if self.isTCP  else soos.SOCK_DGRAM) as sock:
            # every method needed in order to make the server functional before
            # our main loop should be placed here

            # connectDB will create the database if it doesn't exist
            self.connectDB(self.UserTableName, self.RoomsTableName)
            
            sock.bind(self.SocketTuple)
            sock.listen(self.MaximumClients)
            # mainLoop receives a proper socket object AND an address tuple
            # any change related to adapting this program to multithreading
            # should just change the main loop and how a branching occurs 
            self.mainLoop(sock.accept())
            
    def connectDB(self, *args):
        for tables_to_check in args:
            if not dh.checkTables(tables_to_check):
                dh.createTable(tables_to_check)
            
    def mainLoop(self, SocketObject):
        ConsSocketCommunication = SocketObject[0]
        # Socket object index 0 gets the socket itself,
        # whereas 1 returns our client's address
        print(SocketObject[1])
        # first, we must check if the user is an administrator
        # or a common user
        Control = self.parseString(ConsSocketCommunication.recv(1024).decode("UTF-8"))
        if Control and Control.get("usuario") == self.DefaultUser:
            self.commonUserProcedure(ConsSocketCommunication)
        elif Control.get("senha") is not None:
            self.admProcedure(ConsSocketCommunication, Control)
        else:
            ConsSocketCommunication.sendall('''
            We've assumed that you're an attacker, comrade,
            so we're answering with this message! 
            '''.encode("UTF-8"))
               
        def commonUserProcedure(self, socketObject):
            # first step
            socketObject.sendall(None) # first we send all of our software list
            # second step
            socketObject.recv(1024)    # then we receive a query about available softwares and seats
            socketObject.sendall(None) # answer it with every room that is available
            # comm is ended (probably from their side)
        def admProcedure(self, socketObject):
            pass 
