#Python to create a form


#Imports the libraries we need to create a form
from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email

#Creates a contact form class
class ContactForm(Form):
  #Creates the input fields and messages for the form
  name = StringField("Name",  [InputRequired("Please enter your name.")])
  email = StringField("Email",  [InputRequired("Please enter your email address.")])
  subject = StringField("Subject",  [InputRequired("Please enter a subject.")])
  message = TextAreaField("Message",  [InputRequired("Not including a message would be very silly! :)")])
  submit = SubmitField("Send")