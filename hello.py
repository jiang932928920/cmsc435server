from flask import Flask, render_template, redirect, session, jsonify
from flask_wtf import FlaskForm
from flask_pymongo import PyMongo
from wtforms import StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import InputRequired, NumberRange, Length, Email
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'
app.config["MONGO_URI"] = "mongodb://localhost:27017/my_database"
mongo = PyMongo(app)

class SubmissionForm(FlaskForm):
    name = StringField('name', validators=[InputRequired(), Length(min=4, max=30)])
    message = StringField('message', validators=[InputRequired(), Length(min=3, max=50)])
    submit = SubmitField('submit')


@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('base.html', time=current_time())

@app.route('/form', methods=['GET', 'POST'])
def submit():
    form = SubmissionForm()
    if form.validate():
        info = {
            'name': form.name.data,
            'message': form.message.data,
            'date': current_time()
        }
        mongo.db.information.insert_one(info)

    if form.validate_on_submit():
        return redirect('/')
    return render_template('form.html', form=form)

@app.route('/information', methods=['GET'])
def get_all_information():
    information = mongo.db.information
    output = []
    for i in information.find():
        output.append({'name': i['name'], 'message':i['message'], 'date':i['date']})
    return jsonify({'result':output})


def current_time() -> str:
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')

# Not a view function, used for creating a string for the current time.
if __name__ == '__main__':
    app.run(debug=True)

