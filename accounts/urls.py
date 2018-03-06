
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
		path('signup/', views.signup, name='signup'),
		path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True), name='login'),
		path('logout/', auth_views.LogoutView.as_view(), name='logout'),		
		path('reset/', auth_views.PasswordResetView.as_view(
	        template_name='accounts/password_reset.html',
	        email_template_name='accounts/password_reset_email.html',
	        subject_template_name='accounts/password_reset_subject.txt', 
	        success_url='done/'
   		 ), name='password_reset'),
		path('reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
   			 name='password_reset_done'),
		path('reset/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
   			 name='password_reset_confirm'),
		path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
    		name='password_reset_complete'),
		path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html', success_url='done/'),
    		name='password_change'),
		path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
    		name='password_change_done'),
		path('settings/account', views.UserUpdateView.as_view(), name='my_account')
		]