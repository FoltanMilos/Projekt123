import cx_Oracle as cx

class DB_manip:

    # vytvorenie connectu do DB
    def __init__(self):
        self.ip_adress = '127.0.0.1'
        self.username = 'projectUser'
        self.password = 'password11'
        self.port = '1521'
        self.tns_name = 'xe'
        self.schema = 'PROJECTUSER'

        check = False
        try:
            self.conn = cx.connect(self.username + '/' + self.password
                                   + '@' + self.ip_adress + ':' + self.port +
                                   '/' + self.tns_name, mode=cx.SYSDBA)
            check = True
        except Exception as e:
            self.conn = None
            print("Chyba pripojenia na DB!")

        # kontrola ci sa podarilo pripojit
        if(check == True):
            #cur = self.conn.cursor()
            cur = self.select_statement("Select * from "+self.schema+".TEST_TABLE")
            #cur.execute("Select * from "+self.schema+".TEST_TABLE")
            for result in cur:
                print(result)
            #cur.close()
            self.conn.close()


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


    def close_conn(self):
        self.conn.close()


    def update_statement(self,update):
        if (self.conn is None):
            print("Nepodarilo sa pripojit na DB!")
            return None
        else:
            return True

    def delete_statement(self):
        pass



