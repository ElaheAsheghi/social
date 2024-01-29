from django import forms
from .models import * 
from django.contrib.auth.forms import AuthenticationForm


#LoginForm
class LoginForm(AuthenticationForm):

    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(
        attrs = {
            'placeholder':'username or phone'
        }
    ))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(
        attrs = {
            'placeholder': 'password'
        }
    ))


#RegisterForm
class UserRegisterForm(forms.ModelForm):

    password = forms.CharField(max_length=20, widget=forms.PasswordInput,label="password")
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput, label="repeat password")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("پسوردها مطابقت ندارند")
        return cd['password2']
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.filter(phone = phone).exists():
            raise forms.ValidationError("با این شماره اکانت دیگری وجود دارد")
        return phone
    
    def clean_user(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("اکانت دیگری با این نام کاربری وجود دارد")
        return username
    
    
#UserEditForm
class UserEditForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['photo' ,'first_name', 'last_name', 'date_of_birth', 'bio', 'phone', 'email', 'job']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if User.objects.exclude(id = self.instance.id).filter(phone = phone).exists():
            raise forms.ValidationError("اکانت دیگری با این شماره وجود دارد")
        return phone
    
    def clean_user(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(id = self.instace.id).filter(username = username).exists():
            raise forms.ValidationError("اکانت دیگری با این نام کاربری وجود دارد")
        return username
    

#TicketForm
class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش')
    )
    message = forms.CharField(widget=forms.Textarea, required=True)
    name = forms.CharField(max_length=250, required=True, 
                           widget=forms.TextInput(attrs={'placeholder':'نام',
                                                         'class':'name',}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'ایمیل',
                                                            'class':'email'}))
    phone = forms.CharField(max_length=11, required=True, 
                            widget=forms.NumberInput({'placeholder':'شماره تماس',
                                                        'class':'phone'}))
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES)

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric():
                raise forms.ValidationError("مقدار وارد شده عددی نیست")
            else:
                return phone
            

#PostForm
class CreatePostForm(forms.ModelForm):
   
    class Meta:
        model = Post
        fields = ['description', 'image', 'tags']

    def clean_description(self):
        description = self.cleaned_data['description']
        if description:
            if 100 <= len(description) or len(description)<= 2:
                raise forms.ValidationError("تعداد کاراکتر وارد شده برای متن پست مجاز نیست")
            else:
                return description
            

#SearchForm
class SearchForm(forms.Form):

    query = forms.CharField()


#CommentForm
class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']


#LoginForm
class LoginForm(AuthenticationForm):
   
    username = forms.CharField(label='نام کاربری',required=True, widget=forms.TextInput(
        attrs = {
            'placeholder':'username'
        }
    ))
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(
        attrs = {
            'placeholder': 'password'
        }
    ))


#LogoutForm
class LogoutForm(AuthenticationForm):
    pass