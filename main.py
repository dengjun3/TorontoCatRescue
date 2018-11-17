from flask import Flask, session, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from form_classes import LoginForm, CatInformation
import os
from flask_oauth import OAuth
import sys
import requests
import config



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






STATIC_URL_PATH = '/static/'
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
	session['access_token'] = access_token, ''
	return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
	return session.get('access_token')

@app.route('/shelter_upload', methods=['GET', 'POST'])
def shelter_upload():
	#Standard Authentication End
	access_token = session.get('access_token')
	if access_token is None:
		return redirect(url_for('login'))
	try:
		req = requests.post('https://www.googleapis.com/oauth2/v1/userinfo',
				data={'Authorization': 'OAuth '+ access_token[0]})
	except:
		session.pop('access_token', None)
		return redirect(url_for('login'))
	#Standard Authentication End

	form = CatInformation()
	if form.validate_on_submit():
		pho = form.photo.data
		filename = secure_filename(f.filename)
		f.save(os.path.join(app.instance_path, 'photos', filename))

		med_docs = form.medical_notes.data
		filename = secure_filename(f.filename)
		f.save(os.path.join(app.instance_path, 'medical_documents', filename))

		return redirect(url_for('index'))
	return render_template('shelter_upload.html', form=form)

@app.route('/intake_upload', methods=['GET', 'POST'])
def intake_upload():
	#Standard Authentication End
	access_token = session.get('access_token')
	if access_token is None:
		return redirect(url_for('login'))
	try:
		req = requests.post('https://www.googleapis.com/oauth2/v1/userinfo',
				data={'Authorization': 'OAuth '+ access_token[0]})
	except:
		session.pop('access_token', None)
		return redirect(url_for('login'))
	#Standard Authentication End

	form = CatInformation()
	if form.validate_on_submit():
		pho = form.photo.data
		filename = secure_filename(f.filename)
		f.save(os.path.join(app.instance_path, 'photos', filename))

		med_docs = form.medical_notes.data
		filename = secure_filename(f.filename)
		f.save(os.path.join(app.instance_path, 'medical_documents', filename))

		return redirect(url_for('index'))
	return render_template('intake_upload.html', form=form)

@app.route('/foster_upload', methods=['GET', 'POST'])
def foster_upload():
	#Standard Authentication End
	access_token = session.get('access_token')
	if access_token is None:
		return redirect(url_for('login'))
	try:
		req = requests.post('https://www.googleapis.com/oauth2/v1/userinfo',
				data={'Authorization': 'OAuth '+ access_token[0]})
	except:
		session.pop('access_token', None)
		return redirect(url_for('login'))
	#Standard Authentication End

	form = CatInformation()
	if form.validate_on_submit():
		pho = form.photo.data
		filename = secure_filename(f.filename)
		f.save(os.path.join(app.instance_path, 'photos', filename))

		med_docs = form.medical_notes.data
		filename = secure_filename(f.filename)
		f.save(os.path.join(app.instance_path, 'medical_documents', filename))

		return redirect(url_for('index'))
	return render_template('foster_upload.html', form=form)

@app.route('/')
def index():
	#Standard Authentication End
	access_token = session.get('access_token')
	if access_token is None:
		return redirect(url_for('login'))
	try:
		req = requests.post('https://www.googleapis.com/oauth2/v1/userinfo',
				data={'Authorization': 'OAuth '+ access_token[0]})
	except:
		session.pop('access_token', None)
		return redirect(url_for('login'))
	#Standard Authentication End


	form = LoginForm()
	return render_template('index.html', title='Sign In', form=form)

if __name__ == '__main__':
	app.run(debug=True)


