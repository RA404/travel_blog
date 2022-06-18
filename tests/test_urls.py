from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from posts.models import Post, Country


User = get_user_model()


class PostURLsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='UserCls')
        cls.country = Country.objects.create(
            title='New Zealand',
            slug='New-Zealand',
            description='NZ description',
        )
        cls.post = Post.objects.create(
            text='Some post about NZ',
            pub_date='2022-06-18 15:35:33.561887',
            author=cls.user,
            country=cls.country,
        )
        cls.post_urls_templates_for_all = {
            reverse('travel_posts:main'): 'posts/index.html',
            reverse(
                'travel_posts:country_posts',
                kwargs={'slug': PostURLsTests.country.slug},
            ): 'posts/country_posts.html',
            reverse(
                'travel_posts:profile',
                kwargs={'user_name': PostURLsTests.user},
            ): 'posts/profile.html',
            reverse(
                'travel_posts:post_detail',
                kwargs={'post_id': PostURLsTests.post.pk},
            ): 'posts/post_detail.html',
            # reverse('travel_posts:post_create'): 'posts/create_post.html',
            # reverse(
            #     'travel_posts:post_edit',
            #     kwargs={'post_id': PostURLsTests.post.pk}
            # ): 'posts/update_post.html',
        }

    def setUp(self):
        self.web_client_guest = Client()

        self.user = User.objects.create_user(username='UserAuth')
        self.web_client_auth = Client()
        self.web_client_auth.force_login(self.user)

    def test_page_status_ok(self):
        """Test pages statuses for all users, including unauthorized"""
        for post_url in PostURLsTests.post_urls_templates_for_all:
            with self.subTest():
                response = self.web_client_guest.get(post_url)
                self.assertEquals(response.status_code, HTTPStatus.OK)

    def test_page_templates(self):
        """Test templates pages for all users, including unauthorized"""
        for (
            post_url,
            template,
        ) in PostURLsTests.post_urls_templates_for_all.items():
            with self.subTest():
                response = self.web_client_guest.get(post_url)
                self.assertTemplateUsed(response, template)
