from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import DateRangeForm
# Create your views here.
from website.queries.query import get_result_to_display, query_for_keitaro


def index(request):
    return render(request, 'index.html')


# view for dislaing form for choosing two dates, first must be before second or equal. after choosing dates must update
# table below on the same page with data from query to keitaro
@login_required
def date_range(request):
    template = 'website/date_range.html'
    buyer_sub_id = request.user.profile.buyer_sub_id
    # today date in format YYYY-MM-DD in string
    today = datetime.now().strftime('%Y-%m-%d')
    query_result = get_result_to_display(query_for_keitaro(today, today, buyer_sub_id))
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            # convert dates to string for passing to query
            start_date = start_date.strftime('%Y-%m-%d')
            end_date = end_date.strftime('%Y-%m-%d')
            # get data from query
            query_result = get_result_to_display(query_for_keitaro(start_date, end_date, buyer_sub_id))
            return render(request, template, {'form': form,'start_date': start_date, 'end_date': end_date, 'query_result': query_result})
    else:
        form = DateRangeForm()
    return render(request, template, {'form': form, 'query_result': query_result})