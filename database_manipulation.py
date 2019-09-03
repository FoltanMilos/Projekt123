import cx_Oracle as cx

class DB_manip:

    # vytvorenie connectu do DB
    def __init__(self):
        self.ip_adress = '158.193.151.201' #'obelix.fri.uniza.sk'
        self.username = 'foltan'
        self.password = 'h123456'
        self.port = '1521'
        self.sid = 'orcl.fri.uniza.sk'

        check = False
        try:
            dsn_tns = cx.makedsn(self.ip_adress, self.port,
                                         sid = 'orcl')
            print(dsn_tns)
            self.conn = cx.connect(user=self.username, password=self.password, dsn=dsn_tns)
            #ALTERNATE CONNECTION LINK
            #IF NOT WORKING DO FOLOWING:
            #   1 : Change NTS credentials to NONE in sqlnet.ora file (find it in windows explorer finder)
            #   2 : Restart ORACLETNS service in windows services
            #self.conn = cx.connect(r'foltan/h123456@obelix.fri.uniza.sk:1521/orcl.fri.uniza.sk', mode=cx.SYSDBA)
            check = True
        except Exception as e:
            self.conn = None
            print(e)
            print("Chyba pripojenia na DB!")

        # kontrola ci sa podarilo pripojit
        if(check == True):
            self.conn.autocommit = False
            print('################################')
            print("Pripojenie na db uspesne!")
            versioning = self.conn.version.split('.')
            print("Db: ORACLE")
            print("Version: " + str(versioning[0]))
            print('################################')

    # VRACIA result set, ked nieco selectujes pouzi toto
    # davaj si nameisto * nazvy collumnov, budes ich mat uspor. v sete
    def select_statement(self,select):
        if(self.conn is None):
            print("Nepodarilo sa pripojit na DB!")
            return None
        else:
            cr = self.conn.cursor()
            cr.execute(select)
            ret = cr.fetchall() # prehodenie tusim ze na list
            cr.close()
            return ret

    def commit(self):
        self.conn.commit()

    def close_conn(self):
        self.conn.close()

    # Vrati len TRUE,FALSE, vzdy sa vykona, update, altery a pod
    def update_statement(self,update):
        if (self.conn is None):
            print("Nepodarilo sa pripojit na DB!")
            return False
        else:
            cr = self.conn.cursor()
            cc = cr.execute(update)
            return True

    def delete_statement(self,delete):
        if (self.conn is None):
            print("Nepodarilo sa pripojit na DB!")
            return False
        else:
            cr = self.conn.cursor()
            cr.execute(delete)
            return True

    def insert_statement(self,insert,rows):
        if (self.conn is None):
            print("Nepodarilo sa pripojit na DB!")
            return False
        else:
            cr = self.conn.cursor()
            ret_val = 0
            #py_var = cr.var(cx.NUMBER)
            cr.execute(insert,rows)
            return True