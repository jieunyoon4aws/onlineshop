from django import forms

class AddProductForm(forms.Form):
    quantity = forms.IntegerField()
    is_update = forms.BooleanField(required=False, initial= False, widget=forms.HiddenInput)
    # widget: 브라우저에서 값은 넘기고 싶지만, form 안 보이게 설정
    # html에서의 hidden type: <input type='hidden' name='key' value='1234'>

