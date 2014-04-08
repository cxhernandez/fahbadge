import os, optparse, uuid, urlparse, time, tornado, os, sys
import cPickle as pickle
from userinfuser.ui_api import *
from userinfuser.ui_constants import *
from StringIO import StringIO
from threading import Lock
from urllib import urlencode
from pymongo import Connection
import newrelic.agent
import tornado.ioloop
from tornado.web import (RequestHandler, StaticFileHandler, Application,asynchronous)
from tornado.websocket import WebSocketHandler
from tornado.httpclient import AsyncHTTPClient

__ACTIVATE__ = "activation.key"

apiKey = pickle.load(open(__ACTIVATE__))

newrelic.agent.initialize('newrelic.ini') 

#Set up MONGO CLIENT
__DB__ = 'MONGOHQ_URL'

#Declare async
HTTP_CLIENT = AsyncHTTPClient()

#-----------------------------------------------------------------------------
# TASKS
#-----------------------------------------------------------------------------

#Connect to MONGODB
def connect_to_mongo():
    if __DB__ in os.environ:
        c = Connection(os.environ[__DB__])
    else:
        print "if youre developing locally, you need to get the MONGOLAB_URI"
        print 'env variable. run "heroku config" at the command line and'
        print 'it should give you the right string'
        c = Connection()
    #THIS IS APP SPECIFIC. PLEASE CHANGE APPLICATION ID.
    return c.app22870053 
    
DATABASE = connect_to_mongo()
print DATABASE.collection_names()

# GET USER OPTIONS
def parse_cmdln():
    parser=optparse.OptionParser()
    parser.add_option('-p','--port',dest='port',type='int', default=5000) #OPTION TO CHANGE HOST SERVER PORT
    (options, args) = parser.parse_args()
    return (options, args)

#CREATES HOST SESSION AND LOGS USER IP INFO
class Session(object):
    """REALLLY CRAPPY SESSIONS FOR TORNADO VIA MONGODB
    """
    collection = DATABASE.sessions
    
    def __init__(self, request):
        data = {
            'ip_address': request.remote_ip,
            'user_agent':  request.headers.get('User-Agent')
        }
        result = self.collection.find_one(data)
        if result is None:
            # create new data
            self.collection.insert(data)
            self.data = data
        else:
            self.data = result

    def get(self, attr, default=None):
        return self.data.get(attr, default)
    
    def put(self, attr, value):
        self.collection.remove(self.data)
        self.data[attr] = value
        self.collection.insert(self.data)
    
    def __repr__(self):
        return str(self.data)
 
#PREVENTS FREQUENT REQUESTS
class RunHandler(RequestHandler):
    # how often should we allow execution
    max_request_frequency = 10  # seconds

    def log(self, msg):
        print msg
        
    def get(self):
        if self.validate_request_frequency():
            request_id = str(uuid.uuid4())
            HTTP_CLIENT.fetch('localhost', method='POST', callback=self.log)
            self.write()
            
    def validate_request_frequency(self):
        """Check that the user isn't requesting to run too often"""
        session = Session(self.request)
        last_run = session.get('last_run')
        if last_run is not None:
            if (time.time() - last_run) < self.max_request_frequency:
                self.write("You're being a little too eager, no?")
                return False
        session.put('last_run', time.time())

        return True
        
#COUNTS REQUESTS
class IndexHandler(StaticFileHandler):
    def get(self):
        session = Session(self.request)
        session.put('indexcounts', session.get('indexcounts', 0) + 1)
        return super(IndexHandler, self).get('index.html')
 
#HANDLES POSTS
class UploadHandler(tornado.web.RequestHandler):
    def post(self):
        user = self.get_argument('user')
 
#-----------------------------------------------------------------------------
# STATIC CONTENT DECLARATIONS
#-----------------------------------------------------------------------------
application = tornado.web.Application([
        (r'/run', RunHandler),
        (r"/process", UploadHandler),
        (r'/', IndexHandler, {'path': 'public'}),
        (r'/js/(.*)', StaticFileHandler, {'path': 'public/js'}),
        (r'/css/(.*)', StaticFileHandler, {'path': 'public/css'}),
        (r'/images/(.*)', StaticFileHandler, {'path': 'public/images'}),
        (r'/help/(.*)', StaticFileHandler, {'path': 'public/help'}),
        ], debug=True)
 
#-----------------------------------------------------------------------------
# MAIN
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    (options,args)=parse_cmdln()
    port = int(os.environ.get('PORT', options.port))
    application.listen(port)
    print "fahbadge is starting on port %s" % options.port
    tornado.ioloop.IOLoop.instance().start()