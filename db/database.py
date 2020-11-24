import psycopg2
import shortuuid

no_of_seats_in_one_compartment = 6

class DBHELPER:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="1234")

    def getalltrain(self):
        cur = self.conn.cursor()
        res=True
        # execute a statement
        try:
            cur.execute('SELECT * from train')
        except:
            res = False
        if(res):
            trains = cur.fetchall()
        print(trains)
        # close the communication with the PostgreSQL
        cur.close()

        return trains

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

        dbpass="*"
        if(res):
            dbpass = cur.fetchone()

        if dbpass and password != dbpass[0]:
            res = False
        if not dbpass:
            res=False
        cur.close()
        self.conn.commit()

        return res

    def getallstations(self):
        cur = self.conn.cursor()
        res=True
        try:
            cur.execute('''select startpoint, endpoint from train''')
        except Exception as err:
            print(err)
            res = False
        startpoint = set()
        endpoint = set()
        if(res):
            for data in cur.fetchall():
                startpoint.add(data[0])
                endpoint.add(data[1])

        cur.close()

        return list(startpoint), list(endpoint)

    def gettrains(self, from_station, to_station, date):
        cur = self.conn.cursor()
        res=True
        try:
            cur.execute('''select train.trainID, dateofjourney, startpoint, endpoint, AC, nonAC FROM train LEFT JOIN schedule
            ON train.trainID = schedule.trainID where train.startpoint = %s and
             train.endpoint = %s and dateofjourney >= %s order by dateofjourney''',
                (from_station, to_station, date))
        except Exception as err:
            print(err)
            res = False
        trains=[]
        if(res):
            trains = cur.fetchall()[:5]
        cur.close()

        return trains

    def gettraindetails(self,trainid, date):
        cur =self.conn.cursor()
        res=True
        try:
            cur.execute('''select * from schedule where trainid=%s and dateofjourney=%s''',(trainid, date) )
        except Exception as err:
            print(err)
            res = False
        if(res):
            temp = cur.fetchone()
        cur.close()
        return temp

    def getroute(self, trainid):
        cur= self.conn.cursor()
        print("ROUTE TRAIN ID= ", trainid)
        res=True
        try:
            cur.execute('''select startpoint, endpoint from train where trainid=%s''',(trainid,))
        except Exception as err:
            print(err)
            res = False
        
        start,end="",""
        if(res):
            start,end= cur.fetchone()
        cur.close()
        return start, end

    def get_id_from_username(self,username):
        cur = self.conn.cursor()
        res=True
        try:
            cur.execute(''' SELECT id from userrecord where username=%s''',
                            (username,))
        except Exception as err:
            print(err)
            res = False
        userid=-1
        if(res):
            userid=cur.fetchone()[0]
        cur.close()
        return userid

    def findnextberthnum(self, filledseats,berthspercoach,seattype):
        #tickets are 1 indexed
        positions=['L','M','U']
        currcoachnum=(filledseats//berthspercoach)+1 #1 for 1 indexing
        seatnumtemp=(filledseats % berthspercoach)
        # this is actual seatnumber(serially) but the seat has 3 components so
        #seatnumtemp gives number of filled berths in curr coach(the serial seats not including position)
        #seatnumtemp=3*(actualseatnum)+position
        actualseatnum=seatnumtemp//3
        posn=seatnumtemp % 3
        # so the next to be filled seat is
        actualseatnum+=1 # 1 indexing
        #berth assigned= A_currcoachnum_actualseatnum+positions[posn]
        berth=seattype+'_'+str(currcoachnum)+'_'+str(actualseatnum)+positions[posn]
        return berth

    def findallberthnums(self,filledseats,berthspercoach,seattype,numseats):
        allberths=[]
        while(numseats):
            numseats-=1
            allberths.append(self.findnextberthnum(filledseats,berthspercoach,seattype))
            filledseats+=1
        return allberths

    def addusers(self, users, trainid, date, userid, filled_seats, seat_type):

        cur = self.conn.cursor()
        res = True
        try:
            pnr1=shortuuid.ShortUUID().random(length=10) #generate PNR
            #fetch user id
            #berth no. logic
            cur.execute('''INSERT INTO ticket(pnr, dateofjourney, trainID, user_id)
                    VALUES(%s,%s,%s,%s)''',
                            (pnr1, date, trainid, userid,))
            print("ticketdone")
            berths= self.findallberthnums(filled_seats, no_of_seats_in_one_compartment, seat_type, len(users))
            for j in range(len(users)):
                #print(PNR, i)
                i=users[j]
                print("here",i)
                berth = berths[j]
                cur.execute('''INSERT INTO ticketdetail(pnr, firstname, lastname, age, gender, berth)
                    VALUES(%s,%s,%s,%s,%s,%s)''',
                            (pnr1, i[0], i[1], i[2], i[3],berth,))
                
            
        except Exception as err:
            print(err)
            res = False
        
        cur.close()
        self.conn.commit()

        return res, pnr1, berths

    
    def checkavailability(self, trainid, date, seat_type):
        
        #cur = self.conn.cursor()
        print(trainid)
        cur = self.conn.cursor()
        res=True
        try:
            cur.execute('''SELECT get_occupied_berth(%s,%s,%s) ''',
                        (int(trainid),date,seat_type,))
        except Exception as err:
            print(err)
            res = False
        #print(res)
        filled_seats=0
        if(res):
            filled_seats=cur.fetchone()[0]
        res=True
        try:
            cur.execute('''SELECT AC, nonAC FROM schedule WHERE trainID=%s AND dateofjourney=%s''',
                        (trainid,date,))
        except:
            res = False
        ac_Seats,nonac_Seats=0,0
        if(res):
            (ac_Seats,nonac_Seats)=cur.fetchone()
        
        print("ac=",ac_Seats,"nonac=",nonac_Seats,"filled=", filled_seats)
        cur.close()
        seat=0
        if(seat_type=="A"):
            seat=ac_Seats
        else:
            seat=nonac_Seats
        available_seats= no_of_seats_in_one_compartment*seat - filled_seats
        return available_seats, filled_seats
        
        

