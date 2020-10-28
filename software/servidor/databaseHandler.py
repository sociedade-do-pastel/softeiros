import psycopg2

# sysadmin will have to create this database
# in case it doesn't exist
DATABASE_NAME = "AvailAble"

DATABASE_ADDRESS = "127.0.0.1"
DATABASE_PORT = "5432"

# external queries for creating our
# main tables
DicFilenames = {
    "usuario" : "./createUser.sql",
    "sala": "./createSalinha.sql",
    "computador": "./createComputer.sql",
    "softwares_disp": "./createSoos.sql",
}

def createConnection(user="postgres"):
    return psycopg2.connect(user = user,
                            host = DATABASE_ADDRESS,
                            port = DATABASE_PORT,
                            database = DATABASE_NAME)
def checkTables(table):
    with createConnection() as con:
        with con.cursor() as cursor:
            cursor.execute("SELECT EXISTS(SELECT * from information_schema.tables WHERE table_name=%s)",
                           (table, ))
            wasFound = cursor.fetchone()[0]
            return wasFound

def checkAllTables():
    with createConnection() as con:
        with con.cursor() as cursor:
            try:
                for values in DicFilenames.values():
                    with open(values, "r") as arquivito:
                        cursor.execute(arquivito.read())
            except IOError as err:
                print(err)
                return 1
            except psycopg2.Error as err:
                print(err)
                return 2
            con.commit()
        return 0

def getAllSoftware(*args):
    with createConnection() as con:
        with con.cursor() as cursor:
            # all software available should be returned here, no duplicates
            cursor.execute("SELECT DISTINCT ON (1) nome_software FROM public.softwares_disp")
            software_list = []
            for soft in cursor.fetchall():
                software_list.append(soft[0])
            # now I'll have to return a json 
            
def criarSala(*args):
    QUERY_TO_MAKE = "INSERT INTO public.sala (nome_sala, hora_fechamento, ip_sala, qtd_lugares_disp) VALUES (%s, %s, %s, %s)"
    with createConnection() as con:
        with con.cursor() as cursor:
            print(args)
            try:
                cursor.execute(QUERY_TO_MAKE, args)
            except psycopg2.Error as err:
                print(err)
               


    
