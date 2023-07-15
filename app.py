from flask import Flask,request,render_template,jsonify
from src.components.emotions_detection import Detect
from src.components.model_training import BuildModel
import webbrowser


application=Flask(__name__)

app=application

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login_page():
    name=''
    password=''
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form.get('name')
        password = request.form.get('password')
    if name == 'upendra' and password == '12345':
        return render_template('index.html')
    else:
        message_alert = "Invalid username and password"
        return render_template('login.html',result = message_alert)

@app.route('/', methods=['GET','POST'])
def recommend():
    emotion = ''
    if request.method == 'GET':
        return render_template('index.html')
    else:
        emotion = request.form.get('menu')
    webbrowser.open(f"https://www.youtube.com/results?search_query={emotion}+song")
    return render_template('index.html',final_result = emotion)

@app.route('/myfunction')
def emotion_recommend():
    obj = BuildModel()
    train = "data/train"
    test = "data/test"
    train_generator,validation_generator,num_train,num_val,batch_size,num_epoch = obj.data_generation(train,test)      
    model = obj.model_creation()
    obj2 = Detect(model)
    emotion = obj2.display()
    webbrowser.open(f"https://www.youtube.com/results?search_query={emotion}+song")
    return render_template('index.html',final_result = emotion)


@app.route('/about')
def about_details():
    return render_template('about.html')

@app.route('/contact')
def contact_details():
    return render_template('contact.html')


if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)