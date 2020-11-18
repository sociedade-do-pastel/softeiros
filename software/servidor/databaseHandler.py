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

def genericDestructiveQuery(QUERY_TO_MAKE, args):
    '''
    This procedure MODIFIES the database.
    The responsible administrator should
    only call it when needed.
    ---
    QUERY_TO_MAKE: str
    String containing the query to pass to
    the database
    '''
    with createConnection() as con:
        with con.cursor() as cursor:
            try:
                cursor.execute(QUERY_TO_MAKE, tuple(args))
                con.commit()
            except psycopg2.Error as err:
                print(err)

def genericGetQuery(QUERY_TO_MAKE, args):
    '''
    This procedures takes any generic query
    that does not modify our database.
    ---
    QUERY_TO_MAKE: str
    String containing the query to pass to
    the database
    '''
    with createConnection() as con:
        with con.cursor() as cursor:
            try:
                cursor.execute(QUERY_TO_MAKE, tuple(args))
                return cursor.fetchall()
            except psycopg2.Error as err:
                print(err)


# gotta unify all of these later
def checkUser(args):
    QUERY_TO_MAKE = '''SELECT id_user
                       FROM public.usuario
                       WHERE 
                       nome_usuario=%s AND
                       senha_usuario = crypt(%s, senha_usuario)'''
    return genericGetQuery(QUERY_TO_MAKE, args)

    
def createUser(args):
    QUERY_TO_MAKE = '''INSERT INTO public.usuario
                       (nome_usuario, senha_usuario)
                       VALUES
                       (%s, crypt(%s, gen_salt(\'bf\')))'''
    return genericDestructiveQuery(QUERY_TO_MAKE, args)
    
def removeUser(args):
    QUERY_TO_MAKE = '''DELETE FROM public.usuario
                       WHERE id_user=%s'''
    return genericDestructiveQuery(QUERY_TO_MAKE, args)
    
def createSala(args):
    QUERY_TO_MAKE = '''INSERT INTO public.sala
                       (nome_sala, hora_fechamento, ip_sala)
                       VALUES (%s, %s, %s)'''
    return genericDestructiveQuery(QUERY_TO_MAKE, args)

               
def removeSala(nome_sala):
    QUERY_TO_MAKE = '''DELETE
                       FROM public.sala
                       WHERE nome_sala=%s'''
    return genericDestructiveQuery(QUERY_TO_MAKE, nome_sala)


def createComputer(args):
    QUERY_TO_MAKE = '''INSERT INTO public.computador
                       (nome_sala, pos_x, pos_y)
                       VALUES
                       (%s, %s, %s)'''
    return genericDestructiveQuery(QUERY_TO_MAKE, args)

def createSoftware(args):
    QUERY_TO_MAKE = '''INSERT INTO public.softwares_disp
                       (nome_software, id_computador)
                       VALUES
                       (%s, %s)'''
    return genericDestructiveQuery(QUERY_TO_MAKE, args)

def editSala(args):

    QUERY_TO_MAKE = '''UPDATE public.sala SET
                       hora_fechamento=COALESCE(%s, hora_fechamento),
                       ip_sala=COALESCE(%s, ip_sala),
                       WHERE nome_sala=%s
                   '''

    return genericDestructiveQuery(QUERY_TO_MAKE, args)
    
def removeComputer(args):
    ''' '''
    QUERY_TO_MAKE = '''DELETE
                       FROM public.computador
                       WHERE id_computador=%s'''
    return genericDestructiveQuery(QUERY_TO_MAKE, args)
    
def removeSoftware(args):
    '''Used exclusively by the administrator.
args is an alist where the first item is the computer
in where our software is installed on and the second is
the software name itself'''
    
    QUERY_TO_MAKE = '''DELETE
                       FROM public.softwares_disp
                       WHERE (id_computador, nome_software) = (%s, %s)'''
    return genericDestructiveQuery(QUERY_TO_MAKE, args)
    
def userGeneralQuery(args):
    '''General query which is asked by your average user.
args argument defines what table to return so the server can
produce a proper json file'''

    if args == 1:
        QUERY_TO_MAKE = '''SELECT sl.nome_sala, to_char(hora_fechamento, 'HH24:MI')
        FROM public.sala AS sl '''
    elif args == 2:
        QUERY_TO_MAKE = '''SELECT nome_sala, comp.id_computador, pos_x, pos_y, em_uso
        FROM public.sala AS sl
        JOIN public.computador AS comp USING(nome_sala)'''
    else:
        QUERY_TO_MAKE = '''SELECT DISTINCT ON (2)  nome_sala,  soft.nome_software
        FROM public.sala AS sl
        JOIN public.computador AS comp USING(nome_sala)
        JOIN public.softwares_disp AS soft USING(id_computador)'''
        
    return genericGetQuery(QUERY_TO_MAKE, ())

def salista():
    QUERY_TO_MAKE = '''SELECT sl.nome_sala
                       FROM public.sala AS sl'''
    return genericGetQuery(QUERY_TO_MAKE, ())


def softwareList():
    QUERY_TO_MAKE = '''SELECT DISTINCT ON (1) nome_software
    FROM public.softwares_disp'''
    return genericGetQuery(QUERY_TO_MAKE, ())

def computerList():
    QUERY_TO_MAKE = '''SELECT id_computador, nome_sala
    FROM computador'''
    return genericGetQuery(QUERY_TO_MAKE, ())

def expungeSoftware(args):
    QUERY_TO_MAKE = '''DELETE FROM public.softwares_disp
    WHERE nome_software=%s'''
    return genericGetQuery(QUERY_TO_MAKE, args)
    

