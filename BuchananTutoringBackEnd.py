from flask import Flask, request, render_template
from models import *
import json
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import DoesNotExist
import datetime
import hashlib

app = Flask(__name__)
app.register_blueprint(models_app)


FAILURE = "%s" % str(json.dumps({"Success": "False"}))
SUCCESS = "%s" % str(json.dumps({"Success": "True"}))





@app.route('/bhs/login/', methods= ['POST'])
def login():
    if not request.method == 'POST':
        return FAILURE
    elif request.values.get('username') and request.values.get('password'):
        try:
            User.get(request.values.get('password') == User.zanglePassword)
            if User.zangleID == request.values.get('username'):
                return SUCCESS
        except DoesNotExist:
            return FAILURE
    return FAILURE

@app.route('/bhs/create/', methods=['POST'])
def create():
    if not request.method == 'POST':
        return FAILURE
    elif request.values.get('username') and request.values.get('password') and request.values.get('firstName') and request.values.get('lastName'):
        account = User(firstName=request.values.get('firstName'), lastName = request.values.get('lastName'))
        account.zangleID = request.values.get('username')
        account.zanglePassword =  str(hashlib.md5(request.values.get('password').encode('utf-8')).hexdigest())
        account.created = datetime.datetime.now()
        account.save()
        return SUCCESS
    return FAILURE

@app.route('/bhs/classroom/', methods=['POST'])
@app.route('/bhs/classroom/<int:cid>', methods=['GET'])
def classroom(cid=0):
    if cid > 0 and request.method == 'GET':
        try:
            cass = Class.get(cid == Class.id)
        except DoesNotExist:
            return FAILURE
        return "%s" % str(json.dumps(model_to_dict(cass)))
    elif request.method == "POST" and request.values.get('code'):
        _class = Class(classCode=request.values.get('code'))
        if request.values.get('author'):
            _class.bookTitle = request.values.get('author')
        _class.save()
        return SUCCESS

@app.route('/bhs/answers/', methods=['POST'])
@app.route('/bhs/answers/<int:aid>', methods=['GET'])
def answer(aid=0):
    if aid > 0 and request.method == 'GET':
        try:
            answer = Answer.get(aid == Answer.aid)
        except DoesNotExist:
            return FAILURE
        return str(model_to_dict(answer))

    if request.method == "POST" and request.values.get('qid'):
        try:
            Question.get(request.values.get('qid') == Question.id)
        except:
            return FAILURE

        ans = Answer.create(id=request.values.get('qid'))
        if request.values.get('body'):
            ans.body = request.values.get('body')
        elif request.values.get('image'):
            ans.image = request.values.get('image')
        if not ans.body and not ans.image:
            return FAILURE
        ans.save()
        return SUCCESS
    return FAILURE

@app.route('/bhs/questions/', methods=['POST'])
@app.route('/bhs/questions/<int:questionID>', methods=['GET'])
def question(questionID=0):
    if questionID > 0 and request.method == 'GET': #retrieve question
        try:
            _question = Question.get(Question.id == questionID)
        except DoesNotExist:
            return "%s" % str(json.dumps({"Success": "False"}))

        return '%s' % str(model_to_dict(_question))
    elif request.method == 'POST':
        if request.values.get('zangleCreator') or request.values.get('classIndex'):
            if request.values.get('body') or request.values.get('image'):
                if(request.values.get('bookTitle')): title = request.values.get('bookTitle')
                if(request.values.get('pageNumber')): pageNumber = request.values.get('pageNumber')
                x = Question.create(body=request.values.get('body'))

                return str(model_to_dict(x))

            pass
        return 'False'



def valid_login(username, password):
    pass


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def hello_world():
    return render_template('index.html')




if __name__ == '__main__':
    app.run()
