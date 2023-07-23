from flask import Flask,request,render_template,jsonify,flash,Response
from src.components.emotions_detection import Detect
from src.components.model_training import BuildModel
from src.components.youtube_data_scrap import you_scrap
from src.logger import logging
from src.utils import sqli_connect
import cv2



application=Flask(__name__)
app=application
app.secret_key = "super secret key"

#==================Home page===================================
@app.route('/')
def sangeet():
    return render_template('front.html')

#================Login=========================================
@app.route('/login',methods=['GET','POST'])
def login_page():
    name=''
    password=''
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get('name')
        password = request.form.get('password')
    conn = sqli_connect('database')
    cursor = conn.cursor()
    query = "SELECT username, password from user_data where username='{usrname}' and password='{pswd}';".format(usrname=name,pswd=password)
    rows = cursor.execute(query)
    rows = rows.fetchall()
    if len(rows) == 1:
        flash(f"Hi {name}, welcome to Sangeet")
        return render_template('index.html')
    else:
        message_alert = "Invalid username and password"
        flash(message_alert)
        return render_template('login.html',result = message_alert)


#==============register================================
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')  
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
    if password == confirm_password:   
        conn = sqli_connect('database')
        cursor = conn.cursor()     
        query = "INSERT INTO user_data VALUES('{u}','{e}','{p}');".format(u=username,e=email,p=password)
        try:
            cursor.execute(query)
            conn.commit()
            conn.close()
            flash("Registered Successfully")
            return render_template('register.html')
        except Exception as e:
            flash("User already exist")
            logging.info(f"{e}") 
            return render_template('register.html')
    else:
        flash("Password do not match with confirm password")
        return render_template('register.html') 
    
#=====================Dashboard===============================
@app.route('/go')
def base():
    return render_template('base.html')

@app.route('/show_div')
def show_div():
    return jsonify(success=True)
     
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/home', methods=['GET','POST'])
def recommend():
    emotion = ''
    if request.method == 'GET':
        return render_template('index.html')
    else:
        emotion = request.form.get('menu')
    obj3 = you_scrap()
    get_data = obj3.extract(emotion+' song')
    return render_template('songs.html', data = get_data)



@app.route('/myfunction')
def emotion_recommend():
    if request.method == 'POST':
        return render_template('songs.html')
    obj = BuildModel()
    train = "data/train"
    test = "data/test"
    train_generator,validation_generator,num_train,num_val,batch_size,num_epoch = obj.data_generation(train,test)      
    model = obj.model_creation()
    obj2 = Detect(model)
    emotion = obj2.display()
    final_emotion = emotion+" song"
    if final_emotion=="Sad song":
        final_emotion = "sad lofi song"
    obj3 = you_scrap()
    get_data = obj3.extract(final_emotion)
    return render_template('songs.html',data=get_data)




@app.route('/video')
def video_feed():
    return Response(mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/about')
def about_details():
    return render_template('about.html')

@app.route('/contact')
def contact_details():
    return render_template('contact.html')




if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)