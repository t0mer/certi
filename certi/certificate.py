class certificate:
    def __init__(self, CertificateId,id,not_after,not_before,pubkey_sha256,tbs_sha256,issuer,dns_names,monitored_domain):
        self.CertificateId = CertificateId
        self.id = id
        self.tbs_sha256 = tbs_sha256
        self.pubkey_sha256 = pubkey_sha256
        self.issuer = issuer
        self.not_after = not_after
        self.not_before = not_before
        self.dns_names = dns_names
        self.monitored_domain = monitored_domain
