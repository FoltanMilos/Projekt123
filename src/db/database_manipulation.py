import cx_Oracle as cx


class DB_manip:
    # vytvorenie connectu do DB
    def __init__(self,ref_app):
        self.ip_adress = '158.193.151.201' #'obelix.fri.uniza.sk'
        self.username = 'foltan'
        self.password = 'h123456'
        self.port = '1521'
        self.sid = 'orcl.fri.uniza.sk'
        self.ref_app = ref_app

        dsn_tns = cx.makedsn(self.ip_adress, self.port,
                                     sid = 'orcl')
        self.conn = cx.connect(user=self.username, password=self.password, dsn=dsn_tns)
        #ALTERNATIVE CONNECTION LINK
        #IF NOT WORKING DO FOLOWING:
        #   1 : Change NTS credentials to NONE in sqlnet.ora file (find it in windows explorer finder)
        #   2 : Restart ORACLETNS service in windows services
        #self.conn = cx.connect(r'foltan/h123456@obelix.fri.uniza.sk:1521/orcl.fri.uniza.sk', mode=cx.SYSDBA)
        self.conn.autocommit = False
        self.ref_app.log.debug('-----------------------------------')
        self.ref_app.log.info("Connection to DB succesfull!")
        versioning = self.conn.version.split('.')
        self.ref_app.log.info("Db: ORACLE")
        self.ref_app.log.info("Version: " + str(versioning[0]))
        self.ref_app.log.debug('-----------------------------------')

    # VRACIA result set, ked nieco selectujes pouzi toto
    # davaj si nameisto * nazvy collumnov, budes ich mat uspor. v sete
    def select_statement(self,select):
        if self.conn is None:
            self.ref_app.log.warn("Nepodarilo sa pripojit na DB!")
            return None
        else:
            cr = self.conn.cursor()
            cr.execute(select)
            ret = cr.fetchall()
            cr.close()
            return ret

    def commit(self):
        self.conn.commit()

    def close_conn(self):
        self.conn.close()

    # Vrati len TRUE,FALSE, vzdy sa vykona, update, altery a pod
    def update_statement(self,update):
        if self.conn is None:
            return False
        else:
            cr = self.conn.cursor()
            cc = cr.execute(update)
            return True

    def delete_statement(self,delete):
        if self.conn is None:
            self.ref_app.log.warn("Nepodarilo sa pripojit na DB!")
            return False
        else:
            cr = self.conn.cursor()
            cr.execute(delete)
            return True

    def insert_statement(self,insert,rows):
        if self.conn is None:
            self.ref_app.log.warn("Nepodarilo sa pripojit na DB!")
            return False
        else:
            cr = self.conn.cursor()
            cr.execute(insert,rows)
            return True

    def insert_returning_identity(self,returning_insert,id_name):
        if (self.conn is None):
            self.ref_app.log.warn("Nepodarilo sa pripojit na DB!")
            return False
        else:
            cr = self.conn.cursor()
            newest_id_wrapper = cr.var(cx.NUMBER)
            cr.execute(returning_insert + " returning "+id_name+" into :id",id=newest_id_wrapper)
        return newest_id_wrapper.getvalue()[0]