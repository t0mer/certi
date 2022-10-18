import sqlite3
from sqlite3 import Error
from loguru import logger
from monitored_domain import monitored_domain
class SqliteConnector:
    def __init__(self):
        self.db_file = "db/certi.db"
        self.conn = None

    def open_connection(self):
        try:
            self.conn = sqlite3.connect(self.db_file)
        except Error as e:
            logger.error(str(e))

    def close_connection(self):
        try:
            self.conn.close()
        except Error as e:
            logger.error(str(e))

    def create_tables(self):
        self.open_connection()
        create_monitored_domains_table = """ CREATE TABLE IF NOT EXISTS monitored_domains (
                                    DomainId integer PRIMARY KEY,
                                    DomainName text NOT NULL,
                                    Active integer DEFAULT 1 NOT NULL,
                                    FirstRun integer DEFAULT 1 NOT NULL
                                ); """

        create_certificates_table = """ CREATE TABLE IF NOT EXISTS certificates (
                                    CertificateId integer PRIMARY KEY,
                                    Id integer NOT NULL,
                                    tbs_sha256 text NOT NULL,
                                    pubkey_sha256 text NOT NULL,
                                    issuer text NOT NULL,
                                    not_before datetime NOT NULL,
                                    not_after datetime NOT NULL,
                                    dns_names text NOT NULL,
                                    monitored_domain text NOT NULL
                                ); """

        try:
            c = self.conn.cursor()
            c.execute(create_monitored_domains_table) 
            c.execute(create_certificates_table)  
            c.close()
            self.conn.close()          
        except Error as e:
            logger.error(str(e))
   
    def get_monitored_domains(self, api_call=False):
        monitored_domain_list = []
        logger.debug("api_call = " + str(api_call))
        try:
            self.open_connection()
            cursor = self.conn.cursor()
            query = "SELECT DomainId,DomainName,Active,FirstRun FROM monitored_domains"
            cursor.execute(query)
            if api_call == True:
                rows = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
                cursor.close()
                return (rows[0] if rows else None) if False else rows
            else:
                result = cursor.fetchall()
                for row in result:
                    monitored_domain_list.append(monitored_domain(row[0],row[1],row[2],row[3]))
                cursor.close()
                return monitored_domain_list
        except Error as e:
            logger.error(str(e))
            return monitored_domain_list
        finally:
            self.close_connection()



    def get_monitored_domains_by_state(self, api_call=False,Active=True):
        monitored_domain_list = []
        logger.debug("api_call = " + str(api_call))
        try:
            self.open_connection()
            cursor = self.conn.cursor()
            query = "SELECT DomainId,DomainName,Active,FirstRun FROM monitored_domains where Active=?"
            cursor.execute(query,(Active,))
            if api_call == True:
                rows = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
                cursor.close()
                return (rows[0] if rows else None) if False else rows
            else:
                result = cursor.fetchall()
                for row in result:
                    monitored_domain_list.append(monitored_domain(row[0],row[1],row[2],row[3]))
                cursor.close()
                return monitored_domain_list
        except Error as e:
            logger.error(str(e))
            return monitored_domain_list
        finally:
            self.close_connection()

    def add_monitored_domain(self,DomainName):
        try:
            DomainName = (DomainName,)
            self.open_connection()
            sql =  """ INSERT INTO monitored_domains(DomainName) VALUES ((?))"""
            cur = self.conn.cursor()
            cur.execute(sql,DomainName)
            self.conn.commit()
            self.conn.close()
            return str(cur.lastrowid>0), "Domain addedd successfully"
        except Error as e:
            logger.error(str(e))
            return False, str(e)

    def delete_monitored_domain(self,DomainId):
        try:
            self.open_connection()
            sql = 'DELETE FROM monitored_domains WHERE DomainId=?'
            cur = self.conn.cursor()
            cur.execute(sql, (DomainId,))
            self.conn.commit()
            if(cur.rowcount>0):
                return str(True), "Domain deleted successfully"
            else:
                return str(False), "Domain was not deleted, no record found"
        except Error as e:
            logger.error(str(e))
            return str(False), str(e)

    def update_monitored_domain(self, monitored_domain):
        try:
            self.open_connection()
            sql = ''' UPDATE monitored_domains
              SET DomainName = ? 
              WHERE DomainId = ?'''
            cur = self.conn.cursor()
            cur.execute(sql,(monitored_domain.DomainName,monitored_domain.DomainId))
            self.conn.commit()
            cur.close()
            self.conn.close()
            return True
        except Error as e:
            logger.error(str(e))
            return False

    def update_monitored_domain_first_run(self, DomainId,FirstRun):
        try:
            self.open_connection()
            sql = ''' UPDATE monitored_domains
              SET FirstRun = ? 
              WHERE DomainId = ?'''
            cur = self.conn.cursor()
            cur.execute(sql,(FirstRun,DomainId))
            self.conn.commit()
            cur.close()
            self.conn.close()
            return True
        except Error as e:
            logger.error(str(e))
            return False


    def set_monitored_domain_state(self,DomainId,Active):
        try:
            self.open_connection()
            sql = ''' UPDATE monitored_domains
              SET Active = ? 
              WHERE DomainId = ?'''
            cur = self.conn.cursor()
            cur.execute(sql,(Active,DomainId))
            self.conn.commit()
            if(cur.rowcount>0):
                return str(True), "Domain state updated successfully"
            else:
                return str(False), "Domain state was not updated, no record found"
        except Error as e:
            logger.error(str(e))
            return str(False), str(e)
        finally:
            self.conn.close()


    def get_new_certificates(self, certificates):
        new_certificates=[]
        try:
            self.open_connection()
            cursor = self.conn.cursor()
            for certificate in certificates:
                query = "SELECT id FROM certificates WHERE id=? or pubkey_sha256=?"
                cursor.execute(query, (certificate.id,certificate.pubkey_sha256))
                rows = cursor.fetchall()
                if len(rows) > 0:
                    continue
                else:
                    new_certificates.append(certificate)
            cursor.close()
            self.conn.close()
            return new_certificates
        except Exception as e:
            self.conn.close()
            logger.error(e)
            return new_certificates


    def get_certificates(self):
        try:
            self.open_connection()
            cursor = self.conn.cursor()
            query = "SELECT * FROM certificates"
            cursor.execute(query)
            rows = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
            return (rows[0] if rows else None) if False else rows
        except Exception as e:
            self.conn.close()
            logger.error(e)
            return False

#Add new certificates to database
    def insert_certificate_to_db(self, certificates):
        try:
            self.open_connection()
            logger.debug("Inserting " + str(len(certificates)) + " certificates to database")
            cursor = self.conn.cursor()
            for certificate in certificates:
                logger.debug("Inserting certificate: " + certificate.id) 
                
                query = '''INSERT INTO certificates (id,not_after,not_before,pubkey_sha256,tbs_sha256,issuer,dns_names,monitored_domain) VALUES (?,?,?,?,?,?,?,?)'''
                cursor.execute(query, (certificate.id,certificate.not_after,certificate.not_before,certificate.pubkey_sha256,
                                    certificate.tbs_sha256,certificate.issuer,certificate.dns_names,certificate.monitored_domain))
                self.conn.commit()
            cursor.close()
            self.conn.close()
            return True
        except Error as e:
            logger.error(str(e))
            self.conn.close()
            return False




if __name__ == "__main__":
    con = SqliteConnector()
    con.create_tables()
