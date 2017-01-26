#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# QUESTIONS:
# Can form action be changed? If form isn't valid, we want to stay on page, if
#       it is valid, we want to go to another page.
import webapp2

page_header = """
<!DOCTYPE html>
<html>
    <head>
        <title>Signup Form</title>
    </head>
    <body>
"""

page_footer = """
    </body>
</html>
"""

signup_form = """
<h1>Sign Up!</h1>
<form method = "post" action="/" name="signup-form">
    <label>Username
        <input name="username" value="%(user_name)s"/>
    </label>
    <br>
    <label>Password
        <input name="password"/>
    </label>
    <br>
    <label>Verify Password
        <input name="verify"/>
    </label>
    <br>
    <label>Email (optional)
        <input name="email" value="%(email_addy)s"/>
    </label>
    <br>
    <button type="submit">Submit</button>
</form>
"""
content = page_header + signup_form + page_footer

class MainHandler(webapp2.RequestHandler):
    def write_form(self, user_name="", email_addy=""):
        self.response.out.write(content % {"user_name":user_name,
                                           "email_addy":email_addy})
    def get(self):
        self.write_form()
    def post(self):
        user_name = self.request.get("username")
        email_addy = self.request.get("email")
        if user_name:
            self.redirect("/welcome?username=" + user_name)
        else:
            self.write_form(user_name,email_addy)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get('username')
        welcome_msg = "Welcome, " + user_name + "!"
        self.response.out.write(welcome_msg)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
