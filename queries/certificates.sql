 CREATE TABLE certificates (
  CertificateId int(11) NOT NULL AUTO_INCREMENT,
  id bigint(20) NOT NULL,
  tbs_sha256 varchar(255) NOT NULL,
  pubkey_sha256 varchar(255) NOT NULL,
  issuer varchar(255) DEFAULT NULL,
  not_before timestamp NULL DEFAULT NULL,
  not_after timestamp NULL DEFAULT NULL,
  dns_names varchar(255) DEFAULT NULL,
  monitored_domain varchar(255) DEFAULT NULL,
  PRIMARY KEY (CertificateId)
) 