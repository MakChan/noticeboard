from django.test import TestCase
from django.urls import reverse, resolve
from .views import home, notice_page
from .models import Notice

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

    def test_notice_view_contains_link_back_to_homepage(self):
        notice_url = reverse('notices:notice_page', kwargs={'notice_id': 1})
        response = self.client.get(notice_url)
        homepage_url = reverse('notices:home')  
        self.assertContains(response, 'href="{0}"'.format(homepage_url))