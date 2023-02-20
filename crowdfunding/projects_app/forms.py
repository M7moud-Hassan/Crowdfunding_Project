from datetime import datetime

from django import forms
from .models import *
from django.forms.widgets import NumberInput


class ProjectForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Type tile",
                "class": "form-control"
            }
        ))

    details = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Type details",
                "class": "form-control",
                'rows': '2'
            }
        ))

    total_target = forms.FloatField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Type Total Target",
                "class": "form-control",
                           }
        ))

    start_time = forms.DateTimeField(
        widget=NumberInput(
            attrs={
                'placeholder': 'Start date',
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))

    end_time = forms.DateTimeField(
        widget=NumberInput(
            attrs={
                'placeholder': 'End date',
                'type': 'datetime-local',
                'class': 'form-control'
            }
        ))

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      widget=forms.Select(
                                          attrs={
                                              "class": "form-control"
                                          }
                                      ))

    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                         widget=forms.CheckboxSelectMultiple())

    def clean(self):
        data = super().clean()
        start_date = data.get("start_time")
        end_date = data.get("end_time")
        today_date = datetime.strptime(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        if today_date.date() > end_date.date():
            self._errors["end_time"] = self.error_class(["End date should be greater than Current date"])
        else:
            if end_date <= start_date:
                self._errors["end_time"] = self.error_class(["End date should be greater than start date."])
        total_target=data.get("total_target")
        if total_target<100:
            self._errors["total_target"] = self.error_class(["total target should great than 100 "])

    class Meta:
        model = Project
        fields = ('title',
                  'details',
                  'total_target',
                  'start_time',
                  'end_time',
                  'category',
                  'tag')


class ReplyForm(forms.ModelForm):

    class Meta:
        model=Reply
        fields =['reply']