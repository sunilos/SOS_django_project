from django.shortcuts import render
from django.http import HttpResponse, FileResponse 
import datetime
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def index(request):
    now = datetime.datetime.now()
    html = "<h1>Hello %s.</h1>" % now
    return HttpResponse(html)


def welcome(request):
    now = datetime.datetime.now()
    html = "<h1>Welcome in test app at %s.</h1>" % now
    return HttpResponse(html)

def info(request):
    now = datetime.datetime.now()
    html = "<h1>Info at %s.</h1>" % now
    html +=  "<OL>"
    html +=  "<LI>Http Method: " + request.method 
    html +=  "<LI>Path: " + request.path 
    html +=  "<LI>Path Info: " + request.path_info 
    html += "<p>File Path: " + __file__ 
    html +=  "</OL>"

    res = HttpResponse(html)
    return res

def tempate(request):
    msg = "Sunil OS"
    res = render(request,"test/Welcome.html",{"message":msg})
    return res

def pdf(request):
    with open('G:/sunRays/python/dJango-projects/SOS_django_projects/Test/template/test/a.pdf',encoding="utf8") as pdf:
        response = HttpResponse(pdf.read(), mimetype='application/pdf')
        response['Content-Disposition'] = 'inline; filename=a.pdf'
        return response
        
def exel(request):
    res = HttpResponse("Excel")
    return res

@csrf_exempt
def json(request):
    data=[{"name":"Ram","address":"Indore"},{"name":"Shyam","address":"Bhopal"}]
    res = JsonResponse(data,safe=False)
    return res


#readGet?firstName=Ram&lastName=Sharma
def readGetParams(request):
    fn = request.GET["firstName"]
    ln = request.GET["lastName"]   
    res = render(request,"test/HelloParam.html",{"firstName":fn, "lastName": ln})
    return res

#readPost
def readPostParams(request):
    fn = request.POST["firstName"]
    ln = request.POST["lastName"]    
    res = render(request,"test/HelloParam.html",{"firstName":fn, "lastName": ln})
    return res

#Login 
def login(request):
    pass

#Generate custom pdf
def GenPdf(request):
        pdf =render_to_pdf('test/Welcome.html')

        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse("Not Found")

def render_to_pdf(template_src, context_dict={}):
        template = get_template(template_src)
        html  = template.render({"message":"pdf response"})
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

