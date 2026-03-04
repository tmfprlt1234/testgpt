from django import forms

from .models import Record


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['title', 'category', 'amount', 'note']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '카테고리'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'placeholder': '금액'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '비고'}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount < 0:
            raise forms.ValidationError('금액은 0 이상이어야 합니다.')
        return amount
