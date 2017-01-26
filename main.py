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
# Can python variable names match html element names?
# Why didn't /w work in character class for re.compile for username?

import webapp2
import re

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
        <input name="username" value="%(user_name)s"/> &#8198; <label>%(username_msg)s</label>
    </label>
    <br>
    <label>Password
        <input name="password"/> &#8198; <label>%(password_msg)s</label>
    </label>
    <br>
    <label>Verify Password
        <input name="verify"/> &#8198; <label>%(verify_msg)s</label>
    </label>
    <br>
    <label>Email (optional)
        <input name="email" value="%(email_addy)s"/> &#8198; <label>%(email_msg)s</label>
    </label>
    <br>
    <button type="submit">Submit</button>
</form>
"""
content = page_header + signup_form + page_footer


# re (regex) module usage notes: to avoid issues with both
# python and regex module using \ to escape special
# characters, use python's raw string notation. Prefix string
# literal with 'r'
# $ signifies end of string before a newline
def is_valid_username(username):
    # \w should match any alphanumeric character == [a-zA-Z0-9_]
    # - matches a literal - (in Udacity notes, provided
    # r"^[a-zA-Z0-9_-]{3,20}$", I changed it to [/w-] after
    # reading re HOWTO). /w didn't work, went back to Udacity's
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    return USER_RE.match(username)
def is_valid_password(password):
    # . matches anything except a newline character
    PASSWORD_RE = re.compile(r"^.{3,20}$")
    return PASSWORD_RE.match(password)
def is_valid_email(email):
    # \S matches any non-whitespace character
    # . is literal in this case (I think because of the 'r' prefix)
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
    return EMAIL_RE.match(email)

def validity_check(username, password, verify, email):
    #error_msg = "<style color=red><b>%s</b></style>"
    error_flag = False
    username_msg = password_msg = verify_msg = email_msg = ""
    if not is_valid_username(username):
        username_msg = "Please provide a valid username"
        error_flag = True
    if not is_valid_password(password):
        password_msg = "Please provide a valid password"
        error_flag = True
    if password != verify:
        verify_msg = "Verify Password does not match Password"
        error_flag = True
    if len(email) > 0:
        if not is_valid_email(email):
            email_msg = "Please provide a valid email"
            error_flag = True
    if error_flag:
        return (username_msg, password_msg, verify_msg, email_msg)

class MainHandler(webapp2.RequestHandler):
    def write_form(self, user_name="", email_addy="", username_msg="",
                    password_msg="", verify_msg="", email_msg=""):
        self.response.out.write(content % {"user_name":user_name,
                                           "email_addy":email_addy,
                                           "username_msg":username_msg,
                                           "password_msg":password_msg,
                                           "verify_msg":verify_msg,
                                           "email_msg":email_msg})
    def get(self):
        self.write_form()
    def post(self):
        user_name = self.request.get("username")
        pass_word = self.request.get("password")
        verify_password = self.request.get("verify")
        email_addy = self.request.get("email")
        invalid_result = validity_check(user_name,pass_word,verify_password,
                                        email_addy)
        if not invalid_result:
            self.redirect("/welcome?username=" + user_name)
        else:
            self.write_form(user_name,email_addy,invalid_result[0],
                            invalid_result[1],invalid_result[2],
                            invalid_result[3])

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        user_name = self.request.get('username')
        welcome_msg = "Welcome, " + user_name + "!"
        self.response.out.write(welcome_msg)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
