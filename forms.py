from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email
 
class ContactForm(Form):
  name = StringField("Name",  [InputRequired("Please enter your name.")])
  email = StringField("Email",  [InputRequired("Please enter your email address.")])
  subject = StringField("Subject",  [InputRequired("Please enter a subject.")])
  message = TextAreaField("Message",  [InputRequired("Not including a message would be stupid")])
  submit = SubmitField("Send")