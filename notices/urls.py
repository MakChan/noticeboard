
from django.urls import path
from . import views

app_name = 'notices'

urlpatterns = [
		path('', views.NoticeListView.as_view(), name='home'),
		path('notices/<int:notice_id>', views.NoticeView, name='notice_page'),
		path('notice/new', views.NewNoticePage, name='new_notice'),
		path('tag/<tag>', views.TagView.as_view(), name='tag'),
		path('tags', views.TagListView, name='tags'),
		path('u/<user>', views.UserNoticeListView.as_view(), name='user_notices'),
		]