import os
import sys
import time
import json
import MySQLdb
import datetime

def main():
    try:
        conn = MySQLdb.connect(host   = 'localhost',
                               user   = '',
                               passwd = '',
                               db     = 'trec17',
                               port   = 3306)
        cur=conn.cursor()

        cur.execute('SELECT * FROM submit WHERE is_process = 0 limit 10')
        rows = cur.fetchall()
        for row in rows:
            id            = row[0]
            qid           = row[1]
            tid           = row[2] 
            client_id     = row[3]
            
            order = "curl -X POST -H 'Content-Type: application/json' http://scspc654.cs.uwaterloo.ca/tweet/%s/%s/%s -s -w %%{http_code}" % (qid, tid, client_id)
            print order
            responce = os.popen(order).read()
            if responce == '204':
                print 'success'
                cur.execute('UPDATE submit SET is_process = 1 WHERE id = %d' % id)
            elif responce[-3:] == '429':
                print 'rate limit exceeded'
                cur.execute('DELETE FROM submit WHERE is_process = 0 AND id = %d' % id)
            elif responce == '000':
            	print 'down'
            	cur.execute('DELETE FROM submit WHERE is_process = 0 AND id = %d' % id)
            else:            
                print 'ERROR:'
                print responce

            time.sleep(1)

        conn.commit()
    
        cur.close()
        conn.close()
    
        print 'process %d rows' % len(rows)
    except Exception, e:
        print e

if __name__ == "__main__":
    while True:
        print "main ..."
        main()
        
        print 'sleep 10 seconds ...'
        time.sleep(10)



