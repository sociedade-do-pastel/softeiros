import socket as soos
import json
# nome_da_sala
# lista de softwares
# quantidade de lugares disponiveis
JsonToSend = {
              "usuario": "jooj",
              "function" : "userGeneralQuery"
}

AdmJson = {
    "usuario" : "Carlos",
    "senha"   : "senha_secreta",
    "function": "createSala",
    "arglist" : ["K301", "19:10", "192.168.0.2"],
}

def driverTeste(port=8080, address="127.0.0.1"):
    with soos.socket(soos.AF_INET, soos.SOCK_STREAM) as sc:
        sc.connect((address, port))
        sc.sendall(json.dumps(JsonToSend).encode("UTF-8"))
        print(sc.recv(1024).decode("UTF-8"))
        # sc.sendall(json.dumps(JsonToSend[1]).encode("UTF-8"))
        # print(sc.recv(1024).decode("UTF-8"))
        return 0

driverTeste()
