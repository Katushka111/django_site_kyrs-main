from django import forms 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model, authenticate
from django.utils.html import strip_tags
from django.core.validators import RegexValidator
from .models import  CustomUser, ProgressCategory, UserProgress, ProgressUpdate
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm



User = get_user_model()
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, max_length=66,
                              widget=forms.EmailInput(attrs={'class': 'input-register form-control','placeholder': 'Ваша почта'}))
    first_name = forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class': 'input-register form-control','placeholder': 'Имя'}))
    last_name = forms.CharField(required=True,max_length=50,widget=forms.TextInput(attrs={'class': 'input-register form-control','placeholder': 'Фамилия'}))
    password1 = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'Пароль'
        })
    )
    password2 = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'Подтвердите ваш пароль'
        })
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name','email','password1', 'password2','is_trener')
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    def save(self,comit=True):
        user = super().save(commit=False)
        user.username = None
        user.is_trener = self.cleaned_data['is_trener']
        if comit:
            user.save()
        return user


class CustomUserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Email',widget=forms.TextInput(attrs={'autofocus':True,'class':'input-register form-control','placeholder':'Ваша почта'}))
    password = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'autofocus':True,'class':'input-register form-control','placeholder':'Пароль'}))
    

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if email and password:
            self.user_cache = authenticate(self.request, username = email, password=password)
            if(self.user_cache is None):
                raise forms.ValidationError('Invalid email or password')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('this accaunt is inactive.')
        return self.cleaned_data


class CustomUserUpdatedForm(forms.ModelForm):
    phone = forms.CharField(required=False,
                            validators=[RegexValidator(r'^\+?1?\d{9,15}$',"Enter a valid phone number.")],
                            widget=forms.TextInput(attrs={'class': 'input-register form-control','placeholder': 'Ваша почта'}))
    first_name = forms.CharField(required=True,
                                 max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'input-register form-control','placeholder': 'имя'}))
    last_name = forms.CharField(required=True,
                                 max_length=50,
                                 widget=forms.TextInput(attrs={'class': 'input-register form-control','placeholder': 'Фамилия'}))
    email = forms.EmailField(required=False,
                                 widget=forms.EmailInput(attrs={'class': 'input-register form-control','placeholder': 'Ваша почта'}))
    class Meta:
        model = User
        fields = ('first_name','last_name','email','phone')
        widgets = {
            'email':forms.EmailInput(attrs={'class': 'input-register form-control','placeholder': 'Ваша почта'}),
            'first_name':forms.TextInput(attrs={'class': 'input-register form-control','placeholder': 'имя'}),
            'last_name':forms.TextInput(attrs={'class': 'input-register form-control','placeholder': 'Фамилия'}),
            'phone':forms.TextInput(attrs={'class': 'input-register form-control','placeholder': 'Телефонный номер'}),
            }
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise forms.ValidationError('This email is already in use.')
        return email
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('email'):
            cleaned_data['email'] = self.instance.email
            for field in['phone']:
                if cleaned_data.get(field):
                    cleaned_data[field] = strip_tags(cleaned_data[field])
            return cleaned_data 



class UserProgressForm(forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ['category', 'title', 'description', 'target_value', 'unit', 'priority', 'end_date']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите категорию'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название цели (например: "Пробежать 5 км")'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Описание цели (необязательно)'
            }),
            'target_value': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'placeholder': 'Целевое значение'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Единица измерения (км, раз, кг, и т.д.)'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'end_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'category': 'Категория',
            'title': 'Название цели',
            'description': 'Описание',
            'target_value': 'Целевое значение',
            'unit': 'Единица измерения',
            'priority': 'Приоритет',
            'end_date': 'Дата завершения',
        }


class ProgressUpdateForm(forms.ModelForm):
    value_added = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.1',
            'min': '0.1',
            'placeholder': '0.0'
        }),
        label='Добавить значение'
    )
    
    class Meta:
        model = ProgressUpdate
        fields = ['value_added', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Заметки о прогрессе...'
            }),
        }
        labels = {
            'notes': 'Заметки',
        }



class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'Ваш email'
        })
    )

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'Новый пароль'
        }),
        strip=False
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input-register form-control',
            'placeholder': 'Подтвердите новый пароль'
        }),
        strip=False
    )
