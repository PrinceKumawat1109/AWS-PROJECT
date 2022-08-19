from flask import Flask, render_template, request
import boto3
app = Flask(__name__)
dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id='AKIAYKK6KRNVJBIC7TVD',
                          aws_secret_access_key='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',
                          )
from boto3.dynamodb.conditions import Key, Attr
from werkzeug.utils import secure_filename
s3 = boto3.client('s3',
                  # aws_access_key_id='**',
                  aws_access_key_id='AKIAYKK6KRNVJBIC7TVD',
                  # aws_secret_access_key='**',
                  aws_secret_access_key='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',
                  )
BUCKET_NAME = 'upload181229'
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/signup', methods=['post'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        table = dynamodb.Table('users')
        table.put_item(
            Item={
                'name': name,
                'email': email,
                'password': password
            }
        )
        msg = "Registration Complete. Please Login to your account !"
        return render_template('login.html', msg=msg)
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/check', methods=['post'])
def check():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        table = dynamodb.Table('users')
        response = table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response['Items']
        name = items[0]['name']
        print(items[0]['password'])
        if password == items[0]['password']:
            return render_template("home.html", name=name)
    return render_template("login.html")
@app.route('/home')
def home():
    return render_template('home.html')
@app.route('/profile')
def profile():
    return render_template("upload.html")
@app.route('/upload', methods=['post'])
def upload():
    if request.method == 'POST':
        img = request.files['file']
        if img:
            filename = secure_filename(img.filename)
            img.save(filename)
            s3.upload_file(
                Bucket=BUCKET_NAME,
                Filename=filename,
                Key=filename
            )
            msg = "Upload Done ! "
    return render_template("upload.html", msg=msg)
if __name__ == "__main__":
    app.run(debug=True)