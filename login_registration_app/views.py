from django.shortcuts import render, redirect
from .models import Register, Message, Comment
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    print(request.POST)
    validationErrors = Register.objects.registrationValidator(request.POST)
    if len(validationErrors) > 0:
        for key, value in validationErrors.items():
            messages.error(request, value)
        return redirect('/register')
    hashPW = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    newuser = Register.objects.create(first_name= request.POST['fname'], last_name= request.POST ['lname'], email= request.POST ['email'], password= hashPW)
    request.session['loggedinID'] = newuser.id
    return redirect('/newsfeed')

def newaccount(request):
    return render(request, 'register.html')

def logout(request):
    request.session.clear()
    return redirect('/')

def login(request):
    print(request.POST)
    errors = Register.objects.loginValidator(request.POST)
    if len(errors) >0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/')
    user = Register.objects.get(email= request.POST['email'])
    request.session['loggedinID']= user.id
    return redirect('/newsfeed')

def newsfeed(request):
    if 'loggedinID' not in request.session:
        return redirect('/')
    context= {
        'loggedinUser': Register.objects.get(id= request.session['loggedinID']),
        'allmessages': Message.objects.all().order_by("-created_at"),
        'allcomments': Comment.objects.all()
    }
#     ClassName.objects.all().order_by("field_name") - orders by field provided, ascending
# ClassName.objects.all().order_by("-field_name")
    return render(request,'success.html', context)

def postmessage(request):
    newmessage = Message.objects.create(message= request.POST['postmessage'], message_uploader = Register.objects.get(id=request.session['loggedinID']))
    return redirect('/newsfeed')

def postcomment(request, messageid):
    newcomment = Comment.objects.create(comment= request.POST['postcomment'], comment_uploader = Register.objects.get(id=request.session['loggedinID']), message_comment=Message.objects.get(id=messageid))
    # print(Comment.objects.all())
    # print(messageid)
    return redirect('/newsfeed')