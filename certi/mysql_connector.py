import mysql.connector
from loguru import logger
import os
from monitored_domain import monitored_domain

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

cnx = None

#Open Database connection
def open_db_connection():
    global cnx
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, database=DB_NAME,charset='ascii', use_unicode=True)
    logger.info("Connected to database")
    return cnx

#Close Database connection
def close_db_connection():
    global cnx
    if cnx is not None:
        cnx.close()
        logger.info("Disconnected from database")
    
#Get list of monitored domains
def get_monitored_domains():
    global cnx
    monitored_domain_list = []
    if cnx is None or cnx.is_connected() is False:
        open_db_connection()
    cursor = cnx.cursor()
    query = "SELECT DomainId,DomainName FROM monitored_domains"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    for row in result:
        monitored_domain_list.append(monitored_domain(row[0],row[1]))
    return monitored_domain_list

#Add new certificates to database
def insert_certificate_to_db(certificates):
    global cnx
    if cnx is None or cnx.is_connected() is False:
        open_db_connection()
    logger.info("Inserting " + str(len(certificates)) + " certificates to database")
    cursor = cnx.cursor()
    for certificate in certificates:
        logger.info("Inserting certificate: " + certificate.id) 
        
        query = "INSERT INTO certificates (id,not_after,not_before,pubkey_sha256,tbs_sha256,issuer,dns_names,monitored_domain) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (certificate.id,certificate.not_after,certificate.not_before,certificate.pubkey_sha256,
                            certificate.tbs_sha256,certificate.issuer,certificate.dns_names,certificate.monitored_domain))
        cnx.commit()
    cursor.close()
    return True

#Create new certificates list
def get_new_certificates(certificates):
    global cnx
    new_certificates=[]
    try:
        if cnx is None or cnx.is_connected() is False:
            open_db_connection()
        cursor = cnx.cursor()
        for certificate in certificates:
            query = "SELECT id FROM certificates WHERE id = %s or pubkey_sha256 = %s"
            cursor.execute(query, (certificate.id,certificate.pubkey_sha256))
            cursor.fetchall()
            if cursor.rowcount > 0:
                continue
            else:
                new_certificates.append(certificate)
        cursor.close()
        close_db_connection()
        return new_certificates
    except Exception as e:
        logger.error(e)
        return False