from django.db import models
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class RegisterManager(models.Manager):
    def registrationValidator(self, postData):
        errors = {}
        if len(postData['fname']) < 2:
            errors['errorfname'] = "First name must be at least 2 characters."
        if len(postData['lname']) < 2:
            errors['errorlname'] = "Last name must be at least 2 characters."
        if len(postData['email']) < 1:
            errors['erroremail'] = "Please enter an email."
        elif not EMAIL_REGEX.match(postData['email']):
            errors['emailformat'] = "Please enter a valid email."
        else:
            userswithemail = Register.objects.filter(email= postData['email'])
            if len(userswithemail) > 0:
                errors['emailexists'] = "Email already exists, please choose a different email."  
        if len(postData['pw']) < 8:
            errors['errorpw'] = "Password must be at least 8 characters."
        if postData['pw'] != postData['confirmpw']:
            errors['errorpw'] = "Password does not match."
        return errors

    def loginValidator(self, formInfo):
        errors ={}
        if len(formInfo['email']) < 1:
            errors['erroremail'] = "Please enter an email."
        
        emailExist = Register.objects.filter(email= formInfo['email'])
        if len(emailExist) == 0:
            errors['noEmail']="This email does not exist. Please register."
        else:
            user = emailExist[0]
            if not bcrypt.checkpw(formInfo['pw'].encode(), user.password.encode()):
                errors ['pw'] = "Password incorrect, please try again."
        return errors 

class Register(models.Model):
    first_name= models.CharField(max_length=255)
    last_name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegisterManager()
    def __repr__(self):
        return f"<Register object: {self.first_name} {self.last_name} ({self.id})>"

class Message(models.Model):
    message=models.TextField()
    message_uploader = models.ForeignKey(Register, related_name= "uploaded_messages", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    comment=models.TextField()
    comment_uploader= models.ForeignKey(Register, related_name= "uploaded_comments", on_delete=models.CASCADE)
    message_comment=models.ForeignKey(Message, related_name="messages_comments", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


