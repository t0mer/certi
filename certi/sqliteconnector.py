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
                                    DomainName text NOT NULL
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

    #Get list of monitored domains
    def get_monitored_domains(self):
        monitored_domain_list = []
        try:
            self.open_connection()
            cursor = self.conn.cursor()
            query = "SELECT DomainId,DomainName FROM monitored_domains"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            self.conn.close()
            for row in result:
                monitored_domain_list.append(monitored_domain(row[0],row[1]))
            return monitored_domain_list
        except Error as e:
            logger.error(str(e))
            return monitored_domain_list

    def add_monitored_domain(self,DomainName):
        try:
            DomainName = (DomainName,)
            self.open_connection()
            sql =  """ INSERT INTO monitored_domains(DomainName) VALUES ((?))"""
            cur = self.conn.cursor()
            cur.execute(sql,DomainName)
            self.conn.commit()
            self.conn.close()
            return cur.lastrowid>0
        except Error as e:
            logger.error(str(e))
            return 0

    def delete_monitored_domain(self,DomainId):
        try:
            self.open_connection()
            sql = 'DELETE FROM monitored_domains WHERE DomainId=?'
            cur = self.conn.cursor()
            cur.execute(sql, (DomainId,))
            self.conn.commit()
            return True
        except Error as e:
            logger.error(str(e))
            return False

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


if __name__ == "__main__":
    con = SqliteConnector()
    con.create_tables()
    # logger.info(len(con.get_monitored_domains()))
    # con.delete_monitored_domain(1)
    # logger.info(len(con.get_monitored_domains()))
    # m = monitored_domain(2,"walla.co.il")
    # con.update_monitored_domain(m)