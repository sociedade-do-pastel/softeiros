import psycopg2
# sysadmin will have to create this database
# in case it doesn't exist
DATABASE_NAME = "AvailAble"

DATABASE_ADDRESS = "127.0.0.1"
DATABASE_PORT = "5432"

# external queries for creating our
# main tables
SALINHA_CREATE_FILENAME = "createSalinha.sql"
USERS_CREATE_FILENAME = "createUser.sql"
COMPUTADOR_CREATE_FILENAME = "createComputer.sql"
SOFTWARES_CREATE_FILENAME = "createSoos.sql"

def createConnection(user="postgres"):
    return psycopg2.connect(user = user,
                            host = DATABASE_ADDRESS,
                            port = DATABASE_PORT,
                            database = DATABASE_NAME)

def initDatabase():
    pass
def stablishConnection():
    pass
def checkTables(table):
    con = createConnection()
    cursor = con.cursor()
    cursor.execute("SELECT EXISTS(SELECT * from information_schema.tables WHERE table_name=%s)",
                   (table, ))
    wasFound = cursor.fetchone()[0]
    cursor.close()
    con.close()
    return wasFound

def createTable(table_name=SALINHA_CREATE_FILENAME):
    con = createConnection()
    cursor = con.cursor()
    with open(table_name, "r") as arquivito:
        cursor.execute(arquivito.read())
    con.commit()
    cursor.close()
    con.close()
    
