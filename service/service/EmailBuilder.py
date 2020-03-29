from SOS_django_projects.settings import EMAIL_HOST_USER, BASE_DIR
from string import Template

class EmailBuilder:

    template_dir = BASE_DIR + "/" + "service/template/" 

    @staticmethod
    def sign_up(params):
        dir =  EmailBuilder.template_dir + "newuser.html"
        #params = { 'login': "Sunil Sahu" }
        #open the file
        filein = open(dir)
        #read it
        src = Template(filein.read())
        text = src.substitute(params)    
        return text

    @staticmethod
    def change_password(params):
        dir =  EmailBuilder.template_dir + "changepassword.html"
        #params = { 'login': "Sunil Sahu" }
        #open the file
        filein = open(dir)
        #read it
        src = Template(filein.read())
        text = src.substitute(params)    
        return text

    @staticmethod
    def forgot_password(params):
        dir =  EmailBuilder.template_dir + "forgotpassword.html"
        #params = { 'login': "Sunil Sahu" }
        #open the file
        filein = open(dir)
        #read it
        src = Template(filein.read())
        text = src.substitute(params)    
        return text
