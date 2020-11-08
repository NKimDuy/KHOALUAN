from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import Comment, Order

class RegistrationForm(forms.Form):
    username = forms.CharField(label='tài khoản: ', max_length=30)
    email = forms.EmailField(label="địa chỉ email: ")
    password1 = forms.CharField(label="mật khẩu", widget=forms.PasswordInput())
    password2 = forms.CharField(label="nhập lại mật khẩu", widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2 and password1:
                return password2
        raise forms.ValidationError('mật khẩu không hợp lệ')
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('tên tài khoản chứa kí tự đặc biệt')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('tên tài khoản đã tồn tại')
    def save(self):
        User.objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], password=self.cleaned_data['password1'])


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.product = kwargs.pop('product', None)
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        comment = super().save(commit=False)
        comment.author = self.author
        comment.product = self.product
        comment.save()
    class Meta:
        model = Comment
        fields = ['content']


class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author', None)
        self.product = kwargs.pop('product', None)
        self.quantity = kwargs.pop('quantity', None)
        self.price = kwargs.pop('price', None)
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        order = super().save(commit=False)
        order.author = self.author
        order.product = self.product
        order.quantity = self.quantity
        order.price = self.price
        order.save()
    class Meta:
        model = Order
        fields = ['phone', 'mail', 'address']