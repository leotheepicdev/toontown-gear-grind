# TODO: Finish for Production.
serverpem = '''
-----BEGIN CERTIFICATE-----
MIICDDCCAXUCFBjTAM499DfwQQ8FzdmMHHcmjuReMA0GCSqGSIb3DQEBCwUAMEUx
CzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRl
cm5ldCBXaWRnaXRzIFB0eSBMdGQwHhcNMjAwMjI5MTkzNzQxWhcNMjEwMjI4MTkz
NzQxWjBFMQswCQYDVQQGEwJBVTETMBEGA1UECAwKU29tZS1TdGF0ZTEhMB8GA1UE
CgwYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMIGfMA0GCSqGSIb3DQEBAQUAA4GN
ADCBiQKBgQDhUaOTud87fEKhuPFnfUUhqNr1St0UycRQti94G4pnCiO8m9lNDEjp
X3/6/ftN/ipVrTkK8UCkwC+SLYkAuEjaE6cnT5NFiwPSnJZf0Q6AljAC8DexKJcq
V1tyFqbC2MNexjcc5UQ6kIGqX3SiRKyGcxxyLXiWfnSRmBzcqgZtEQIDAQABMA0G
CSqGSIb3DQEBCwUAA4GBABZqDrDG2Ly7wkHAbjuq8r6iKf82t9ZeTIB9l5v8vbcE
miMGYhOy0DxvbtTQ9gVhnVjmYV950fOr0QsmEbKahYCZ1AjVIFTJg2K9j2Anxf6S
F9iCkM6CiT006aAtI+2Lyx4PF/eJxJpPSx2FLRefCU28wMZ8nONXlcw0O2jjNJft
-----END CERTIFICATE-----
'''

clientpem = '''
-----BEGIN RSA PRIVATE KEY-----
MIICXQIBAAKBgQDhUaOTud87fEKhuPFnfUUhqNr1St0UycRQti94G4pnCiO8m9lN
DEjpX3/6/ftN/ipVrTkK8UCkwC+SLYkAuEjaE6cnT5NFiwPSnJZf0Q6AljAC8Dex
KJcqV1tyFqbC2MNexjcc5UQ6kIGqX3SiRKyGcxxyLXiWfnSRmBzcqgZtEQIDAQAB
AoGBALVJtG1VrfD0p7/rSABWYFsWuyWFWKAzPwsZqtPehNsm414LnylI6xkqR5Sw
6ZP1HibVOwI83iAwqZXZoVO88o9RRh/oxIcjxTqgUQot6LnFO+qfyXg64UFviP1K
/1SqqWEqTNSZOKAN3xbSRbWwTaDtgEHY1nY0qs6yYHq29FKpAkEA+zP++APvzXpm
fqSH2aRT6Bgf6ndkPk33mqJmTCFo62FFqMMdIUJ6fnW8nuyyiLDjEt8h5wp4LFP4
nIbhRV8OxwJBAOWfG7mAPwwKAgKQh3eefiLYkdILufb4L/xICfS8fELlxizVYmra
1jTeyMe0OSZ+WJrLN2Snx7aXFIZpVy7drWcCQDZcDCLTh0Mp56AkLpm0a8vf3Jg6
eeDZsmkuF4EGAdRd2lsozdbysdtH0yd5BTF7RchBrO54X4UILtaAgaMnbOUCQGCV
MiYuiVZZB0to23I3Gjsx+PPutsPo1NY6vuVQOrwwxdCp2IG1lpAafT1y0u8cCczi
WWRfJiPpHFsFCATQfVUCQQCauX3D2f1taFNGCBi6iVnnjTWPzLcOlLrwJlaHI1TT
4AP49YDfBceRpx3NXjKSKX/Hn+lLPhumup7Wsb71/bqM
-----END RSA PRIVATE KEY-----
'''

certificate = '''
'''

def getProdCertificate():
	return certificate
