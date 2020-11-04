import databaseHandler as dh
import sys

def getAllInput(iterations):
    argList = []
    print("1 - Arg value ; 2 - Arg type, please separate it with a whitespace")
    while iterations > 0:
        try:
            ArgValue, ArgType = input().split()
            if ArgType == "int":
                ArgValue = int(ArgValue)
            elif ArgType == "float":
                ArgValue = float(ArgValue)
        except ValueError:
            ArgValue = None
        finally:
            argList.append(ArgValue)
            iterations -= 1
    return argList

dic = {
    1 : dh.getAllSoftware,
    2 : lambda:dh.createSala(getAllInput(3)),
    3 : lambda:dh.removeSala(getAllInput(1)),
    4 : lambda:dh.editSala(getAllInput(3)),
    5 : lambda:dh.createComputer(getAllInput(3)),
    6 : lambda:dh.removeComputer(getAllInput(1)),
    7 : lambda:dh.createSoftware(getAllInput(2)),
    8 : lambda:dh.removeSoftware(getAllInput(2)),
    9 : dh.checkAllTables,
    10 : sys.exit,
}
def main():
    escolha = int(input('''Operacao desejada
                       1 - Pegar lista de softwares
                       === SALA == 
                       2 - Criar nova sala
                       3 - Remover Sala
                       4 - Editar Sala
                       === Computador === 
                       5 - Adicionar Computador
                       6 - Remover Computador 
                       === Software ===
                       7 - Adicionar software 
                       8 - Remover software
                       == Checking ==
                       9 - Checar se tabelas existem e criar\n'''))
    
    print(dic.get(escolha, 10)())
main()