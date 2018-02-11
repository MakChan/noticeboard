from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Notice, User
from .forms import NewNoticeForm

def home(request) :
	notices = Notice.objects.all()
	return render(request, 'notices/home.html', {'notices': notices})

def notice_page(request, notice_id) :
	notice = get_object_or_404(Notice, id = notice_id)
	return render(request, 'notices/notice_page.html', {'notice': notice})

def new_notice(request) :

    user = User.objects.first()  # TODO: get the currently logged in user
    if request.method == 'POST':
        form = NewNoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = user
            notice.save()
            return redirect('notices:notice_page', notice_id=notice.pk)  # TODO: redirect to the created topic page
    else:
        form = NewNoticeForm()
    return render(request, 'notices/new_notice.html', {'form': form})



