#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import flask
import json
from time import gmtime, strftime
import uuid

app = flask.Flask(__name__)

def _handle_http_exception(e):
	try:
		code = e.code
		text = e.description
	except:
		# если изменились атрибуты класса e.__class__
		code = 500
		text = "Internal server error, %s" % (e.__class__.__name__)
	html = flask.render_template("http.tpl", text=text, code=code)
	resp = flask.make_response(html, code)
	return resp

from werkzeug.exceptions import default_exceptions
for code in default_exceptions:
	app.errorhandler(code)(_handle_http_exception)

from functools import wraps
def _catch_custom_exception(func):
	@wraps(func)
	def decorated_function(*args, **kwargs):
		try:
			return func(*args, **kwargs)
		except Exception as e:
			code = 500
			text = "%s, %s" % (e.__class__.__name__,str(e))
			html = flask.render_template("http.tpl", text=text, code=code)
			resp = flask.make_response(html, code)
			return resp
	return decorated_function

def first(a):
	return next(iter(a or []), None)

@app.route('/api/',defaults={"path":""},methods=["GET"])
@app.route('/api/<path:path>',methods=["GET"])
@_catch_custom_exception
def api(path):
	headers = flask.request.headers
	print headers
	print path
	sys.stdout.flush()
	# i = 0/0
	# return "Default Value"
	code = 200
	text = "Sample value"
	html = flask.render_template("html.tpl", text=text, code=code)
	resp = flask.make_response(html, code)
	return resp

from Cookie import SimpleCookie
@app.route('/auth/',defaults={"path":""},methods=["GET"])
@app.route('/auth/<path:path>',methods=["GET"])
@_catch_custom_exception
def auth(path):
	headers = flask.request.headers

	c = headers.get("Cookie")
	c = str(c)
	s = SimpleCookie(c)
	prefix = "vk_app_"
	prefix0 = filter(lambda x: x.startswith(prefix), s)
	print type(prefix0),prefix0
	vkJSON = c[len(prefix0):]
	print vkJSON

	sys.stdout.flush()
	code = 200
	text = "Sample value"
	html = flask.render_template("auth.tpl", text=text, code=code)
	resp = flask.make_response(html, code)
	return resp

from werkzeug.contrib.fixers import ProxyFix
app.debug = True
app.wsgi_app = ProxyFix(app.wsgi_app)

if __name__ == "__main__":
	app.run(host = "127.0.0.1", port = 7000, threaded = True) #, debug = False)
