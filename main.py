from flask import *
from ast import literal_eval as le
from random import choice, randint
import json
from replit import db as data
import os
import base64
import re
drs = [False]
def cli():
	cookie = json.loads(base64.b64decode(request.cookies['i'].encode()).decode('utf-8'))
	un = cookie['un']
	passwd = cookie['passwd']
	if not un in data['users'].keys():
		return False
	if passwd == data['users'][un]['passwd']:
		return un
	else:
		return False
def dcli():
	cookie = json.loads(base64.b64decode(request.cookies['di'].encode()).decode('utf-8'))
	un = cookie['un']
	passwd = cookie['passwd']
	if not un in data['dev'].keys():
		return False
	if passwd == data['dev'][un]['passwd']:
		return un
	else:
		return False
app = Flask(__name__)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./','favicon.ico',mimetype='image/vnd.microsoft.icon')
@app.route('/')
def home():
	if 'i' in request.cookies:
		u = True
		un = cli()
		if not un:
			return '<h1>471: Hacker Caught.</h1><p>Invalid Login AFTER loging in. Hello, HACKER!!!</p>',471
	else:
		u = False
	return render_template('home.html',u=u)
@app.route('/dev/<n>/auth.js')
def script(n):
	resp = make_response(render_template('script.js',un=n))
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp
@app.route('/example')
def ex():
	return render_template('ex.html')
@app.route('/checklogin',methods=['POST'])
def cl():
	req = le(request.form['req'])
	if not request.form['un'] in data['users']:
		dt = {'status':False}
	else:
		dt = {'status':data['users'][request.form['un']]['passwd'] == request.form['passwd']}
	if dt['status']:
		if 'firstname' in req:
			dt['firstname'] = data['users'][request.form['un']]['name'][0]
		if 'lastname' in req:
			dt['lastname'] = data['users'][request.form['un']]['name'][1]
	resp = make_response(str(json.dumps(dt)))
	resp.headers['Access-Control-Allow-Origin'] = 'authjs.greatusername.repl.co'
	if json.loads(request.form['rmb']) and dt['status'] == True:
		resp.set_cookie('i',base64.b64encode(str(json.dumps({'un':request.form['un'],'passwd':request.form['passwd']})).encode()).decode('utf-8'))
	return resp
@app.route('/auth')
def auth():
	un = request.args.get('un')
	if un != None:
		if not un in data['dev'].keys():
			resp = make_response("<script>window.opener.done({'status':false,'error':'Invalid Username'});window.close();</script>")
		else:
			if request.args.get('url') in data['dev'][un]['url']:
				if un == 'authjs':
					blk = True
				else:
					blk = False
				if 'i' in request.cookies:
					if not und:
						return '<h1>471: Hacker Caught.</h1><p>Invalid Login AFTER loging in. Hello, HACKER!!!</p>',471
					ud = data['users'][und]
					p = le(str(request.args.get('p')))
					dat = {'status':True}
					if 'firstname' in p:
						dat['firstname'] = ud['name'][0]
					if 'lastname' in p:
						dat['lastname'] = ud['name'][1]
					if 'username' in p:
						dat['username'] = und
					return make_response(render_template('ali.html',name=data['dev'][un]['name'],un=un,p=request.args.get('p'),uname=und,data=json.dumps(dat)))
				elif request.headers['X-Replit-User-Id'] and request.headers['X-Replit-User-Id'] in data['replit']:
					und = data['replit'][request.headers['X-Replit-User-Id']]['un']
					ud = data['users'][und]
					p = le(str(request.args.get('p')))
					dat = {'status':True}
					if 'firstname' in p:
						dat['firstname'] = ud['name'][0]
					if 'lastname' in p:
						dat['lastname'] = ud['name'][1]
					if 'username' in p:
						dat['username'] = und
					if blk:
						resp = make_response(f'<script>window.close()</script>')
						resp.set_cookie('i',base64.b64encode(str(json.dumps({'un':data['replit'][request.headers['X-Replit-User-Id']]['un'],'passwd':ud['passwd']})).encode()).decode('utf-8'))
						return resp
					drs[0] = True
					return make_response(render_template('ali.html',name=data['dev'][un]['name'],un=un,p=request.args.get('p'),uname=und,data=json.dumps(dat)))
				resp = make_response(render_template('auth.html',name=data['dev'][un]['name'],un=un,p=request.args.get('p'),blk=blk))
			else:
				resp = make_response("<script>window.opener.done({'status':false,'error':'Invalid URL'});window.close();</script>")
	else:
		resp = make_response("<script>window.opener.done({'status':false,'error':'No Username'});window.close();</script>")
	return resp
@app.route('/test')
def test():
	return render_template('test.html')
@app.route('/signup')
def signup():
	return make_response(render_template('signup.html'))
