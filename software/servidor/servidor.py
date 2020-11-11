##########################################################
# This is the file where our server object is defined as #
# well as its default values, protocols and everything   #
# else.                                                  #
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
    "salista": None,
    "computerList": None,
    "softwareList": None,
}

class Servidor:
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
            # self.mainLoop(sock.accept())
            
          
    def checkDB(self):
        return dh.checkAllTables()
      
    def mainLoop(self, SocketObject, _):
        """
        Branching path for multithreading, here all the communication is done
        with a single client.
        """
        print(SocketObject)
        try:
            ConsSocketCommunication = SocketObject
            # Socket object index 0 gets the socket itself,
            # whereas 1 returns our client's address
            # first, we must check if the user is an administrator
            # or a common user
            Control = self.parseString(
                ConsSocketCommunication.recv(1024).decode("UTF-8"))
            if Control and Control.get("usuario") == self.DefaultUser:
                self.commonUserProcedure(ConsSocketCommunication, Control)
            elif Control.get("senha") is not None:
                if self.checkCredentials(Control) == []:
                    self.sendError(ConsSocketCommunication,
                               "Credenciais não reconhecidas, tente novamente.")
                else:
                    self.admProcedure(ConsSocketCommunication, Control)
            else:
                # in case it's some attacker trying to snoop around
                ConsSocketCommunication.sendall('''
                Your request doesn't comform with our 
                request standards, please reformat.
                '''.encode("UTF-8"))
        except TypeError as err:
            print("Erro ao resgatar do database")
            print(err)
            SocketObject.sendall(
                json.dumps({"Error": '''Our server has handled your request
                incorrectly, please try again later'''}).encode("UTF-8"))

        finally:
            SocketObject.sendall("END".encode("UTF-8"))
            self.lock_thread.release()
            
    def checkCredentials(self, Control):
        return dh.checkUser((Control.get("usuario"), Control.get("senha")))

    def sendError(self, SocketObject, ErrorMessage):
        SocketObject.sendall(ErrorMessage.encode("UTF-8"))

        
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
        # first we send all of our software list
        socketObject.sendall(self.createResponseUser(Control))
        # then we finalize our message with a literal uppercase END
       
    def admProcedure(self, socketObject, Control):
        if Control.get("arglist") is not None and Control.get("function") is not None:
            adm_response = MAPPED_QUERIES.get(
                Control.get("function"))(Control.get("arglist"))
            socketObject.sendall(self.createResponseAdm(adm_response))
        else:
            adm_error_message = f'''Usuario {Control.get("usuario")} cadastrado,
            porem query nao compreendido'''
            self.sendError(socketObject, adm_error_message)
    def createResponseAdm(self, response_to_transform):
        return json.dumps(
            {"database_response": response_to_transform}).encode("UTF-8")
        
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
            "pos_y":lista_computadores[3]}
        # all software pieces with no doubled items
        for lista_soft in MAPPED_QUERIES.get(
                Control.get("function", None))(None):
            dictionary_to_send[lista_soft[0]]["lista_softwares"].append(
                lista_soft[1])
        return json.dumps(dictionary_to_send).encode("UTF-8")
