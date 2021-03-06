import jinja2
import os
import webapp2
import logging
from datetime import datetime
from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.api import users
from webapp2_extras import sessions
from google.appengine.api import memcache
from SecurityUtils import AccessOK, AccessOKNew

from models import Papers


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
jinja_environment.filters['AccessOK'] = AccessOK
jinja_environment.filters['AccessOKNew'] = AccessOKNew

#jinja_environment = jinja2.Environment(autoescape=True,
#    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)
		
    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

class DisplayHome(BaseHandler):
    def get(self):

#        q = Papers.query(Papers.Category != 'Feedback').order(Papers.Category, -Papers.CreatedDate)
        q = Papers.query(Papers.Category != 'Feedback').order(Papers.Category, -Papers.CreatedDate)
        papers = q.fetch(10)

        if papers:
            Havepapers = True
        else:
            Havepapers = False
		
        logout = None
        login = None
        currentuser = users.get_current_user()
        if currentuser:
              logout = users.create_logout_url('/' )
        else:
              login = users.create_login_url('/')

        template_values = {'content1': 'No content yet.', 'papers':papers, 'Havepapers':Havepapers, 'currentuser':currentuser, 'login':login, 'logout': logout}

        template = jinja_environment.get_template('Home.html')
        jinja_environment.filters['AccessOK'] = AccessOK
        jinja_environment.filters['AccessOKNew'] = AccessOKNew

        self.response.out.write(template.render(template_values))

class DisplayTransIntro(BaseHandler):
    def get(self):

        q = Papers.query(Papers.Category != 'Feedback').order(Papers.Category, -Papers.CreatedDate)
        papers = q.fetch(10)

        if papers:
            Havepapers = True
        else:
            Havepapers = False
		
        logout = None
        login = None
        currentuser = users.get_current_user()
        if currentuser:
              logout = users.create_logout_url('/' )
        else:
              login = users.create_login_url('/')

        template_values = {'content1': 'No content yet.', 'papers':papers, 'Havepapers':Havepapers, 'currentuser':currentuser, 'login':login, 'logout': logout}

        template = jinja_environment.get_template('TransIntro.html')
        jinja_environment.filters['AccessOK'] = AccessOK
        jinja_environment.filters['AccessOKNew'] = AccessOKNew

        self.response.out.write(template.render(template_values))
