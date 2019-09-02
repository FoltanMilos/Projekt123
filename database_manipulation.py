import cx_Oracle as cx

class DB_manip:

    # vytvorenie connectu do DB
    def __init__(self):
        self.ip_adress = 'obelix.fri.uniza.sk'   # #158.193.151.201
        self.username = 'foltan'
        self.password = 'foltanKONTOprePROJEKT'
        self.port = '1521'
        self.sid = 'orcl'  #orcl.fri.uniza.sk ,
        self.schema = 'FOLTAN'

        check = False
        try:
            dsn_tns = cx.makedsn(self.ip_adress, self.port,
                                         service_name = 'orcl.fri.uniza.sk') #
            self.conn = cx.connect(user='foltan', password='foltanKONTOprePROJEKT', dsn=dsn_tns)


            #self.conn = cx.connect(self.username + '/' + self.password
            #                       + '@' + self.ip_adress + ':' + self.port +
            #                       '/' + self.sid, mode=cx.SYSDBA)
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
            #cur = self.conn.cursor()
            cur = self.select_statement("Select * from "+self.schema+".proj_user")
            for result in cur:
                print(result)
            cur.close()
            self.conn.close()


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