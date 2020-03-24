from django.shortcuts import render,redirect
from django.http import HttpResponse, FileResponse 
import datetime
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import xlwt
import logging
from service.models import User, Role



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
        
def excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="data.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['id', 'name', 'description' ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column 

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Role.objects.all().values_list('id', 'name', 'description',)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


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
@csrf_exempt
def login(request):
    if request.method=="POST":
        loginId=request.POST["loginId"]
        password=request.POST["password"]    
        if(loginId  == "admin" and password == "admin"):
                res = redirect('/test/html')
        else:
                message = "Invalid ID or Password"
                res = render(request,"test/Login.html",{"form":message})
    else:
        res=render(request,"test/Login.html")
    return res

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

