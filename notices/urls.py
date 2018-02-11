
from django.urls import path
from . import views

app_name = 'notices'

urlpatterns = [
		path('', views.home, name='home'),
		path('notices/<int:notice_id>', views.notice_page, name='notice_page'),
		path('notice/new', views.new_notice, name='new_notice')
		]