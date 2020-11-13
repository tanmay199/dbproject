from database import DBHELPER
from flask import Flask, render_template
app = Flask(__name__)
dbhelper=DBHELPER()
@app.route('/')
def index():
   alltrain = dbhelper.getalltrain() 
   return render_template('index.html', trains=alltrain)

if __name__ == '__main__':
   app.run(debug=True)