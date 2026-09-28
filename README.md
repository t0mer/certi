# Certi

[![Docker Pulls](https://img.shields.io/docker/pulls/techblog/certi)](https://hub.docker.com/r/techblog/certi)
[![License](https://img.shields.io/github/license/t0mer/certi)](LICENSE.md)

Certi is a Python-based Certificate Transparency (CT) log monitoring tool that helps you keep track of the SSL/TLS certificates issued for your domains. It periodically queries the [SSLMate Cert Spotter](https://sslmate.com/certspotter/) API for every domain you monitor, stores the certificates it finds in a local SQLite database, and sends a notification through [Apprise](https://github.com/caronc/apprise) whenever a new certificate appears. Domains are managed through a small REST API with Swagger documentation.

It's aimed at self-hosters and domain owners who want to know when a certificate is issued for their domains, whether it was expected (a renewal) or not (a mis-issued or rogue certificate).

## Table of Contents
- [What are Certificate Transparency logs](#what-are-certificate-transparency-logs)
- [Features](#features)
- [Screenshots](#screenshots)
- [How it works](#how-it-works)
- [Requirements](#requirements)
- [Components and Frameworks used in Certi](#components-and-frameworks-used-in-certi)
- [Limitations](#limitations)
- [Installation](#installation)
- [Configuration](#configuration)
- [Managing the application (REST API)](#managing-the-application-rest-api)
- [Supported Notifications](#supported-notifications)
- [Security notes](#security-notes)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## What are Certificate Transparency logs
Certificate logs are append-only ledgers of certificates. Because they're distributed and independent, anyone can query them to see what certificates have been included and when. Because they're append-only, they are verifiable by monitors. Organizations and individuals with the technical skills and capacity can run a log.

Thanks to Certificate Transparency, domain owners, browsers, academics, and other interested people can analyze and monitor logs. They're able to see which CAs have issued which certificates, when, and for which domains.

## Features
- Monitor all your domains (including their subdomains) for newly issued certificates.
- Get alerts through many communication channels thanks to [Apprise](https://github.com/caronc/apprise).
- No alert flood on first run: certificates found during a domain's first scan are recorded as a baseline, and only certificates discovered afterwards trigger notifications (see the caveat in [Troubleshooting](#troubleshooting) if the first scan fails).
- Store all discovered certificates (issuer, validity dates, DNS names, SHA-256 hashes) in a local SQLite database.
- Manage your domains using a REST API (Swagger documentation included).
- Enable or disable monitoring per domain without deleting it.
- Multi-architecture Docker image (`linux/amd64`, `linux/arm64`, `linux/arm/v7`).

## Screenshots

### New certificate notification (Telegram)
![New certificate notification](screenshots/certi.png)

### Swagger documentation
[![Swagger Documentation](screenshots/certi-swagger.png "Swagger Documentation")](screenshots/certi-swagger.png)

## How it works

```mermaid
flowchart LR
    API[REST API :8081] -->|add / remove / toggle domains| DB[(SQLite<br/>db/certi.db)]
    W[Scan worker] -->|read active domains| DB
    W -->|GET /v1/issuances| CS[Cert Spotter API]
    W -->|store new certificates| DB
    W -->|new certificate| AP[Apprise]
    AP --> N[Telegram, Slack, Discord, email, ...]
```

Certi runs two threads side by side (via `multiprocessing.dummy`):

1. **Scan worker** — every `SLEEP_TIME` seconds it loads all *active* monitored domains and, for each one, queries `https://api.certspotter.com/v1/issuances` with `include_subdomains=true` (so each lookup is a *full-domain query*, see [Limitations](#limitations)). It waits one second between domains. Certificates whose Cert Spotter `id` or public key SHA-256 are not yet in the database are stored, and a notification is sent for each one, except during a domain's first scan.
2. **REST API** — a [FastAPI](https://github.com/tiangolo/fastapi) server (served by Uvicorn on port `8081`) used to manage monitored domains and list discovered certificates.

The notification contains the monitored domain, the issuer, the start and end dates, and the list of DNS names on the certificate.

## Requirements
- Docker (or Docker Compose).
- An [SSLMate Cert Spotter](https://sslmate.com/certspotter/) API key (a free account is enough, subject to the limits below).
- At least one Apprise notification URL if you want to receive alerts.

## Components and Frameworks used in Certi
* [Loguru](https://pypi.org/project/loguru/) for logging.
* [FastAPI](https://github.com/tiangolo/fastapi) for the REST API.
* [Apprise](https://github.com/caronc/apprise) for notifications.
* [Requests](https://pypi.org/project/requests/) for querying the Cert Spotter API.
* SQLite for storage.

## Limitations
Certi uses the SSLMate Cert Spotter search API.
The free API account has the following limitations:
* 100 single-hostname queries / hour.
* 10 full-domain queries / hour.
* 75 queries / minute.
* 5 queries / second.

A <b>single-hostname query</b> is a query which returns certificates for a single specific hostname (the `include_subdomains` parameter is false).

A <b>full-domain query</b> is a query which returns certificates for all descendant subdomains of the queried domain (the `include_subdomains` parameter is true).

Certi always queries with `include_subdomains=true`, so every monitored domain costs one full-domain query per scan. With the free plan, keep `(number of active domains) × (scans per hour)` at or below 10. The default `SLEEP_TIME` of 7200 seconds (one scan every 2 hours) allows up to 20 active domains.

## Installation
Certi is a Docker-based application. The image is published on Docker Hub as [`techblog/certi`](https://hub.docker.com/r/techblog/certi).

### Docker Compose
```yaml
services:
  certi:
    image: techblog/certi
    container_name: certi
    restart: always
    ports:
      - "8081:8081"
    environment:
      - API_KEY=<your Cert Spotter API key>
      - SLEEP_TIME=7200
      - NOTIFIERS=tgram://bottoken/ChatID
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/opt/certi/db
```

```bash
docker compose up -d
```

> **Note:** don't leave `SLEEP_TIME` or `LOG_LEVEL` as an empty value (`SLEEP_TIME=`). An empty variable overrides the image default and Certi will fail to start. Either set a value or remove the line.

### Docker
```bash
docker run -d --name certi --restart always \
  -p 8081:8081 \
  -e API_KEY=<your Cert Spotter API key> \
  -e NOTIFIERS="tgram://bottoken/ChatID" \
  -v "$(pwd)/data:/opt/certi/db" \
  techblog/certi
```

### Build from source
```bash
git clone https://github.com/t0mer/certi.git
cd certi
docker build -t certi .
```

The image is built on top of `techblog/fastapi`, which provides Python, FastAPI and Uvicorn.

## Configuration

### Environment variables

| Variable | Default (in image) | Required | Description |
| -------- | ------------------ | -------- | ----------- |
| `API_KEY` | *(empty)* | Yes | API key for the [SSLMate Cert Spotter](https://sslmate.com/certspotter/) search API. Sent as a `Bearer` token. |
| `SLEEP_TIME` | `7200` | No | Time between scans, in seconds (default is 2 hours). Keep it high enough to stay within the search API limits. Must be an integer. |
| `NOTIFIERS` | *(empty)* | No | One or more [Apprise URLs](#supported-notifications), separated by spaces. Leave empty to disable notifications. |
| `LOG_LEVEL` | `DEBUG` | No | Log level. Possible values: `DEBUG`, `INFO`, `WARNING`, `ERROR`. |

Example with two notification channels:

```
NOTIFIERS=tgram://bottoken/ChatID discord://webhook_id/webhook_token
```

### Volumes
To prevent data loss, mount a volume for the application database.
`/opt/certi/db` is the path inside the container where the SQLite database (`certi.db`) is located. The tables are created automatically on startup, but the directory itself must exist, so always mount this volume (see [Troubleshooting](#troubleshooting)).

### Ports
| Port | Description |
| ---- | ----------- |
| `8081` | REST API and Swagger documentation. The port is fixed in the code; map it to a different host port if needed (for example `"9000:8081"`). |

## Managing the application (REST API)
Certi has a small REST API for easy management. By default, the port is set to 8081. Swagger documentation is available by adding `/docs` to the end of the URL, for example `http://<docker-host>:8081/docs`. The OpenAPI schema is served at `/openapi.json`.

There is no web UI besides Swagger: add the domains you want to monitor through the API. The first scan runs right after startup, so domains added later are picked up on the next scan.

The API has the following endpoints:

| Method | Path | Description |
| ------ | ---- | ----------- |
| `GET` | `/domains/get` | Get the list of all monitored domains. |
| `PUT` | `/domains/add/{DomainName}` | Add a domain to the monitored domains list. |
| `DELETE` | `/domains/delete/{DomainId}` | Delete a domain from the monitored domains list. |
| `POST` | `/domains/active/{DomainId}/{state}?Active=true\|false` | Set the domain status to active/inactive. The state is read from the `Active` query parameter. |
| `GET` | `/certificates/get` | Get the list of all certificates that Certi found. |

### Examples

Add a domain:
```bash
curl -X PUT http://localhost:8081/domains/add/example.com
```
```json
"{\"message\":\"Domain added successfully\",\"success\":\"true\"}"
```

List monitored domains:
```bash
curl http://localhost:8081/domains/get
```
```json
[{"DomainId": 1, "DomainName": "example.com", "Active": 1, "FirstRun": 1}]
```

Disable monitoring for domain `1`:
```bash
curl -X POST "http://localhost:8081/domains/active/1/false?Active=false"
```

Delete domain `1`:
```bash
curl -X DELETE http://localhost:8081/domains/delete/1
```

List discovered certificates:
```bash
curl http://localhost:8081/certificates/get
```

Each certificate record contains `CertificateId`, `Id` (the Cert Spotter issuance ID), `tbs_sha256`, `pubkey_sha256`, `issuer`, `not_before`, `not_after`, `dns_names` and `monitored_domain`.

> The add, delete and state endpoints return their result as a JSON-encoded string (`{"message": "...", "success": "true|false"}`), not as a JSON object.

## Supported Notifications
Certi sends notifications through [Apprise](https://github.com/caronc/apprise), so every service supported by Apprise can be used. [Check out the Apprise wiki for more information on the supported services](https://github.com/caronc/apprise/wiki).

### Popular Notification Services
> **Note:** service availability depends on the Apprise version installed in your image. The Docker image and local installs pull the latest Apprise (unpinned), so fresh builds get Apprise 2.x, which removed Boxcar, Faast, Gitter, Microsoft Teams (`msteams://`), PopcornNotify and Spontit. Those rows are marked *(removed in Apprise 2.x)* below. ServerChan (`serverchan://`) is also not recognized by Apprise 2.x and is marked *(not recognized by Apprise 2.x)*. The [Apprise wiki](https://github.com/caronc/apprise/wiki) is the source of truth for the services and URL formats your version supports.

The table below lists some of the supported services, with example service URLs to put in `NOTIFIERS`. Click on any of the services listed below to get more details on how to configure Apprise for it.

| Notification Service | Service ID | Default Port | Example Syntax |
| -------------------- | ---------- | ------------ | -------------- |
| [Apprise API](https://github.com/caronc/apprise/wiki/Notify_apprise_api)  | apprise:// or apprises:// | (TCP) 80 or 443 | apprise://hostname/Token
| [AWS SES](https://github.com/caronc/apprise/wiki/Notify_ses)  | ses://   | (TCP) 443   | ses://user@domain/AccessKeyID/AccessSecretKey/RegionName<br/>ses://user@domain/AccessKeyID/AccessSecretKey/RegionName/email1/email2/emailN
| [Boxcar](https://github.com/caronc/apprise/wiki/Notify_boxcar) *(removed in Apprise 2.x)*  | boxcar://   | (TCP) 443   | boxcar://hostname<br />boxcar://hostname/@tag<br/>boxcar://hostname/device_token<br />boxcar://hostname/device_token1/device_token2/device_tokenN<br />boxcar://hostname/@tag/@tag2/device_token
| [Discord](https://github.com/caronc/apprise/wiki/Notify_discord)  | discord://   | (TCP) 443   | discord://webhook_id/webhook_token<br />discord://avatar@webhook_id/webhook_token
| [Emby](https://github.com/caronc/apprise/wiki/Notify_emby)  | emby:// or embys:// | (TCP) 8096 | emby://user@hostname/<br />emby://user:password@hostname
| [Enigma2](https://github.com/caronc/apprise/wiki/Notify_enigma2)  | enigma2:// or enigma2s:// | (TCP) 80 or 443 | enigma2://hostname
| [Faast](https://github.com/caronc/apprise/wiki/Notify_faast) *(removed in Apprise 2.x)* | faast://    | (TCP) 443    | faast://authorizationtoken
| [FCM](https://github.com/caronc/apprise/wiki/Notify_fcm) | fcm://    | (TCP) 443    | fcm://project@apikey/DEVICE_ID<br />fcm://project@apikey/#TOPIC<br/>fcm://project@apikey/DEVICE_ID1/#topic1/#topic2/DEVICE_ID2/
| [Flock](https://github.com/caronc/apprise/wiki/Notify_flock) | flock://    | (TCP) 443    | flock://token<br/>flock://botname@token<br/>flock://app_token/u:userid<br/>flock://app_token/g:channel_id<br/>flock://app_token/u:userid/g:channel_id
| [Gitter](https://github.com/caronc/apprise/wiki/Notify_gitter) *(removed in Apprise 2.x)* | gitter://    | (TCP) 443    | gitter://token/room<br/>gitter://token/room1/room2/roomN
| [Google Chat](https://github.com/caronc/apprise/wiki/Notify_googlechat) | gchat://    | (TCP) 443    | gchat://workspace/key/token
| [Gotify](https://github.com/caronc/apprise/wiki/Notify_gotify) | gotify:// or gotifys://   | (TCP) 80 or 443    | gotify://hostname/token<br />gotifys://hostname/token?priority=high
| [Growl](https://github.com/caronc/apprise/wiki/Notify_growl)  | growl://   | (UDP) 23053   | growl://hostname<br />growl://hostname:portno<br />growl://password@hostname<br />growl://password@hostname:port<br />**Note**: you can also use the get parameter _version_ which can allow the growl request to behave using the older v1.x protocol. An example would look like: growl://hostname?version=1
| [Home Assistant](https://github.com/caronc/apprise/wiki/Notify_homeassistant)       | hassio:// or hassios://   | (TCP) 8123 or 443 | hassio://hostname/accesstoken<br />hassio://user@hostname/accesstoken<br />hassio://user:password@hostname:port/accesstoken<br />hassio://hostname/optional/path/accesstoken
| [IFTTT](https://github.com/caronc/apprise/wiki/Notify_ifttt) | ifttt://    | (TCP) 443    | ifttt://webhooksID/Event<br />ifttt://webhooksID/Event1/Event2/EventN<br/>ifttt://webhooksID/Event1/?+Key=Value<br/>ifttt://webhooksID/Event1/?-Key=value1
| [Join](https://github.com/caronc/apprise/wiki/Notify_join) | join://   | (TCP) 443    | join://apikey/device<br />join://apikey/device1/device2/deviceN/<br />join://apikey/group<br />join://apikey/groupA/groupB/groupN<br />join://apikey/DeviceA/groupA/groupN/DeviceN/
| [KODI](https://github.com/caronc/apprise/wiki/Notify_kodi) | kodi:// or kodis://    | (TCP) 8080 or 443   | kodi://hostname<br />kodi://user@hostname<br />kodi://user:password@hostname:port
| [Kumulos](https://github.com/caronc/apprise/wiki/Notify_kumulos) | kumulos:// | (TCP) 443 | kumulos://apikey/serverkey
| [LaMetric Time](https://github.com/caronc/apprise/wiki/Notify_lametric) | lametric:// | (TCP) 443 | lametric://apikey@device_ipaddr<br/>lametric://apikey@hostname:port<br/>lametric://client_id@client_secret
| [Mailgun](https://github.com/caronc/apprise/wiki/Notify_mailgun) | mailgun:// | (TCP) 443 | mailgun://user@hostname/apikey<br />mailgun://user@hostname/apikey/email<br />mailgun://user@hostname/apikey/email1/email2/emailN<br />mailgun://user@hostname/apikey/?name="From%20User"
| [Matrix](https://github.com/caronc/apprise/wiki/Notify_matrix) | matrix:// or matrixs://  | (TCP) 80 or 443 | matrix://hostname<br />matrix://user@hostname<br />matrixs://user:pass@hostname:port/#room_alias<br />matrixs://user:pass@hostname:port/!room_id<br />matrixs://user:pass@hostname:port/#room_alias/!room_id/#room2<br />matrixs://token@hostname:port/?webhook=matrix<br />matrix://user:token@hostname/?webhook=slack&format=markdown
| [Mattermost](https://github.com/caronc/apprise/wiki/Notify_mattermost) | mmost:// or mmosts:// | (TCP) 8065 | mmost://hostname/authkey<br />mmost://hostname:80/authkey<br />mmost://user@hostname:80/authkey<br />mmost://hostname/authkey?channel=channel<br />mmosts://hostname/authkey<br />mmosts://user@hostname/authkey<br />
| [Microsoft Teams](https://github.com/caronc/apprise/wiki/Notify_msteams) *(removed in Apprise 2.x)* | msteams://  | (TCP) 443   | msteams://TokenA/TokenB/TokenC/
| [MQTT](https://github.com/caronc/apprise/wiki/Notify_mqtt) | mqtt://  or mqtts:// | (TCP) 1883 or 8883   | mqtt://hostname/topic<br />mqtt://user@hostname/topic<br />mqtts://user:pass@hostname:9883/topic
| [Nextcloud](https://github.com/caronc/apprise/wiki/Notify_nextcloud) | ncloud:// or nclouds:// | (TCP) 80 or 443 | ncloud://adminuser:pass@host/User<br/>nclouds://adminuser:pass@host/User1/User2/UserN
| [NextcloudTalk](https://github.com/caronc/apprise/wiki/Notify_nextcloudtalk) | nctalk:// or nctalks:// | (TCP) 80 or 443 | nctalk://user:pass@host/RoomId<br/>nctalks://user:pass@host/RoomId1/RoomId2/RoomIdN
| [Notica](https://github.com/caronc/apprise/wiki/Notify_notica) | notica://  | (TCP) 443   | notica://Token/
| [Notifico](https://github.com/caronc/apprise/wiki/Notify_notifico) | notifico://  | (TCP) 443   | notifico://ProjectID/MessageHook/
| [Office 365](https://github.com/caronc/apprise/wiki/Notify_office365) | o365://  | (TCP) 443   | o365://TenantID:AccountEmail/ClientID/ClientSecret<br />o365://TenantID:AccountEmail/ClientID/ClientSecret/TargetEmail<br />o365://TenantID:AccountEmail/ClientID/ClientSecret/TargetEmail1/TargetEmail2/TargetEmailN
| [OneSignal](https://github.com/caronc/apprise/wiki/Notify_onesignal) | onesignal:// | (TCP) 443 | onesignal://AppID@APIKey/PlayerID<br/>onesignal://TemplateID:AppID@APIKey/UserID<br/>onesignal://AppID@APIKey/#IncludeSegment<br/>onesignal://AppID@APIKey/Email
| [Opsgenie](https://github.com/caronc/apprise/wiki/Notify_opsgenie) | opsgenie:// | (TCP) 443 | opsgenie://APIKey<br/>opsgenie://APIKey/UserID<br/>opsgenie://APIKey/#Team<br/>opsgenie://APIKey/\*Schedule<br/>opsgenie://APIKey/^Escalation
| [ParsePlatform](https://github.com/caronc/apprise/wiki/Notify_parseplatform) | parsep:// or parseps:// | (TCP) 80 or 443 | parsep://AppID:MasterKey@Hostname<br/>parseps://AppID:MasterKey@Hostname
| [PopcornNotify](https://github.com/caronc/apprise/wiki/Notify_popcornnotify) *(removed in Apprise 2.x)* | popcorn://  | (TCP) 443   | popcorn://ApiKey/ToPhoneNo<br/>popcorn://ApiKey/ToPhoneNo1/ToPhoneNo2/ToPhoneNoN/<br/>popcorn://ApiKey/ToEmail<br/>popcorn://ApiKey/ToEmail1/ToEmail2/ToEmailN/<br/>popcorn://ApiKey/ToPhoneNo1/ToEmail1/ToPhoneNoN/ToEmailN
| [Prowl](https://github.com/caronc/apprise/wiki/Notify_prowl) | prowl://   | (TCP) 443    | prowl://apikey<br />prowl://apikey/providerkey
| [PushBullet](https://github.com/caronc/apprise/wiki/Notify_pushbullet) | pbul://    | (TCP) 443    | pbul://accesstoken<br />pbul://accesstoken/#channel<br/>pbul://accesstoken/A_DEVICE_ID<br />pbul://accesstoken/email@address.com<br />pbul://accesstoken/#channel/#channel2/email@address.net/DEVICE
| [Pushjet](https://github.com/caronc/apprise/wiki/Notify_pushjet) | pjet:// or pjets:// | (TCP) 80 or 443 | pjet://hostname/secret<br />pjet://hostname:port/secret<br />pjets://secret@hostname/secret<br />pjets://hostname:port/secret
| [Push (Techulus)](https://github.com/caronc/apprise/wiki/Notify_techulus) | push://    | (TCP) 443    | push://apikey/
| [Pushed](https://github.com/caronc/apprise/wiki/Notify_pushed) | pushed://    | (TCP) 443    | pushed://appkey/appsecret/<br/>pushed://appkey/appsecret/#ChannelAlias<br/>pushed://appkey/appsecret/#ChannelAlias1/#ChannelAlias2/#ChannelAliasN<br/>pushed://appkey/appsecret/@UserPushedID<br/>pushed://appkey/appsecret/@UserPushedID1/@UserPushedID2/@UserPushedIDN
| [Pushover](https://github.com/caronc/apprise/wiki/Notify_pushover)  | pover://   | (TCP) 443   | pover://user@token<br />pover://user@token/DEVICE<br />pover://user@token/DEVICE1/DEVICE2/DEVICEN<br />**Note**: you must specify both your user_id and token
| [PushSafer](https://github.com/caronc/apprise/wiki/Notify_pushsafer)  | psafer:// or psafers://  | (TCP) 80 or 443  | psafer://privatekey<br />psafers://privatekey/DEVICE<br />psafer://privatekey/DEVICE1/DEVICE2/DEVICEN
| [Reddit](https://github.com/caronc/apprise/wiki/Notify_reddit) | reddit:// | (TCP) 443   | reddit://user:password@app_id/app_secret/subreddit<br />reddit://user:password@app_id/app_secret/sub1/sub2/subN
| [Rocket.Chat](https://github.com/caronc/apprise/wiki/Notify_rocketchat) | rocket:// or rockets://  | (TCP) 80 or 443   | rocket://user:password@hostname/RoomID/Channel<br />rockets://user:password@hostname:443/#Channel1/#Channel1/RoomID<br />rocket://user:password@hostname/#Channel<br />rocket://webhook@hostname<br />rockets://webhook@hostname/@User/#Channel
| [Ryver](https://github.com/caronc/apprise/wiki/Notify_ryver) | ryver://  | (TCP) 443   | ryver://Organization/Token<br />ryver://botname@Organization/Token
| [SendGrid](https://github.com/caronc/apprise/wiki/Notify_sendgrid) | sendgrid://  | (TCP) 443   | sendgrid://APIToken:FromEmail/<br />sendgrid://APIToken:FromEmail/ToEmail<br />sendgrid://APIToken:FromEmail/ToEmail1/ToEmail2/ToEmailN/
| [ServerChan](https://github.com/caronc/apprise/wiki/Notify_serverchan) *(not recognized by Apprise 2.x)* | serverchan://   | (TCP) 443    | serverchan://token/
| [SimplePush](https://github.com/caronc/apprise/wiki/Notify_simplepush) | spush://   | (TCP) 443    | spush://apikey<br />spush://salt:password@apikey<br />spush://apikey?event=Apprise
| [Slack](https://github.com/caronc/apprise/wiki/Notify_slack) | slack://  | (TCP) 443   | slack://TokenA/TokenB/TokenC/<br />slack://TokenA/TokenB/TokenC/Channel<br />slack://botname@TokenA/TokenB/TokenC/Channel<br />slack://user@TokenA/TokenB/TokenC/Channel1/Channel2/ChannelN
| [SMTP2Go](https://github.com/caronc/apprise/wiki/Notify_smtp2go) | smtp2go:// | (TCP) 443 | smtp2go://user@hostname/apikey<br />smtp2go://user@hostname/apikey/email<br />smtp2go://user@hostname/apikey/email1/email2/emailN<br />smtp2go://user@hostname/apikey/?name="From%20User"
| [Streamlabs](https://github.com/caronc/apprise/wiki/Notify_streamlabs) | strmlabs:// | (TCP) 443 | strmlabs://AccessToken/<br/>strmlabs://AccessToken/?name=name&identifier=identifier&amount=0&currency=USD
| [SparkPost](https://github.com/caronc/apprise/wiki/Notify_sparkpost) | sparkpost:// | (TCP) 443 | sparkpost://user@hostname/apikey<br />sparkpost://user@hostname/apikey/email<br />sparkpost://user@hostname/apikey/email1/email2/emailN<br />sparkpost://user@hostname/apikey/?name="From%20User"
| [Spontit](https://github.com/caronc/apprise/wiki/Notify_spontit) *(removed in Apprise 2.x)* | spontit://  | (TCP) 443   | spontit://UserID@APIKey/<br />spontit://UserID@APIKey/Channel<br />spontit://UserID@APIKey/Channel1/Channel2/ChannelN
| [Syslog](https://github.com/caronc/apprise/wiki/Notify_syslog) | syslog://  | (UDP) 514 (_if hostname specified_) | syslog://<br />syslog://Facility<br />syslog://hostname<br />syslog://hostname/Facility
| [Telegram](https://github.com/caronc/apprise/wiki/Notify_telegram) | tgram://  | (TCP) 443   | tgram://bottoken/ChatID<br />tgram://bottoken/ChatID1/ChatID2/ChatIDN
| [Twitter](https://github.com/caronc/apprise/wiki/Notify_twitter) | twitter://  | (TCP) 443   | twitter://CKey/CSecret/AKey/ASecret<br/>twitter://user@CKey/CSecret/AKey/ASecret<br/>twitter://CKey/CSecret/AKey/ASecret/User1/User2/User2<br/>twitter://CKey/CSecret/AKey/ASecret?mode=tweet
| [Twist](https://github.com/caronc/apprise/wiki/Notify_twist) | twist://  | (TCP) 443   | twist://password:login<br/>twist://password:login/#channel<br/>twist://password:login/#team:channel<br/>twist://password:login/#team:channel1/channel2/#team3:channel
| [XBMC](https://github.com/caronc/apprise/wiki/Notify_xbmc) | xbmc:// or xbmcs://    | (TCP) 8080 or 443   | xbmc://hostname<br />xbmc://user@hostname<br />xbmc://user:password@hostname:port
| [XMPP](https://github.com/caronc/apprise/wiki/Notify_xmpp) | xmpp:// or xmpps://    | (TCP) 5222 or 5223   | xmpp://user:password@hostname<br />xmpps://user:password@hostname:port?jid=user@hostname/resource<br/>xmpps://user:password@hostname/target@myhost, target2@myhost/resource
| [Webex Teams (Cisco)](https://github.com/caronc/apprise/wiki/Notify_wxteams) | wxteams://  | (TCP) 443   | wxteams://Token
| [Zulip Chat](https://github.com/caronc/apprise/wiki/Notify_zulip) | zulip://  | (TCP) 443   | zulip://botname@Organization/Token<br />zulip://botname@Organization/Token/Stream<br />zulip://botname@Organization/Token/Email

## Security notes
- **The REST API has no authentication.** Anyone who can reach port 8081 can list, add and delete monitored domains and read the stored certificates. Don't expose it to the internet; keep it on a trusted network or put it behind a reverse proxy with authentication.
- `API_KEY` and the Apprise URLs in `NOTIFIERS` often contain secrets (bot tokens, webhook keys, passwords). Keep them out of version control, for example by using an `.env` file with Docker Compose.
- The data volume contains only certificate metadata and the list of monitored domains; no credentials are stored in the database.

## Troubleshooting
- **The container exits on startup with `ValueError: invalid literal for int()`** — `SLEEP_TIME` is set to an empty value. Set it to a number of seconds or remove the variable to use the default (7200).
- **The container exits on startup with a log level error** — `LOG_LEVEL` is set to an empty value. Set it to `DEBUG`, `INFO`, `WARNING` or `ERROR`, or remove the variable.
- **`unable to open database file` in the logs** — the database directory `/opt/certi/db` does not exist. Mount a volume on `/opt/certi/db`.
- **`Error getting certificates for domain {...}: 401` / `429`** — the API key is missing or invalid (401), or you hit the Cert Spotter rate limits (429). Check `API_KEY`, increase `SLEEP_TIME` or reduce the number of active domains.
- **Scanning stops after an error** — when an unexpected error occurs in the scan loop, Certi logs `Please fix the errors and restart the application` and stops scanning (the API keeps running). Fix the cause and restart the container.
- **No notification for existing certificates** — this is expected: certificates found during a domain's first scan are stored without sending alerts. Use `GET /certificates/get` to see them.
- **A burst of alerts for old certificates** — if a domain's first scan fails (for example an invalid API key or a rate-limit error), the domain is still marked as scanned, so the next successful scan sends a notification for every existing certificate. Make sure `API_KEY` is valid before adding domains.

## Development
Project layout:

```
certi/
├── certi.py             # entry point: scan worker, Cert Spotter queries, Apprise notifications
├── server.py            # FastAPI REST API (port 8081)
├── sqliteconnector.py   # SQLite access (db/certi.db)
├── certificate.py       # certificate model
└── monitored_domain.py  # monitored domain model
```

Run locally without Docker (Python 3):

```bash
pip install -r requirements.txt fastapi uvicorn jinja2
cd certi
mkdir -p db
export API_KEY=<your Cert Spotter API key> SLEEP_TIME=7200 LOG_LEVEL=DEBUG NOTIFIERS=""
python3 certi.py
```

`requirements.txt` is used for local runs only: the Dockerfile does not install it, it installs `apprise` on top of the `techblog/fastapi` base image, which provides FastAPI, Uvicorn and the other dependencies. FastAPI, Uvicorn and Jinja2 (imported by `server.py`) are not listed in `requirements.txt`, so install them explicitly as shown above.

Docker images are published by GitHub Actions: `docker-publish.yml` builds `techblog/certi:latest` and `techblog/certi:<VERSION>` for `linux/amd64`, `linux/arm64` and `linux/arm/v7` when a GitHub release is published (or on manual dispatch). The version comes from the `VERSION` file. `publish-ghcr.yml` is a manual workflow that can publish `ghcr.io/t0mer/certi`, but no public GHCR image is available yet. `jcr-image.yml` pushes to a private JFrog registry.

## Contributing
Issues and pull requests are welcome. Please open an issue first to discuss larger changes.

## License
Certi is licensed under the [Apache License 2.0](LICENSE.md).
