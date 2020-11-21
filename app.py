from db.database import DBHELPER
from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)

dbhelper=DBHELPER()

@app.route('/')
def index():
   startpoints, endpoints = dbhelper.getallstations()
   return render_template('index.html', startpoints=startpoints, endpoints=endpoints)


@app.route('/traindetails' )
def no_of_berths():
   trainid=request.args.get('trainid')
   date=request.args.get('date')
   #rint(trainid)
   #print(date)
   temp= dbhelper.gettraindetails(trainid, date)
   print(temp)
   return render_template('traindetails.html')





@app.route('/search-trains', methods=['POST'])
def search_trains():
   if request.method=='POST':
      from_station = request.form['from']
      to_station = request.form['to']
      date = request.form['date']

      trains = dbhelper.gettrains(from_station, to_station, date)

      return jsonify(trains)

@app.route('/register', methods=['POST', 'GET'])
def register():
   if request.method == "GET":
      return render_template('register.html')
   else:
      first_name = request.form['first_name']
      last_name = request.form['last_name']
      credit_card = request.form['credit_card']
      password = request.form['password']
      address = request.form['address']
      username = request.form["username"]
      res = dbhelper.register_user(username, first_name, last_name, credit_card, password, address)
      if res:
         return redirect(url_for('login'))
      else:
         return render_template('register.html', err="User Already exists!")

@app.route('/login', methods=['POST', 'GET'])
def login():
   if request.method == "GET":
      return render_template('login.html')
   else:
      username = request.form["username"]
      password = request.form['password']

      res = dbhelper.check_login(username, password)
      if res:
         session['user'] = username
         return redirect(url_for('index'))
      else:
         return render_template('login.html', err="Invalid user or password")


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/book-ticket' , methods = ['GET','POST'])
def book_ticket():
   if request.method=="GET":
      seat_type= request.args["seat-type"]
      no_of_seats= request.args["No of Seats"]
      trainid= request.args["trainid"]
      date= request.args["date"]
      print(trainid, date)
      return render_template('bookticket.html', passenger=int(no_of_seats), seat_type=seat_type)
   else:
      no_of_seats=int(request.form["no_of_passengers"])
      for i in range(no_of_seats):
         print(request.form["Firstname"+str(i+1)])
      return "mallue"


if __name__ == '__main__':
   app.secret_key = '32f607a8a551499b9fda0bb8175cbdbc'
   app.run(debug=True)