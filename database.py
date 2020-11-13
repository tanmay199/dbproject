import psycopg2

class DBHELPER:
    def __init__(self):
        self.conn = psycopg2.connect(
        host="localhost",
        database="project",
        user="postgres",
        password="1234")

    def getalltrain(self):
        cur = self.conn.cursor()
        
	    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT * from train')

        # display the PostgreSQL database server version
        db_version = cur.fetchall()
        print(db_version)
       
	    # close the communication with the PostgreSQL
        cur.close()

        return db_version
