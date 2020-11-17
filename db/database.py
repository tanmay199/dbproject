import psycopg2

class DBHELPER:
    def __init__(self):
        self.conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="mypass")

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

    def register_user(self, username, first_name, last_name, credit_card, password, address):

        cur = self.conn.cursor()
        res = True
        try:
            cur.execute('''INSERT INTO userrecord(username, firstname,lastname,credit_card,password, address)
                VALUES(%s,%s,%s,%s,%s,%s)''',
                            (username, first_name, last_name, credit_card, password, address,))
        except:
            res = False
        

        cur.close()
        self.conn.commit()

        return res

    def check_login(self, username, password):
        cur = self.conn.cursor()
        res = True

        try:
            cur.execute(''' SELECT password from userrecord where username=%s''',
                            (username,))
        except:
            res = False

        dbpass = cur.fetchone()

        if password != dbpass[0]:
            res = False

        cur.close()
        self.conn.commit()

        return res