import base64
import itertools

encrypted_message = b'''
EEgGBgoICxIdQ1lRT1IUGw4PFUlIWUwMGh8FDg8GGwFeS1VVVAwYGgQLCRwPSFlTTg4IBwEWDRhI 
VUlJTAcPDRYcDwYXHwxMQkFJBRoDBhAFDAYLDxpDWVFPUgYHBwECBQEdTENVVBsKDAMHEApMT09T 
ThgPBwtDVUtIExwGTE5bTkMOAgFUVBQ=
'''
key = b'kousiknandy'
decrypted_message = ''.join([chr(ord(a) ^ ord(b)) for (a,b) in \
                             zip(base64.b64decode(encrypted_message), \
                                 itertools.cycle(key))])
print decrypted_message
