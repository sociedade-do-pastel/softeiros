import socket as soos
import json
# nome_da_sala
# lista de softwares
# quantidade de lugares disponiveis
FirstJson = {"usuario": "Jooj"}

def driverTeste(port=8080, address="127.0.0.1"):
    with soos.socket(soos.AF_INET, soos.SOCK_STREAM) as sc:
        sc.connect((address, port))
        sc.sendall(json.dumps(JsonToSend).encode("UTF-8"))

        return 0

driverTeste()
