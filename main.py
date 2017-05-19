#!/usr/bin/env python
import os
import jinja2
import webapp2

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("index.html")

    def post(self):
        my_number = 27
        first_try = int(self.request.get("first_try"))

        message_win = ""
        message_low = ""
        message_high = ""
        message_error = ""
        message_error2 = ""

        if first_try > 50 or first_try < 1:
            message_error = "I said between 1 and 50."
        elif first_try < my_number:
            message_high = "Try higher."
        elif first_try > my_number:
            message_low = "Try lower."
        elif first_try == my_number:
            message_win = "Congratulations. " + str(my_number) + " is my number."

        params = {"message_high": message_high, "message_low": message_low, "message_win": message_win, "message_error": message_error, "message_error2": message_error2}

        return self.render_template("index.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
], debug=True)

