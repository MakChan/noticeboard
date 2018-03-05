from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Notice, User
from .forms import NewNoticeForm
from django.views.generic import ListView, UpdateView


class NoticeListView(ListView):
	model = Notice
	context_object_name = 'notices'
	template_name = 'notices/home.html'
	paginate_by = 10


	def get_context_data(self, **kwargs):
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		queryset = Notice.objects.order_by('-created_at')
		return queryset

def TagView(request, tag):

	notices = Notice.objects.filter(tags__icontains=tag+',').order_by('-created_at').values()
	if len(notices) == 0:
		return render(request, 'notices/no_tag.html', {'tag':tag})

	return render(request, 'notices/tag.html', {'notices': notices, 'tag':tag})

def TagListView(request) :
	queryset = Notice.objects.filter(tags__isnull=False).values_list('tags', flat=True)
	tags = set(''.join(queryset).split(',')[:-1])
	return render(request, 'notices/tags.html', {'tags': tags})


def NoticeView(request, notice_id) :
	notice = get_object_or_404(Notice, id = notice_id)
	return render(request, 'notices/notice_page.html', {'notice': notice})


@login_required
def NewNoticePage(request) :

	if request.method == 'POST':
		form = NewNoticeForm(request.POST)
		if form.is_valid():
			notice = form.save(commit=False)
			notice.created_by = request.user
			notice.save()
			return redirect('notices:notice_page', notice_id=notice.pk) 
	else:
		form = NewNoticeForm()
	return render(request, 'notices/new_notice.html', {'form': form})

