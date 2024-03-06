from django.shortcuts import render

# Create your views here.

""" Terms and Conditions' view 
"""


def terms_and_conditions(request):
    return render(request, 'blog/terms_and_conditions_page.html')
