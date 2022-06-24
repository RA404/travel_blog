from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import forms

from posts.models import Post, Country


User = get_user_model()


class TestViews(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestClsUser')
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
        cls.form_fields = {
            'text': forms.fields.CharField,
            'country': forms.fields.ChoiceField,
        }

    def setUp(self):
        self.auth_client = Client()
        self.auth_client.force_login(TestViews.user)

    def test_context_main_page(self):
        res = self.auth_client.get(reverse('travel_posts:main'))
        res_context = res.context.get('page_posts')[0]
        self.assertEquals(TestViews.post, res_context)

    def test_context_country_list(self):
        res = self.auth_client.get(
            reverse(
                'travel_posts:country_posts',
                kwargs={'slug': TestViews.country.slug}
            ),
        )
        res_context_country = res.context.get('country')
        res_context_post = res.context.get('page_posts')[0]
        self.assertEquals(TestViews.post.country, res_context_country)
        self.assertEquals(TestViews.post, res_context_post)

    def test_context_profile(self):
        res = self.auth_client.get(
            reverse(
                'travel_posts:profile',
                kwargs={'user_name': TestViews.user.username}
            )
        )
        res_context = res.context.get('page_posts')[0]
        self.assertEquals(TestViews.post, res_context)

    def test_context_post_detail(self):
        res = self.auth_client.get(
            reverse(
                'travel_posts:post_detail',
                kwargs={'post_id': TestViews.post.pk}
            )
        )
        res_context = res.context.get('post')
        self.assertEquals(TestViews.post, res_context)

    def test_context_edit_post(self):
        res = self.auth_client.get(
            reverse(
                'travel_posts:post_edit',
                kwargs={
                    'post_id': TestViews.post.pk,
                }
            )
        )
        form_fields = TestViews.form_fields
        for field, expected_field in form_fields.items():
            with self.subTest(field=field):
                form_field = res.context.get('form').fields.get(field)
                self.assertIsInstance(form_field, expected_field)

    def test_context_create_post(self):
        res = self.auth_client.get(
            reverse('travel_posts:post_create')
        )
        form_fields = TestViews.form_fields
        for field, expected_field in form_fields.items():
            with self.subTest(field=field):
                form_field = res.context.get('form').fields.get(field)
                self.assertIsInstance(form_field, expected_field)
