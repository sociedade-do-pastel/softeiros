import socket as soos
import databaseHandler as dh
from datetime import datetime
import sys
import json
MAPPED_QUERIES = {
    "userGeneralQuery": dh.userGeneralQuery,
    None : lambda: json.encode({"error":1}),
}

class Servidor:
    def __init__(self, port=8080, DA=""):
        self.SocketTuple = (DA, port)
        self.isTCP = True
        self.isIPV4 = True
        self.run = True
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
            if self.checkDB() != 0:
                print("Something is wrong with the database, please check it.")
                sys.exit()
                
            sock.bind(self.SocketTuple)
            sock.listen(self.MaximumClients)
            # mainLoop receives a proper socket object AND an address tuple
            # any change related to adapting this program to multithreading
            # should just change the main loop and how a branching occurs 
            self.mainLoop(sock.accept())
            
    def checkDB(self):
        return dh.checkAllTables()
        
    def mainLoop(self, SocketObject):
        ConsSocketCommunication = SocketObject[0]
        # Socket object index 0 gets the socket itself,
        # whereas 1 returns our client's address
        print(SocketObject[1])
        # first, we must check if the user is an administrator
        # or a common user
        Control = self.parseString(ConsSocketCommunication.recv(1024).decode("UTF-8"))
        if Control and Control.get("usuario") == self.DefaultUser:
            self.commonUserProcedure(ConsSocketCommunication, Control)
        elif Control.get("senha") is not None:
            self.admProcedure(ConsSocketCommunication, Control)
        else:
            ConsSocketCommunication.sendall('''
            We've assumed that you're an attacker, comrade,
            so we're answering with this message! 
            '''.encode("UTF-8"))
               
    def commonUserProcedure(self, socketObject, Control):
        # first we send all of our software list
        socketObject.sendall(self.JsonFyAndConvertToString(Control))
        
    def admProcedure(self, socketObject, Control):
        pass
    
    def JsonFyAndConvertToString(self, control):
        dictionary_to_send = {}
        for lista_salas in MAPPED_QUERIES.get(control.get("function", None))(1):
            dictionary_to_send[lista_salas[0]] = {"hora_fechamento": lista_salas[1],
                                                  "lista_computadores": {}}

        for lista_computadores in MAPPED_QUERIES.get(control.get("function", None))(2):
            dictionary_to_send[lista_computadores[0]]["lista_computadores"][lista_computadores[1]] = {
            "pos_x":lista_computadores[2],
            "pos_y":lista_computadores[3]}
            
        return json.dumps(dictionary_to_send).encode("UTF-8")
