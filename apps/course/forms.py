# streamers/forms.py
from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
    #     exclude = ['enable', 'join_date', 'is_capacite', 'date_capacite'] 
    #     # widgets = {
    #     #     'join_date': forms.DateTimeInput(
    #     #         attrs={'type': 'datetime-local', 'class': 'form-control'},
    #     #         format='%Y-%m-%dT%H:%M'
    #     #     ),
    #     #     'date_capacite': forms.DateTimeInput(
    #     #         attrs={'type': 'datetime-local', 'class': 'form-control'},
    #     #         format='%Y-%m-%dT%H:%M'
    #     #     ),
    #     # }

    # def __init__(self, *args, **kwargs):
    #     super(StreamerForm, self).__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         if not isinstance(field.widget, forms.CheckboxInput):
    #             field.widget.attrs['class'] = 'form-control'
