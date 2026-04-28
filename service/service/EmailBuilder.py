from SOS_django_projects.settings import EMAIL_HOST_USER, BASE_DIR
from string import Template

class EmailBuilder:

    #Message template path 
    template_dir = BASE_DIR + "/" + "service/template/" 

    #Build sign up message
    @staticmethod
    def sign_up(params):
        dir =  EmailBuilder.template_dir + "newuser.html"
        #open the file
        filein = open(dir)
        #read it
        src = Template(filein.read())
        text = src.substitute(params)    
        return text

    #build change password message
    @staticmethod
    def change_password(params):
        dir =  EmailBuilder.template_dir + "changepassword.html"
        #open the file
        filein = open(dir)
        #read it
        src = Template(filein.read())
        text = src.substitute(params)    
        return text

    #Build forgot password message
    @staticmethod
    def forgot_password(params):
        dir =  EmailBuilder.template_dir + "forgotpassword.html"
        #open the file
        filein = open(dir)
        #read it
        src = Template(filein.read())
        text = src.substitute(params)    
        return text
