from django import forms

class SubmissonForm(forms.Form):
    solution = forms.CharField(label="Solution", max_length=255)
