import socket as soos
import json
# nome_da_sala
# lista de softwares
# quantidade de lugares disponiveis
JsonToSend = [{
              "usuario": "Jooj",
              "function" : "userGeneralQuery"
}]




def driverTeste(port=8080, address="127.0.0.1"):
    with soos.socket(soos.AF_INET, soos.SOCK_STREAM) as sc:
        sc.connect((address, port))
        sc.sendall(json.dumps(JsonToSend[0]).encode("UTF-8"))
        print(sc.recv(1024).decode("UTF-8"))
        # sc.sendall(json.dumps(JsonToSend[1]).encode("UTF-8"))
        # print(sc.recv(1024).decode("UTF-8"))
        return 0

driverTeste()
