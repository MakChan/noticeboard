from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, notice_page, new_notice
from .models import Notice, User
from .forms import NewNoticeForm

class HomeTests(TestCase):
    def setUp(self):
        self.notice = Notice.objects.create(title='Notice Title', message='Notice Description.', created_by_id=1)
        url = reverse('notices:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    def test_home_view_contains_link_to_notices_page(self):
        notices_url = reverse('notices:notice_page', kwargs={'notice_id': self.notice.id})
        self.assertContains(self.response, 'href="{0}"'.format(notices_url))

    def test_home_view_contains_new_notice_link(self):
        new_notice_url = reverse('notices:new_notice')
        self.assertContains(self.response, 'href="{0}"'.format(new_notice_url))      


class NoticeTests(TestCase):
    def setUp(self):
        Notice.objects.create(title='Notice Title', message='Notice Description.', created_by_id=1)

    def test_notice_view_success_status_code(self):
        url = reverse('notices:notice_page', kwargs={'notice_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_notice_view_not_found_status_code(self):
        url = reverse('notices:notice_page', kwargs={'notice_id': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_notice_url_resolves_notice_view(self):
        view = resolve('/notices/1')
        self.assertEquals(view.func, notice_page)      

    def test_notice_view_contains_link_back_to_home_view(self):
        notice_url = reverse('notices:notice_page', kwargs={'notice_id': 1})
        response = self.client.get(notice_url)
        homepage_url = reverse('notices:home')  
        self.assertContains(response, 'href="{0}"'.format(homepage_url))

class NewNoticeTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='john', email='john@doe.com', password='123')

    def test_new_notice_view_success_status_code(self):
        url = reverse('notices:new_notice')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_notice_url_resolves_new_notice_view(self):
        view = resolve('/notice/new')
        self.assertEquals(view.func, new_notice)

    def test_new_notice_view_contains_link_back_to_home_view(self):
        new_notice_url = reverse('notices:new_notice')
        home_url = reverse('notices:home')
        response = self.client.get(new_notice_url)
        self.assertContains(response, 'href="{0}"'.format(home_url))        

    def test_csrf(self):
        url = reverse('notices:new_notice')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_notice_valid_post_data(self):
        '''
        While the post data is valid,
        The expected behavior is to add the data into the database.
        '''        
        url = reverse('notices:new_notice')
        data = {
            'title': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        response = self.client.post(url, data)
        self.assertTrue(Notice.objects.exists())

    def test_new_notice_invalid_post_data(self):  
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('notices:new_notice')
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_contains_form(self): 
        url = reverse('notices:new_notice')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewNoticeForm)        

    def test_new_notice_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('notices:new_notice')
        data = {
            'title': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Notice.objects.exists())