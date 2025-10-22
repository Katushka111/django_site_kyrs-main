from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['product_id', 'rating', 'text', 'author_name', 'author_email']
        widgets = {
            'product_id': forms.HiddenInput(),
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Поделитесь своим мнением о товаре...',
                'class': 'form-control'
            }),
            'author_name': forms.TextInput(attrs={
                'placeholder': 'Ваше имя',
                'class': 'form-control'
            }),
            'author_email': forms.EmailInput(attrs={
                'placeholder': 'your@email.com',
                'class': 'form-control'
            }),
            'rating': forms.RadioSelect(attrs={
                'class': 'rating-input'
            })
        }
        labels = {
            'rating': 'Оценка',
            'text': 'Отзыв',
            'author_name': 'Ваше имя',
            'author_email': 'Email'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поле product_id скрытым
        self.fields['product_id'].widget = forms.HiddenInput()
        # Устанавливаем значение по умолчанию для product_id
        if 'product_id' in self.initial:
            self.fields['product_id'].initial = self.initial['product_id']
        
        # Делаем product_id необязательным, но с значением по умолчанию
        self.fields['product_id'].required = False
    
    def clean_product_id(self):
        product_id = self.cleaned_data.get('product_id')
        # Если product_id не указан, используем 0 (общий отзыв)
        if not product_id:
            return 0
        return product_id
