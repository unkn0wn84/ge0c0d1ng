# -*- coding: utf-8 -*-

from flask import Flask, request, redirect, url_for, render_template
import os, time, random

UPLOAD_FOLDER = os.path.dirname( os.path.abspath( __file__ ) ) + "/tmp"
UPLOAD_FOLDER_2 = os.path.dirname( os.path.abspath( __file__ ) ) + "/ntmp"
ALLOW_LIST = [ 'xlsx' ]
ALLOWED_EXTENSIONS = set( ALLOW_LIST )
parespy = os.path.join( os.path.dirname( os.path.abspath( __file__ ) ) , "parse.py" )

print "[ * ] Server Info"
print "Upload Path : %s" % UPLOAD_FOLDER
print "Allowed File type : %s" % "".join( ALLOW_LIST )
print parespy
os.system( "mkdir %s"  % UPLOAD_FOLDER  )
os.system( "mkdir %s"  % UPLOAD_FOLDER_2  )


app = Flask(__name__)
app.config[ 'UPLOAD_FOLDER' ] = UPLOAD_FOLDER

def allowed_file( filename ):
    return '.' in filename and filename.rsplit( '.', 1 )[1] in ALLOWED_EXTENSIONS

@app.route( '/' )
def app_main():
    return render_template( 'main.html' )

@app.route( '/upload', methods=[ 'POST' ] )
def upload_file():
	file = request.files[ 'file' ]
	if file and allowed_file(file.filename):
		email = request.form[ 'email' ]
		filename = str( int( time.time() ) ) + str( int(random.random()*100) ) + ALLOW_LIST[0]
		file.save( os.path.join( app.config['UPLOAD_FOLDER'], filename ) )
		os.system( "python %s %s %s &" % ( parespy, filename, email ) )
		return "<script>alert('result send to : %s ');location.href='/'</script>" % email
	return "<script>alert('not allowed file type');history.back();</script>"

if __name__ == '__main__':
    app.run()