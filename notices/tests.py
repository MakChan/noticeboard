from django.test import TestCase
from django.urls import reverse, resolve
from .views import NoticeView, NewNoticePage, NoticeListView, UserNoticeListView, TagListView, TagView
from .models import Notice, User
from .forms import NewNoticeForm

class HomeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john', email='john@doe.com', password='123')
        self.notice = Notice.objects.create(title='Notice Title', message='Notice Description.', created_by=self.user)
        url = reverse('notices:home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, NoticeListView)

    def test_home_view_contains_link_to_notices_page(self):
        notices_url = reverse('notices:notice_page', kwargs={'notice_id': self.notice.id})
        self.assertContains(self.response, 'href="{0}"'.format(notices_url))

    def test_home_view_contains_new_notice_link(self):
        new_notice_url = reverse('notices:home')
        self.assertContains(self.response, 'href="{0}"'.format(new_notice_url))      


class NoticeTests(TestCase):
    def setUp(self):
        Notice.objects.create(title='Notice Title', message='Notice Description.', created_by_id=1)
        username = 'jane'
        password = '321'
        User.objects.create_user(
            username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)


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
        self.assertEquals(view.func, NoticeView)

    def test_notice_view_contains_link_back_to_home_view(self):
        notice_url = reverse('notices:notice_page', kwargs={'notice_id': 1})
        response = self.client.get(notice_url)
        homepage_url = reverse('notices:home')  
        self.assertContains(response, 'href="{0}"'.format(homepage_url))


class LoginRequiredNewNoticeTests(TestCase):
    def setUp(self):
        self.url = reverse('notices:new_notice')
        self.response = self.client.get(self.url)

    def test_redirection(self):
        login_url = reverse('admin:login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(
            login_url=login_url, url=self.url))


class UnauthorizedNewNoticeTests(TestCase):
    def setUp(self):
        '''
        Create a new user different without staff permissions
        '''
        username = 'jane'
        password = '321'
        User.objects.create_user(
            username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)
        self.url = reverse('notices:new_notice')
        self.response = self.client.get(self.url)

    def test_redirection(self):
        '''
        A notice can be posted by only a staff user.
        Unauthorized users should get redirected to login page.
        '''
        login_url = reverse('admin:login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(
            login_url=login_url, url=self.url))



class NewNoticeTests(TestCase):
    def setUp(self):
        username = 'jane'
        password = '321'
        User.objects.create_superuser(
            username=username, email='jane@doe.com', password=password)
        self.client.login(username=username, password=password)

    def test_new_notice_view_success_status_code(self):
        url = reverse('notices:new_notice')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_new_notice_url_resolves_new_notice_view(self):
        view = resolve('/notice/new')
        self.assertEquals(view.func, NewNoticePage)

    def test_csrf(self):
        url = reverse('notices:new_notice')
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        url = reverse('notices:new_notice')
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewNoticeForm)

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
        self.client.post(url, data)
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


class UserNoticeListTests(TestCase):
    def setUp(self):
        username = 'jane'
        password = '321'
        self.user = User.objects.create_superuser(
            username=username, email='jane@doe.com', password=password)
        self.notice = Notice.objects.create(
            title='Notice Title', message='Notice Description.', created_by=self.user)
        self.client.login(username=username, password=password)
        url = reverse('notices:user_notices', kwargs={'user': self.user})
        self.response = self.client.get(url)

    def test_user_notice_list_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_user_notice_list_url_resolves_user_notice_list_view(self):
        view = resolve('/u/{}'.format(self.user))
        self.assertEquals(view.func.view_class, UserNoticeListView)

    def test_user_notice_list_view_contains__user_notices(self):
        self.assertContains(self.response, '{}'.format(self.notice.title))

    def test_user_notice_list_view_contains__new_notice_link(self):
        self.assertContains(self.response, '{}'.format(self.user.username))


class TagListTests(TestCase):
    def setUp(self):
        username = 'jane'
        password = '321'
        self.user = User.objects.create_superuser(
            username=username, email='jane@doe.com', password=password)
        self.notice = Notice.objects.create(
            title='Notice Title', message='Notice Description.', created_by=self.user, tags='tag1,')
        self.client.login(username=username, password=password)
        url = reverse('notices:tags')
        self.response = self.client.get(url)

    def test_tag_list_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_tag_list_url_resolves_tag_list_view(self):
        view = resolve('/tags')
        self.assertEquals(view.func, TagListView)

    def test_tag_list_view_contains__tags(self):
        self.assertContains(self.response, '{}'.format('tag1'))


class TagNoticesTests(TestCase):
    def setUp(self):
        username = 'jane'
        password = '321'
        self.user = User.objects.create_superuser(
            username=username, email='jane@doe.com', password=password)
        self.notice = Notice.objects.create(
            title='Notice Title', message='Notice Description.', created_by=self.user, tags='tag1,')
        self.client.login(username=username, password=password)
        url = reverse('notices:tag', kwargs={'tag': 'tag1'})
        self.response = self.client.get(url)

    def test_tag_notice_list_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_tag_notice_list_url_resolves_tag_notice_list_view(self):
        view = resolve('/tag/{}'.format('tag1'))
        self.assertEquals(view.func.view_class, TagView)

    def test_tag_notice_list_view_contains__notice(self):
        self.assertContains(self.response, '{}'.format(self.notice.title))

