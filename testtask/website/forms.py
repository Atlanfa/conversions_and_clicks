from django import forms
from django.forms import ModelForm

from website.models import DateRange


class DateInput(forms.DateInput):
    input_type = 'date'


# form for choosing two dates, first must be before second or equal
class DateRangeForm(ModelForm):

    class Meta:
        model = DateRange
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError('Start date must be before end date')
        return cleaned_data