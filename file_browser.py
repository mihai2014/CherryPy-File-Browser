import cherrypy
from jinja2 import Template

import signal
import os,sys
import platform

def signal_handler(signal, frame):
        print('You pressed Ctrl+Z!')
	#os.popen("fuser -k 8080/tcp")
	sys.exit(0)

signal.signal(signal.SIGTSTP, signal_handler)

def order(dir):
    dirs = []
    files = []
    all_items = []

    for item in os.listdir(dir):
	fullpath = os.path.join(dir, item)
	if os.path.isdir(fullpath): 
	    dirs.append(item)
	else: 
	    files.append(item)

    return sorted(dirs) + sorted(files)

def ls(dir):
    data  = []

    for item in order(dir):
        fullpath = os.path.join(dir, item)

        if os.path.isdir(fullpath):
	    data.append({'type':'D','href':'/change_directory/?path='+fullpath,'name':item,'info':''})
        else:
            info = os.stat(fullpath)
            #print os.path.getmtime(fullpath)
            describe = str(info.st_size) + " bytes"    #+ " " + str(info.st_atime) + " " + str(info.st_atime)
	    data.append({'type':'F','href':'/static'+fullpath,'name':item,'info':describe})

    return data

my_list = ""
display_type = 'local'
data = []

def traverse1(dir):
    global my_list

    my_list += '<ul>'

    for item in os.listdir(dir):

        fullpath = os.path.join(dir, item)
	
	if os.path.isdir(fullpath):
	    my_list += '<li>%s</li>' % item
	    #data.append({'type':'D','href':'#','name':item})
	else:
	    my_list += '<li><a href="%s">%s</a></li>' % ('/static'+fullpath ,item)
	    #data.append({'type':'F','href':'/static'+fullpath,'name':item})

        if os.path.isdir(fullpath):
            if os.listdir(fullpath) != []:
                traverse1(fullpath)

    my_list += '</ul>'


def traverse2(rootDir):
    global data

    #my_list += '<ul>'
    for dirName, subdirList, fileList in os.walk(rootDir):
	#type = 'D'
	#href = '#'
	#name = '/static'+dirName+'/'
	if len(fileList) == 0:
	    data.append({'type':'D','href':'#','name':'/static'+dirName})
        for fname in fileList:
	    #my_list += '<li><a href="%s">%s</a></li>' % ('/static'+dirName+'/'+fname ,'/static'+dirName+'/'+fname)
	    data.append({'type':'F','href':'/static'+dirName+'/'+fname,'name':dirName+'/'+fname})
    #my_list += '<ul>'





def get_data(dirName):
    global data, display_type, my_list
    data = []
    my_list = ""

    if display_type == 'tree1':
        traverse1(dirName)
	data = my_list

    if display_type == 'tree2':
        traverse2(dirName)

    if display_type == 'local':
        data = ls(dirName)

    index = open('public/index.html').read()
    template = Template(index)
    return template.render(data = data, type = display_type)


class root(object):

    @cherrypy.expose
    def index(self):
	return get_data('/')

    @cherrypy.expose
    def change_directory(self, path):
	return get_data(path)

    @cherrypy.expose
    def display(self, type):
	global display_type
	display_type = type


if __name__ == '__main__':
    print "System: " + platform.system()

    cherrypy.quickstart(root(),'/',"file_browser.conf")

#    alternate starting
#    conf = {
#        '/': {
#    	    'tools.gzip.on': True,
#            #'tools.staticdir.root': os.path.abspath(os.getcwd()),
#        'tools.staticdir.root': '/',
#    	    'tools.encode.encoding': 'utf-8',
#        },
#        'global': {
#            'server.socket_host': '0.0.0.0',
#            'server.socket_port': 8080,
#        },
#        '/static': {
#            'tools.staticdir.on': True,
#	    'tools.staticdir.dir': '.',
#        },
#	'/public': {
#	    'tools.staticdir.on': True,
#	    'tools.staticdir.dir': os.getcwd()+'/public/',
#	},
#    }
#    cherrypy.quickstart(root(), '/', conf)


