from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import Notice

def home(request) :
    notices = Notice.objects.all()
    return render(request, 'notices/home.html', {'notices': notices})

def notice_page(request, notice_id) :
	notice = get_object_or_404(Notice, id = notice_id)
	return render(request, 'notices/notice_page.html', {'notice': notice})