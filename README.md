# Certi
Certi is a python based SSL Transparency log monitoring tool that helps you keep tracking your issued certificates.

## What are Certificate logs
Certificate logs are append-only ledgers of certificates. Because they're distributed and independent, anyone can query them to see what certificates have been included and when. Because they're append-only, they are verifiable by Monitors. Organisations and individuals with the technical skills and capacity can run a log.

Thanks to CT, domain owners, browsers, academics, and other interested people can analyse and monitor logs. They’re able to see which CAs have issued which certificates, when, and for which domains.


## Features
- Monitor all your domains for certificate.
- Get alerts in many multiple communication channels thanks to [apprise](https://github.com/caronc/apprise)
- Manage your domains using REST API (swagger documentation included).


## Components and Frameworks used in Certi
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

## Supported Notifications
The section identifies all of the services supported by this library. [Check out the wiki for more information on the supported modules here](https://github.com/caronc/apprise/wiki).

### Popular Notification Services
The table below identifies the services this tool supports and some example service urls you need to use in order to take advantage of it. Click on any of the services listed below to get more details on how you can configure Apprise to access them.

| Notification Service | Service ID | Default Port | Example Syntax |
| -------------------- | ---------- | ------------ | -------------- |
| [Apprise API](https://github.com/caronc/apprise/wiki/Notify_apprise_api)  | apprise:// or apprises:// | (TCP) 80 or 443 | apprise://hostname/Token
| [AWS SES](https://github.com/caronc/apprise/wiki/Notify_ses)  | ses://   | (TCP) 443   | ses://user@domain/AccessKeyID/AccessSecretKey/RegionName<br/>ses://user@domain/AccessKeyID/AccessSecretKey/RegionName/email1/email2/emailN
| [Boxcar](https://github.com/caronc/apprise/wiki/Notify_boxcar)  | boxcar://   | (TCP) 443   | boxcar://hostname<br />boxcar://hostname/@tag<br/>boxcar://hostname/device_token<br />boxcar://hostname/device_token1/device_token2/device_tokenN<br />boxcar://hostname/@tag/@tag2/device_token
| [Discord](https://github.com/caronc/apprise/wiki/Notify_discord)  | discord://   | (TCP) 443   | discord://webhook_id/webhook_token<br />discord://avatar@webhook_id/webhook_token
| [Emby](https://github.com/caronc/apprise/wiki/Notify_emby)  | emby:// or embys:// | (TCP) 8096 | emby://user@hostname/<br />emby://user:password@hostname
| [Enigma2](https://github.com/caronc/apprise/wiki/Notify_enigma2)  | enigma2:// or enigma2s:// | (TCP) 80 or 443 | enigma2://hostname
| [Faast](https://github.com/caronc/apprise/wiki/Notify_faast) | faast://    | (TCP) 443    | faast://authorizationtoken
| [FCM](https://github.com/caronc/apprise/wiki/Notify_fcm) | fcm://    | (TCP) 443    | fcm://project@apikey/DEVICE_ID<br />fcm://project@apikey/#TOPIC<br/>fcm://project@apikey/DEVICE_ID1/#topic1/#topic2/DEVICE_ID2/
| [Flock](https://github.com/caronc/apprise/wiki/Notify_flock) | flock://    | (TCP) 443    | flock://token<br/>flock://botname@token<br/>flock://app_token/u:userid<br/>flock://app_token/g:channel_id<br/>flock://app_token/u:userid/g:channel_id
| [Gitter](https://github.com/caronc/apprise/wiki/Notify_gitter) | gitter://    | (TCP) 443    | gitter://token/room<br/>gitter://token/room1/room2/roomN
| [Google Chat](https://github.com/caronc/apprise/wiki/Notify_googlechat) | gchat://    | (TCP) 443    | gchat://workspace/key/token
| [Gotify](https://github.com/caronc/apprise/wiki/Notify_gotify) | gotify:// or gotifys://   | (TCP) 80 or 443    | gotify://hostname/token<br />gotifys://hostname/token?priority=high
| [Growl](https://github.com/caronc/apprise/wiki/Notify_growl)  | growl://   | (UDP) 23053   | growl://hostname<br />growl://hostname:portno<br />growl://password@hostname<br />growl://password@hostname:port</br>**Note**: you can also use the get parameter _version_ which can allow the growl request to behave using the older v1.x protocol. An example would look like: growl://hostname?version=1
| [Home Assistant](https://github.com/caronc/apprise/wiki/Notify_homeassistant)       | hassio:// or hassios://   | (TCP) 8123 or 443 | hassio://hostname/accesstoken<br />hassio://user@hostname/accesstoken<br />hassio://user:password@hostname:port/accesstoken<br />hassio://hostname/optional/path/accesstoken
| [IFTTT](https://github.com/caronc/apprise/wiki/Notify_ifttt) | ifttt://    | (TCP) 443    | ifttt://webhooksID/Event<br />ifttt://webhooksID/Event1/Event2/EventN<br/>ifttt://webhooksID/Event1/?+Key=Value<br/>ifttt://webhooksID/Event1/?-Key=value1
| [Join](https://github.com/caronc/apprise/wiki/Notify_join) | join://   | (TCP) 443    | join://apikey/device<br />join://apikey/device1/device2/deviceN/<br />join://apikey/group<br />join://apikey/groupA/groupB/groupN<br />join://apikey/DeviceA/groupA/groupN/DeviceN/
| [KODI](https://github.com/caronc/apprise/wiki/Notify_kodi) | kodi:// or kodis://    | (TCP) 8080 or 443   | kodi://hostname<br />kodi://user@hostname<br />kodi://user:password@hostname:port
| [Kumulos](https://github.com/caronc/apprise/wiki/Notify_kumulos) | kumulos:// | (TCP) 443 | kumulos://apikey/serverkey
| [LaMetric Time](https://github.com/caronc/apprise/wiki/Notify_lametric) | lametric:// | (TCP) 443 | lametric://apikey@device_ipaddr<br/>lametric://apikey@hostname:port<br/>lametric://client_id@client_secret
| [Mailgun](https://github.com/caronc/apprise/wiki/Notify_mailgun) | mailgun:// | (TCP) 443 | mailgun://user@hostname/apikey<br />mailgun://user@hostname/apikey/email<br />mailgun://user@hostname/apikey/email1/email2/emailN<br />mailgun://user@hostname/apikey/?name="From%20User"
| [Matrix](https://github.com/caronc/apprise/wiki/Notify_matrix) | matrix:// or matrixs://  | (TCP) 80 or 443 | matrix://hostname<br />matrix://user@hostname<br />matrixs://user:pass@hostname:port/#room_alias<br />matrixs://user:pass@hostname:port/!room_id<br />matrixs://user:pass@hostname:port/#room_alias/!room_id/#room2<br />matrixs://token@hostname:port/?webhook=matrix<br />matrix://user:token@hostname/?webhook=slack&format=markdown
| [Mattermost](https://github.com/caronc/apprise/wiki/Notify_mattermost) | mmost:// or mmosts:// | (TCP) 8065 | mmost://hostname/authkey<br />mmost://hostname:80/authkey<br />mmost://user@hostname:80/authkey<br />mmost://hostname/authkey?channel=channel<br />mmosts://hostname/authkey<br />mmosts://user@hostname/authkey<br />
| [Microsoft Teams](https://github.com/caronc/apprise/wiki/Notify_msteams) | msteams://  | (TCP) 443   | msteams://TokenA/TokenB/TokenC/
| [MQTT](https://github.com/caronc/apprise/wiki/Notify_mqtt) | mqtt://  or mqtts:// | (TCP) 1883 or 8883   | mqtt://hostname/topic<br />mqtt://user@hostname/topic<br />mqtts://user:pass@hostname:9883/topic
| [Nextcloud](https://github.com/caronc/apprise/wiki/Notify_nextcloud) | ncloud:// or nclouds:// | (TCP) 80 or 443 | ncloud://adminuser:pass@host/User<br/>nclouds://adminuser:pass@host/User1/User2/UserN
| [NextcloudTalk](https://github.com/caronc/apprise/wiki/Notify_nextcloudtalk) | nctalk:// or nctalks:// | (TCP) 80 or 443 | nctalk://user:pass@host/RoomId<br/>nctalks://user:pass@host/RoomId1/RoomId2/RoomIdN
| [Notica](https://github.com/caronc/apprise/wiki/Notify_notica) | notica://  | (TCP) 443   | notica://Token/
| [Notifico](https://github.com/caronc/apprise/wiki/Notify_notifico) | notifico://  | (TCP) 443   | notifico://ProjectID/MessageHook/
| [Office 365](https://github.com/caronc/apprise/wiki/Notify_office365) | o365://  | (TCP) 443   | o365://TenantID:AccountEmail/ClientID/ClientSecret<br />o365://TenantID:AccountEmail/ClientID/ClientSecret/TargetEmail<br />o365://TenantID:AccountEmail/ClientID/ClientSecret/TargetEmail1/TargetEmail2/TargetEmailN
| [OneSignal](https://github.com/caronc/apprise/wiki/Notify_onesignal) | onesignal:// | (TCP) 443 | onesignal://AppID@APIKey/PlayerID<br/>onesignal://TemplateID:AppID@APIKey/UserID<br/>onesignal://AppID@APIKey/#IncludeSegment<br/>onesignal://AppID@APIKey/Email
| [Opsgenie](https://github.com/caronc/apprise/wiki/Notify_opsgenie) | opsgenie:// | (TCP) 443 | opsgenie://APIKey<br/>opsgenie://APIKey/UserID<br/>opsgenie://APIKey/#Team<br/>opsgenie://APIKey/\*Schedule<br/>opsgenie://APIKey/^Escalation
| [ParsePlatform](https://github.com/caronc/apprise/wiki/Notify_parseplatform) | parsep:// or parseps:// | (TCP) 80 or 443 | parsep://AppID:MasterKey@Hostname<br/>parseps://AppID:MasterKey@Hostname
| [PopcornNotify](https://github.com/caronc/apprise/wiki/Notify_popcornnotify) | popcorn://  | (TCP) 443   | popcorn://ApiKey/ToPhoneNo<br/>popcorn://ApiKey/ToPhoneNo1/ToPhoneNo2/ToPhoneNoN/<br/>popcorn://ApiKey/ToEmail<br/>popcorn://ApiKey/ToEmail1/ToEmail2/ToEmailN/<br/>popcorn://ApiKey/ToPhoneNo1/ToEmail1/ToPhoneNoN/ToEmailN
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
| [ServerChan](https://github.com/caronc/apprise/wiki/Notify_serverchan) | serverchan://   | (TCP) 443    | serverchan://token/
| [SimplePush](https://github.com/caronc/apprise/wiki/Notify_simplepush) | spush://   | (TCP) 443    | spush://apikey<br />spush://salt:password@apikey<br />spush://apikey?event=Apprise
| [Slack](https://github.com/caronc/apprise/wiki/Notify_slack) | slack://  | (TCP) 443   | slack://TokenA/TokenB/TokenC/<br />slack://TokenA/TokenB/TokenC/Channel<br />slack://botname@TokenA/TokenB/TokenC/Channel<br />slack://user@TokenA/TokenB/TokenC/Channel1/Channel2/ChannelN
| [SMTP2Go](https://github.com/caronc/apprise/wiki/Notify_smtp2go) | smtp2go:// | (TCP) 443 | smtp2go://user@hostname/apikey<br />smtp2go://user@hostname/apikey/email<br />smtp2go://user@hostname/apikey/email1/email2/emailN<br />smtp2go://user@hostname/apikey/?name="From%20User"
| [Streamlabs](https://github.com/caronc/apprise/wiki/Notify_streamlabs) | strmlabs:// | (TCP) 443 | strmlabs://AccessToken/<br/>strmlabs://AccessToken/?name=name&identifier=identifier&amount=0&currency=USD
| [SparkPost](https://github.com/caronc/apprise/wiki/Notify_sparkpost) | sparkpost:// | (TCP) 443 | sparkpost://user@hostname/apikey<br />sparkpost://user@hostname/apikey/email<br />sparkpost://user@hostname/apikey/email1/email2/emailN<br />sparkpost://user@hostname/apikey/?name="From%20User"
| [Spontit](https://github.com/caronc/apprise/wiki/Notify_spontit) | spontit://  | (TCP) 443   | spontit://UserID@APIKey/<br />spontit://UserID@APIKey/Channel<br />spontit://UserID@APIKey/Channel1/Channel2/ChannelN
| [Syslog](https://github.com/caronc/apprise/wiki/Notify_syslog) | syslog://  | (UDP) 514 (_if hostname specified_) | syslog://<br />syslog://Facility<br />syslog://hostname<br />syslog://hostname/Facility
| [Telegram](https://github.com/caronc/apprise/wiki/Notify_telegram) | tgram://  | (TCP) 443   | tgram://bottoken/ChatID<br />tgram://bottoken/ChatID1/ChatID2/ChatIDN
| [Twitter](https://github.com/caronc/apprise/wiki/Notify_twitter) | twitter://  | (TCP) 443   | twitter://CKey/CSecret/AKey/ASecret<br/>twitter://user@CKey/CSecret/AKey/ASecret<br/>twitter://CKey/CSecret/AKey/ASecret/User1/User2/User2<br/>twitter://CKey/CSecret/AKey/ASecret?mode=tweet
| [Twist](https://github.com/caronc/apprise/wiki/Notify_twist) | twist://  | (TCP) 443   | twist://pasword:login<br/>twist://password:login/#channel<br/>twist://password:login/#team:channel<br/>twist://password:login/#team:channel1/channel2/#team3:channel
| [XBMC](https://github.com/caronc/apprise/wiki/Notify_xbmc) | xbmc:// or xbmcs://    | (TCP) 8080 or 443   | xbmc://hostname<br />xbmc://user@hostname<br />xbmc://user:password@hostname:port
| [XMPP](https://github.com/caronc/apprise/wiki/Notify_xmpp) | xmpp:// or xmpps://    | (TCP) 5222 or 5223   | xmpp://user:password@hostname<br />xmpps://user:password@hostname:port?jid=user@hostname/resource<br/>xmpps://user:password@hostname/target@myhost, target2@myhost/resource
| [Webex Teams (Cisco)](https://github.com/caronc/apprise/wiki/Notify_wxteams) | wxteams://  | (TCP) 443   | wxteams://Token
| [Zulip Chat](https://github.com/caronc/apprise/wiki/Notify_zulip) | zulip://  | (TCP) 443   | zulip://botname@Organization/Token<br />zulip://botname@Organization/Token/Stream<br />zulip://botname@Organization/Token/Email

## Installation
Certi is a docker based application that can be installed using docker compose:
```
version: "3.6"
services:
  certi:
    image: techblog/certi
    container_name: certi
    restart: always
    ports:
      - "8081:8081"
    environment:
      - API_KEY=
      - SLEEP_TIME=
      - NOTIFIERS=
      - LOG_LEVEL= 
    volumes:
      - ./data:/opt/certi/db
```

### Environment
* API_KEY - API key for [sslmate](https://sslmate.com/) search API.
* SLEEP_TIME - Time between scans (Default is 7200, which is 2 hours) - To prevent exceeding the search API limits.
* NOTIFIERS - List of [Supported Notifications](#Supported-Notifications)
* LOG_LEVEL - Optional valuse are: DEBUG (default), INFO, ERROR

### Volumes
In order to prevent data loss, it's recomended to mount a volume for the application Database.
"/opt/certi/db" is the path inside the container where the sqlite db is located. it will be created automatically upon application startup. 

### Ports
Certi has a managment api for the domains and certificates. by default the port is set to 8081.


## Managing the application
Certi has a small REST API endpoint created for easy managment. by default the port is set to to 8081. Swagger documentation can be accessed by adding "/docs" to the end of the url [http://docker:8081/docs].

The api have the following endpoints:
* domains/get (HTTP GET)- Get list of all monitored domains.
* domains/add/{DomainName} (HTTP PUT) - Add domain to monitored domains list.
* domains/delete/{DomainId} (HTTP DELETE) - Delete domain from the monitored domains list.
* /domains/active/{DomainId}/{state} (HTTP POST) - Set domain status to Active/InActive.
* /certificates/get (HTTP GET) - Get list off all certicicates that the Certi found.

[![Swagger Documentation](https://github.com/t0mer/certi/blob/main/screenshots/certi-swagger.png?raw=true "Swagger Documentation")](https://github.com/t0mer/certi/blob/main/screenshots/certi-swagger.png?raw=true "Swagger Documentation")

