from django.shortcuts import render, redirect
from django.db.models import Q
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
        return redirect('/newaccount')
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

    query=""
    if request.GET:
        query= request.GET['q']
        context['query'] = str(query)

#     ClassName.objects.all().order_by("field_name") - orders by field provided, ascending
#      ClassName.objects.all().order_by("-field_name")


    return render(request,'success.html', context)

def profile(request, profileid):
    if 'loggedinID' not in request.session:
        return redirect('/')
    context= {
        'loggedinUser': Register.objects.get(id= request.session['loggedinID']),
        'profiletoshow': Register.objects.get(id=profileid),
        'myposts' : Message.objects.filter(message_uploader= Register.objects.get(id= profileid)),
        'allcomments': Comment.objects.all()
    }
    return render(request,'profile.html', context)

def postmessage(request):
    newmessage = Message.objects.create(message= request.POST['postmessage'], message_uploader = Register.objects.get(id=request.session['loggedinID']))
    return redirect('/newsfeed')

def postcomment(request, messageid):
    newcomment = Comment.objects.create(comment= request.POST['postcomment'], comment_uploader = Register.objects.get(id=request.session['loggedinID']), message_comment=Message.objects.get(id=messageid))
    # print(Comment.objects.all())
    # print(messageid)
    return redirect('/newsfeed')

def deletepost(request, postid):
    deletepost=Message.objects.get(id=postid)
    deletepost.delete()
    return redirect('/newsfeed')
    

def deletecomment(request, commentid):
    deletecomment=Comment.objects.get(id=commentid)
    deletecomment.delete()
    return redirect('/newsfeed')

def profilemessage(request, profileid):
    newmessage = Message.objects.create(message= request.POST['postmessage'], message_uploader = Register.objects.get(id=request.session['loggedinID']))
    return redirect(f'/profile/{profileid}')

def profilecomment(request, profileid, commentid):
    newcomment = Comment.objects.create(comment= request.POST['postcomment'], comment_uploader = Register.objects.get(id=request.session['loggedinID']), message_comment=Message.objects.get(id=commentid))
    # print(Comment.objects.all())
    # print(messageid)
    return redirect(f'/profile/{profileid}')

def deleteprofilepost(request, profileid, postid):
    deletepost=Message.objects.get(id=postid)
    deletepost.delete()
    return redirect(f'/profile/{profileid}')
    

def deleteprofilecomment(request, profileid, commentid):
    deletecomment=Comment.objects.get(id=commentid)
    deletecomment.delete()
    return redirect(f'/profile/{profileid}')

def get_user_queryset(query=None):
    queryset=[]
    queries= query.split(" ")
    for q in queries:
        users= Register.objects.filter(
            Q(first_name__icontains=q),
            Q(last_name__icontains=q)
        ).distinct()
        
        for user in users:
            queryset.append(user)
    
    return list(set(queryset))

# def detail_user_view(request, slug):

# 	context = {}

# 	User = get_object_or_404(User, slug=slug)
# 	context['user'] = user

# 	return render(request, '/detail_user.html', context)
