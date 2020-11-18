##########################################################
# This is the file where our server object is defined,as #
# well as its default values, protocols and everything   #
# else related to the main server structure.             #
##########################################################
from _thread import start_new_thread
import socket as soos
import databaseHandler as dh
import threading
import sys
import json


# all queries made by both the user and our admin
# can be summarized here. Each function is bound to a lambda
MAPPED_QUERIES = {
    "userGeneralQuery": dh.userGeneralQuery,
    # room editing
    "createSala": dh.createSala,
    "editSala": dh.editSala,
    "removeSala": dh.removeSala,
    # computer editing
    "createComputer": dh.createComputer,
    "removeComputer": dh.removeComputer,
    # software editing
    "createSoftware": dh.createSoftware,
    "removeSoftware": dh.removeSoftware,
    # check queries
    "salista": dh.salista,
    "computerList": dh.computerList,
    "softwareList": dh.softwareList,
    # delete all softwares
    "expungeSoftware": dh.expungeSoftware,
}

class Server:
    """
    Our main server class.
    --
    Attributes:
    ==========
    SocketTuple = Tuple
    Contains both the Default Address so it can be bound and default port

    isTCP = bool
    Defines our transport layer protocol in which the server will operate on
    isIPV4 = bool
    Defines our addressing protocol

    run = bool
    used as a way to control our multithreading

    DefaultUser = string
    default username

    MaximumClients = integer
    Way to define how many clients our application can serve at the same time
    """
    def __init__(self, port=8080, DA=""):
        """
        Single constructor for our server class
        --
        Arguments:
        ==========
        port = int
        Defines which port the socket will be bound

        DA = default address
        Defines our default address "has to be IPV4 or IPV6"
        """
        self.SocketTuple = (DA, port)
        self.isTCP = True
        self.isIPV4 = True
        self.run = True
        self.DefaultUser = "jooj"
        self.MaximumClients = 2
        self.lock_thread = threading.Lock()
        
    def parseString(self, StringToParse):
        """
        Parser for all requests that arrive, we'll always expect a JSON
        --
        Arguments:
        =========
        StringToParse = String
        Request sent by the client.
        """
        # first we load a json object
        try:
            JasonObject = json.loads(StringToParse)
        # if it was an invalid object
        except json.JSONDecodeError:
            JasonObject = None
        return JasonObject

    def serverSocket(self):
        """
        Probably the most important method for this class, forces the server to
        listen on an specific address
        --
        Important objects:
        =========
        sock = class socket
        Protocol in which all of our transport layer processes are abstracted
        """
        with soos.socket(soos.AF_INET if self.isIPV4 else soos.AF_INET6,
                         soos.SOCK_STREAM
                         if self.isTCP  else soos.SOCK_DGRAM) as sock:
            # every method needed in order to make the server functional before
            # our main loop should be placed here

            # connectDB will create the database if it doesn't exist
            if self.checkDB() != 0:
                print("Something is wrong with the database, please check it.")
                sys.exit()
            
            sock.bind(self.SocketTuple)
            sock.listen(self.MaximumClients)
            while True:
                SocketObject = sock.accept()
                print(f'Conectado com {SocketObject}')
                self.lock_thread.acquire()
                start_new_thread(self.mainLoop, SocketObject)
            # mainLoop receives a proper socket object AND an address tuple
            # any change related to adapting this program to multithreading
            # should just change the main loop and how a branching occurs
            # uncomment this if you wish to turn this program single thread
            # self.mainLoop(sock.accept())
            
    def checkDB(self):
        return dh.checkAllTables()
      
    def mainLoop(self, SocketObject, _):
        """
        Branching path for multithreading, here all the communication is done
        with a single client.
        """
        try:
            ConsSocketCommunication = SocketObject
            # parse string will parse the upcoming JSON string
            # and turn it into a proper JSON object
            Control = self.parseString(
                ConsSocketCommunication.recv(1024).decode("UTF-8"))
            if Control is None:
                self.sendObject(json.dumps({"state":"connected"}),
                                ConsSocketCommunication)
            elif Control.get("usuario") == self.DefaultUser:
                self.commonUserProcedure(ConsSocketCommunication, Control)
            elif Control.get("senha") is not None:
                if self.checkCredentials(Control) == []:
                    self.sendObject(ConsSocketCommunication,
                               "Credenciais não reconhecidas, tente novamente.")
                else:
                    self.admProcedure(ConsSocketCommunication, Control)
            else:
                # in case it's some attacker trying to snoop around
                self.sendObject(json.dumps(
                    {"error": "Your request doesn't comform with our standards"}), ConsSocketCommunication)
                
        except TypeError as err:
            print("Erro ao resgatar do database")
            print(err)
            self.sendObject(json.dumps(
                {"Error": "Our server has handled your request incorrectly, please try again later"}), ConsSocketCommunication)
        finally:
            print("Disconnected from client")
            self.lock_thread.release()
            
    def checkCredentials(self, Control):
        return dh.checkUser((Control.get("usuario"), Control.get("senha")))

    def sendObject(self, MessageOrRequest, SocketObject):
        ObjectToSend = MessageOrRequest.encode("UTF-8") # string to send
        ObjectToSendSize = len(ObjectToSend) # length in bytes of the above object
        # first we send information regarding the length of the string we're sending
        SocketObject.sendall(bytes(str(ObjectToSendSize), "UTF-8"))
        SocketObject.sendall(b'\n') # ending our connection 
        # then the object itself
        SocketObject.sendall(ObjectToSend)
        
    def commonUserProcedure(self, socketObject, Control):
        """
        Processes all queries requested by our common user.
        --
        Arguments:
        =========
        socketObject = socket
        Object of the socket class

        Control = String
        Parsed incoming json from a single client
        """
        self.sendObject(self.createResponseUser(Control), socketObject)
        
    def admProcedure(self, socketObject, Control):
        if Control.get("function") is not None:
            arglist = Control.get("arglist")
            if arglist is not None:
                adm_response = MAPPED_QUERIES.get(
                    Control.get("function"))(arglist) or "Database retornou null"
            else:
                adm_response = MAPPED_QUERIES.get(
                    Control.get("function"))() or "Database retornou null"
        self.sendObject(self.createResponseAdm(adm_response), socketObject)
        
    def createResponseAdm(self, response_to_transform):
        return json.dumps(
            {"database_response": response_to_transform})
        
    def createResponseUser(self, Control):
        """
        This method defines the single response that'll be given to our user.
        --
        Control = String
        Parsed incoming json from a single client
        """
        dictionary_to_send = {} # this is going to be converted afterwards
        # gets all rooms
        for lista_salas in MAPPED_QUERIES.get(Control.get("function", None))(1):
            dictionary_to_send[lista_salas[0]] = {
                "hora_fechamento": lista_salas[1],
                "lista_computadores": {},
                "lista_softwares": []}

        # all computers
        for lista_computadores in MAPPED_QUERIES.get(
                Control.get("function", None))(2):
            dictionary_to_send[lista_computadores[0]]["lista_computadores"][lista_computadores[1]] = {
            "pos_x":lista_computadores[2],
                "pos_y":lista_computadores[3],
                "em_uso": lista_computadores[4]}
        # all software pieces with no doubled items
        for lista_soft in MAPPED_QUERIES.get(
                Control.get("function", None))(None):
            dictionary_to_send[lista_soft[0]]["lista_softwares"].append(
                lista_soft[1])
        return json.dumps(dictionary_to_send)
