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
    QUERY_TO_MAKE = "SELECT EXISTS(SELECT * from information_schema.tables WHERE table_name=%s)"
    return genericGetQuery(QUERY_TO_MAKE, table)[0][0]

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

def getAllSoftware():
    QUERY_TO_MAKE = "SELECT DISTINCT ON (1) nome_software FROM public.softwares_disp"
    return [soft[0] for soft in genericGetQuery(QUERY_TO_MAKE, ())]
   
    # now I'll have to return a json 

def genericDestructiveQuery(QUERY_TO_MAKE, args):
    with createConnection() as con:
        with con.cursor() as cursor:
            try:
                cursor.execute(QUERY_TO_MAKE, tuple(args))
                con.commit()
            except psycopg2.Error as err:
                print(err)
def genericGetQuery(QUERY_TO_MAKE, args):
    with createConnection() as con:
        with con.cursor() as cursor:
            try:
                cursor.execute(QUERY_TO_MAKE, tuple(args))
                return cursor.fetchall()
            except psycopg2.Error as err:
                print(err)

        
def createSala(args):
    QUERY_TO_MAKE = '''INSERT INTO public.sala
                       (nome_sala, hora_fechamento, ip_sala)
                       VALUES (%s, %s, %s)'''
    genericDestructiveQuery(QUERY_TO_MAKE, args)

               
def removeSala(nome_sala):
    QUERY_TO_MAKE = '''DELETE
                       FROM public.sala
                       WHERE nome_sala=%s'''
    genericDestructiveQuery(QUERY_TO_MAKE, nome_sala)


def createComputer(args):
    QUERY_TO_MAKE = '''INSERT INTO public.computador
                       (nome_sala, pos_x, pos_y)
                       VALUES
                       (%s, %s, %s)'''
    genericDestructiveQuery(QUERY_TO_MAKE, args)

def createSoftware(args):
    QUERY_TO_MAKE = '''INSERT INTO public.softwares_disp
                       (nome_software, id_computador)
                       VALUES
                       (%s, %s)'''
    genericDestructiveQuery(QUERY_TO_MAKE, args)

def editSala(args):

    QUERY_TO_MAKE = '''UPDATE public.sala SET
                       hora_fechamento=COALESCE(%s, hora_fechamento),
                       ip_sala=COALESCE(%s, ip_sala),
                       WHERE nome_sala=%s
                   '''

    genericDestructiveQuery(QUERY_TO_MAKE, args)
    
def removeComputer(args):
    QUERY_TO_MAKE = '''DELETE
                       FROM public.computador
                       WHERE id_computador=%s'''
    genericDestructiveQuery(QUERY_TO_MAKE, args)
    
def removeSoftware(args):
    QUERY_TO_MAKE = '''DELETE
                       FROM public.softwares_disp
                       WHERE (id_computador, nome_software) = (%s, %s)'''
    genericDestructiveQuery(QUERY_TO_MAKE, args)
    
def userGeneralQuery(args):
    if args == 1:
        QUERY_TO_MAKE = '''SELECT sl.nome_sala, to_char(hora_fechamento, 'HH24:MI')
        FROM public.sala AS sl '''
    elif args == 2:
        QUERY_TO_MAKE = '''SELECT nome_sala, comp.id_computador, pos_x, pos_y
        FROM public.sala AS sl
        JOIN public.computador AS comp USING(nome_sala)'''
    return genericGetQuery(QUERY_TO_MAKE, ())