@app.route('/_signup',methods=['POST'])
def _signup():
	if request.form['un'] in data['users']:
		return make_response(str(json.dumps({'status':False,'error':'Username Taken.'})))
	data['users'][request.form['un']] = {'passwd':request.form['passwd'],'name':[request.form['fn'],request.form['ln']]}
	resp = make_response('{"status":true}')
	resp.set_cookie('i',base64.b64encode(str(json.dumps({'un':request.form['un'],'passwd':request.form['passwd']})).encode()).decode('utf-8'))
	return resp
@app.route('/login')
def li():
	return render_template('login.html')
@app.route('/account')
def account():
	if 'i' in request.cookies:
		un = cli()
		if un:
			return render_template('account.html',fname=data['users'][un]['name'][0],lname=data['users'][un]['name'][1],un=str(un))
		else:
			return '<h1>471: Hacker Caught.</h1><p>Invalid Login AFTER loging in. Hello, HACKER!!!</p>',471
	else:
		return redirect('/login',302)
@app.route('/chgv',methods=['POST'])
def chgv():
	un = cli()
	if not un:
		return '<h1>471: Hacker Caught.</h1><p>Invalid Login AFTER loging in. Hello, HACKER!!!</p>',471
	ty = request.form['ty']
	v = request.form['v']
	n = ''
	if ty == 'fn':
		data['users'][un]['name'][0] = v
		n = 'First Name'
	elif ty == 'ln':
		n = 'Last Name'
		data['users'][un]['name'][1] = v
	resp = make_response(n)
	resp.headers['Access-Control-Allow-Origin'] = 'authjs.greatusername.repl.co'
	return resp
@app.route('/devsignup')
def dsu():
	return make_response(render_template('dsignup.html'))
@app.route('/_dsignup',methods=['POST'])
def _dsignup():
	if request.form['un'] in data['users']:
		return make_response(str(json.dumps({'status':False,'error':'Username Taken.'})))
	data['dev'][request.form['un']] = {'passwd':request.form['passwd'],'name':request.form['n'],'url':le(request.form['urls'])}
	resp = make_response('{"status":true}')
	resp.set_cookie('di',base64.b64encode(str(json.dumps({'un':request.form['un'],'passwd':request.form['passwd']})).encode()).decode('utf-8'))
	return resp
@app.route('/dev-account')
def devaccount():
	if not 'di' in request.cookies:
		return redirect('/devlogin',302)
	un = dcli()
	if not un:
		return '<h1>471: Hacker Caught.</h1><p>Invalid Login AFTER loging in. Hello, HACKER!!!</p>',471
	ud = data['dev'][un]
	urls1 = ud['url']
	urls = []
	url1 = ud['url'][0]
	c = 0
	for item in urls1:
		if not c == 0:
			urls.append(item)
		c+=1
	return make_response(render_template('dev_account.html',un=un,name=ud['name'],url1=url1,urls=json.dumps(urls)))
@app.route('/_dchgv',methods=['POST'])
def _dchgv():
	un = dcli()
	if not un:
		return '<h1>471: Hacker Caught.</h1><p>Invalid Login AFTER loging in. Hello, HACKER!!!</p>',471
	ty = request.form['ty']
	v = request.form['v']
	n = ''
	if ty == 'n':
		data['dev'][un]['name'] = v
		n = 'Name'
	elif re.match('url([0-9]+)',ty):
		number = int(re.match('url([0-9]+)',ty)[1])
		n = f'Url #{str(number)}'
		try:
			data['dev'][un]['url'][number-1] = v
		except IndexError:
			data['dev'][un]['url'].append(v)
	resp = make_response(n)
	resp.headers['Access-Control-Allow-Origin'] = 'authjs.greatusername.repl.co'
	return resp
@app.route('/devlogin')
def devlogin():
	return render_template('devlogin.html')
@app.route('/_devlogin',methods=['POST'])
def _devlogin():
	if not request.form['un'] in data['dev']:
		dt = {'status':False}
	else:
		dt = {'status':data['dev'][request.form['un']]['passwd'] == request.form['passwd']}
	resp = make_response(str(json.dumps(dt)))
	resp.headers['Access-Control-Allow-Origin'] = 'authjs.greatusername.repl.co'
	if dt['status']:
		resp.set_cookie('di',base64.b64encode(str(json.dumps({'un':request.form['un'],'passwd':request.form['passwd']})).encode()).decode('utf-8'))
	return resp
@app.route('/dev')
def dev():
	if 'di' in request.cookies:
		u = True
		un = dcli()
		if not un:
			return '<h1>471: Hacker Caught.</h1><p>Invalid Login AFTER loging in. Hello, HACKER!!!</p>',471
	else:
		u = False
	return render_template('dev.html',u=u)
@app.route("/status")
def status():
	return render_template('status.html')
app.run('0.0.0.0',port=9999)