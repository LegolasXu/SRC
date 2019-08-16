import urllib, sys
import ssl, json
AK = "fGTcxxxxxxxxxxxxxk68c"
SK = "vKUxxxxxxxxxxxxxxxxxxxxxxxxxGq2u"
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'\
       '&client_id=%s'\
       '&client_secret=%s' % (AK, SK)
def GetToken():
    request = urllib2.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib2.urlopen(request)
    content = response.read()
    if (content):
        js = json.loads(content)
        return js['access_token']
    return None
print(js)