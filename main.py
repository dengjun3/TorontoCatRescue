from flask import Flask, session, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from form_classes import LoginForm, CatInformation
from google_sheets import find_permission, input_data, return_database
import os
from flask_oauth import OAuth
from flask_wtf import CsrfProtect
import sys
import requests
import config

csrf = CsrfProtect()

GOOGLE_CLIENT_ID = config.OAUTH_CONFIG['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = config.OAUTH_CONFIG['GOOGLE_CLIENT_SECRET']
REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console

oauth = OAuth()
google = oauth.remote_app('google',
						  base_url='https://www.google.com/accounts/',
						  authorize_url='https://accounts.google.com/o/oauth2/auth',
						  request_token_url=None,
						  request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
												'response_type': 'code'},
						  access_token_url='https://accounts.google.com/o/oauth2/token',
						  access_token_method='POST',
						  access_token_params={'grant_type': 'authorization_code'},
						  consumer_key=GOOGLE_CLIENT_ID,
						  consumer_secret=GOOGLE_CLIENT_SECRET)






STATIC_URL_PATH = '/static'
app = Flask(__name__, static_url_path=STATIC_URL_PATH)
app.config['SECRET_KEY'] = 'cats'



@app.route('/login')
def login():
	callback=url_for('authorized', _external=True)
	return google.authorize(callback=callback) 

@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
	access_token = resp['access_token']
	authorization_header = {"Authorization": "OAuth " + str(access_token)}
	r = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", 
						headers=authorization_header)
	print(r)
	print(r.json())
	session['access_token'] = access_token
	session['email'] = r.json()['email']
	return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
	return session.get('access_token')

@app.route('/shelter_upload', methods=['GET', 'POST'])
def shelter_upload():
	#Standard Authentication End
	access_token = session.get('access_token')
	email = session.get('email')
	
	if access_token is None:
		return redirect(url_for('login'))


	form = CatInformation()
	if form.validate_on_submit():
		input_data(form, 'shelter')

		if form.photo.data is not None:
			pho = form.photo.data
			filename = secure_filename(pho.filename)
			pho.save(os.path.join(app.instance_path, 'photos', filename))

		if form.medical_documents.data is not None:
			med_docs = form.medical_documents.data
			filename = secure_filename(med_docs.filename)
			med_docs.save(os.path.join(app.instance_path, 'medical_documents', filename))
		
		return redirect(url_for('index'))
	else:
		print(form.errors)
		
	return render_template('shelter_upload.html', form=form, title="new")

@app.route('/intake_upload', methods=['GET', 'POST'])
def intake_upload():
	#Standard Authentication End
	access_token = session.get('access_token')
	email = session.get('email')

	if access_token is None:
		return redirect(url_for('login'))

	form = CatInformation()
	if form.validate_on_submit():
		input_data(form, 'intake')
		
		if form.photo.data is not None:
			pho = form.photo.data
			filename = secure_filename(pho.filename)
			pho.save(os.path.join(app.instance_path, 'photos', filename))

		if form.medical_documents.data is not None:
			med_docs = form.medical_documents.data
			filename = secure_filename(med_docs.filename)
			med_docs.save(os.path.join(app.instance_path, 'medical_documents', filename))
		
		return redirect(url_for('index'))
	else:
		print(form.errors)

	return render_template('intake_upload.html', form=form)

@app.route('/foster_upload', methods=['GET', 'POST'])
def foster_upload():
	#Standard Authentication End
	access_token = session.get('access_token')
	email = session.get('email')

	if access_token is None:
		return redirect(url_for('login'))
	

	form = CatInformation()
	if form.validate_on_submit():
		input_data(form, 'foster')
		
		if form.photo.data is not None:
			pho = form.photo.data
			filename = secure_filename(pho.filename)
			pho.save(os.path.join(app.instance_path, 'photos', filename))

		if form.medical_documents.data is not None:
			med_docs = form.medical_documents.data
			filename = secure_filename(med_docs.filename)
			med_docs.save(os.path.join(app.instance_path, 'medical_documents', filename))
		
		return redirect(url_for('index'))
	else:
		print(form.errors)
	return render_template('foster_upload.html', form=form, title="new")

@app.route('/database')
def database():
	card = return_database()
	card.pop(0)
	return render_template('database.html', cards=card, title="data")

@app.route('/waitlist')
def waitlist():
	card = return_database()
	card = [i for i in card if i[20]=="shelter"]
	return render_template('database.html', cards=card, title="wait")


@app.route('/')
def index():
	
	#Standard Authentication End
	access_token = session.get('access_token')
	email = session.get('email')

	if access_token is None or email is None:
		return redirect(url_for('login'))

	permission = find_permission(email)
	print(permission)
	print(email)

	if permission == 'shelter':
		return redirect(url_for('shelter_upload'))
	elif permission == 'intake':
		return redirect(url_for('intake_upload'))
	elif permission == 'foster':
		return redirect(url_for('foster_upload'))
	else:
		return("User not in system")

	# form = LoginForm()
	# return render_template('index.html', title='Sign In', form=form)

if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.run(debug=True)


