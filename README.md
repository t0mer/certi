# certi
Certi is a python based SSL Transparency log monitoring tool that helps you keep tracking your issued certificates.

## What are Certificate logs
Certificate logs are append-only ledgers of certificates. Because they're distributed and independent, anyone can query them to see what certificates have been included and when. Because they're append-only, they are verifiable by Monitors. Organisations and individuals with the technical skills and capacity can run a log.

Thanks to CT, domain owners, browsers, academics, and other interested people can analyse and monitor logs. They’re able to see which CAs have issued which certificates, when, and for which domains.


## Features
- Monitor all your domains for certificate.
- Get alerts in many multiple communication channels thanks to [apprise](https://github.com/caronc/apprise)
- Manage your domains using REST API (swagger documentation included).


## Components and Frameworks used in TTS-STT
* [Loguru](https://pypi.org/project/loguru/) For logging.
* [FastAPI](https://github.com/tiangolo/fastapi) For REST API.
* [Apprise](https://github.com/caronc/apprise) For notifications.


## Limitations
Certi is using sslmate search API.
The free API account has the following limitations:
* 100 single-hostname queries / hour.
* 10 full-domain queries / hour.
* 75 queries / minute.
* 5 queries / second.

A <b>single-hostname query</b> is a query which returns certificates for a single specific hostname. (The include_subdomains parameter is false.)

A <b>full-domain query<b> is a query which returns certificates for all descendant sub-domains of the queried domain. (The include_subdomains parameter is true.)