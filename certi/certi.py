# from concurrent.futures.process import _MAX_WINDOWS_WORKERS
from multiprocessing.dummy import Process
from requests.structures import CaseInsensitiveDict
import multiprocessing 
import time
import requests
import threading
import apprise
import sys
import os
import json
from sqliteconnector import SqliteConnector
from certificate import certificate
from loguru import logger
import sys

from server import Server
SLEEP_TIME = int(os.getenv("SLEEP_TIME"))
NOTIFIERS = os.getenv("NOTIFIERS")
API_KEY = os.getenv("API_KEY")
certificates = []
db = SqliteConnector()
server = Server(db)
apobj = apprise.Apprise()



def new_certificate_notification(certificate):
    if len(NOTIFIERS)!=0:
        apobj.notify(
            body=("New certificate issued for: {}. \r\n Issuer: {}.  \r\n Start Date: {}.  \r\n End Date: {}.  \r\n Valid Domains: {}".format(certificate.monitored_domain, certificate.issuer,  certificate.not_before, certificate.not_after, certificate.dns_names)),
            title="New certificate issued",
        )

#Query certspotter for certificates
def get_certificates_by_domain(domain):
    global certificates
    url = "https://api.certspotter.com/v1/issuances?domain="+ domain +"&expand=dns_names&expand=issuer&include_subdomains=true"
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer {}".format(API_KEY)
    resp = requests.get(url, headers=headers)
    if resp.status_code == 200:
        logger.info("Got " + str(len(resp.json())) + " certificates for domain " + domain)
        for cert in resp.json():
            certificates.append(certificate(CertificateId=0,id=cert['id'],not_after=cert['not_after'].replace('T', ' ').replace('Z', ''),
            not_before=cert['not_before'].replace('T', ' ').replace('Z', ''),pubkey_sha256=cert['pubkey_sha256'],tbs_sha256=cert['tbs_sha256'],
            issuer=cert['issuer']['name'],dns_names=str(cert['dns_names']),monitored_domain=domain))
    else:
        logger.error("Error getting certificates for domain {" + domain + "}: " + str(resp.status_code) + " " + resp.text)
        return False

def worker(event):
    global certificates
    while not event.isSet():
        try:
            certificates.clear()
            for domain in db.get_monitored_domains():
                logger.info("Fetching certificates for domain: " + domain.DomainName)
                get_certificates_by_domain(domain.DomainName)
                time.sleep(1)
            new_certificates=db.get_new_certificates(certificates)
            logger.info("Found " + str(len(new_certificates)) + " new certificates")
            db.insert_certificate_to_db(new_certificates)
            for certificate in new_certificates:
                new_certificate_notification(certificate)
            logger.debug('Sleeping...')
            event.wait(SLEEP_TIME)
        except KeyboardInterrupt:
            event.set()
            break
        except Exception as e:
            event.set()
            logger.error(e)
            logger.error("Please fix the errors and restart the application")

            
def main():
    db.create_tables()
    event = threading.Event()
    thread = threading.Thread(target=worker, args=(event,))
    thread.start()

   

if __name__ == "__main__":
    
    if len(NOTIFIERS)!=0:
        logger.info("Setting Apprise notification channels")
        jobs=NOTIFIERS.split()
        for job in jobs:
            logger.info("Adding: " + job)
            apobj.add(job)
   

    main_bot = Process(target = main)
    main_web = Process(target = server.start)
    main_bot.start()
    main_web.start()
    main_bot.join()
    main_web.join()

    

