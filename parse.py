# -*- coding:utf-8 -*-
from urllib2 import urlopen, quote
from multiprocessing import Process, Queue
import xlrd, xlwt
import json, os, time, random

def isset( variable ):
	return variable in locals() or variable in globals()

def get_gps( data ):
	data = json.load( urlopen( "https://maps.googleapis.com/maps/api/geocode/json?address=" + data ) )
	if "OK" != data[ 'status' ]:
		return 0
	for coordinates in data[ 'results' ]:
		lat = coordinates[ 'geometry' ][ 'location' ][ 'lat' ]
		lng = coordinates[ 'geometry' ][ 'location' ][ 'lng' ]
	return ( lat,lng )

def th_run( wh2, i, j, data ):
	data = get_gps( quote( str( data ) ) )
	if data == 0:
		print "NO DATA"
		wh2.write( i, j, str( 0 ) )
		wh2.write( i, j + 1, str( 0 ) )
	else:
		#print data
		print data
		wh2.write( i, j, str( data[0] ) )
		wh2.write( i, j + 1, str( data[1] ) )
	return

s_time = time.time()
UPLOAD_FOLDER = os.path.dirname( os.path.abspath( __file__ ) )
filename = "test.xlsx"
path = UPLOAD_FOLDER
file_path = path + "/tmp/" + filename
new_filename = str( int( time.time() ) ) + str( int(random.random()*100) ) + '.xls'
new_file_path = path + "/ntmp/" + new_filename

wb = xlrd.open_workbook( file_path )
wh = wb.sheet_by_index( 0 )

row = wh.nrows
col = wh.ncols

geo_col = None

wb2 = xlwt.Workbook(encoding='utf-8')
wh2 = wb2.add_sheet(u'sheet0')

for i in range( col ):
	tmp = wh.cell_value( 0, i )
	wh2.write( 0, i, tmp )
	if "GEO" == tmp:
		geo_col = i

if geo_col == None:
	print "NO COLUMN"
	exit(0)
wh2.write( 0, col, 'Latitude')
wh2.write( 0, col+1, 'Longitude')

p = []

for i in range( 1, row ):
	for j in range( col ):
		wh2.write( i, j, wh.cell_value( i, j ) )
	#print quote( str( wh.cell_value( i,geo_col ) ) )
	p.append( Process( target=th_run, args=( wh2, i, col, wh.cell_value( i,geo_col ) ) ) )
	p[ i - 1 ].start()
for i in range( 1, row ):
	p[ i - 1 ].join()
print "write success : %s" % new_file_path
print str(time.time()-s_time)
wb2.save( new_file_path )