from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from posts.models import Post, Country


User = get_user_model()


class TestPostsForms(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='UserCls')
        cls.country = Country.objects.create(
            title='Country Name',
            slug='country-name',
            description='Country description',
        )
        cls.country_changed = Country.objects.create(
            title='Another country Name',
            slug='another-country-name',
            description='Another country description',
        )
        cls.form_create_data = {
            'text': 'Some post text',
            'country': TestPostsForms.country.pk,
            'author': TestPostsForms.user,
        }
        cls.form_edit_data = {
            'text': 'Edited post text',
            'country': TestPostsForms.country_changed.pk,
            'author': TestPostsForms.user,
        }

    def setUp(self):
        self.guest_client = Client()

        self.auth_client = Client()
        self.auth_client.force_login(TestPostsForms.user)

        self.not_author = User.objects.create_user(username='TestNotAuthor')
        self.not_author_client = Client()
        self.not_author_client.force_login(self.not_author)

    def test_auth_user_create_post(self):
        posts_count = Post.objects.count()
        form_data = TestPostsForms.form_create_data

        res = self.auth_client.post(
            reverse('travel_posts:post_create'),
            data=form_data,
            follow=True,
        )

        created_post = Post.objects.last()

        self.assertRedirects(
            res,
            reverse(
                'travel_posts:profile',
                kwargs={'user_name': TestPostsForms.user}
            )
        )
        self.assertEquals(Post.objects.count(), posts_count + 1)
        self.assertEquals(created_post.text, form_data['text'])
        self.assertEquals(created_post.country, TestPostsForms.country)
        self.assertEquals(created_post.author, TestPostsForms.user)

    def test_guest_user_cant_create_post(self):
        post_count_before = Post.objects.count()

        create_url = reverse('travel_posts:post_create')
        expected_url = f'{reverse("users:login")}?next={create_url}'

        res = self.guest_client.post(
            create_url,
            data=TestPostsForms.form_create_data,
            follow=True,
        )
        post_count_after = Post.objects.count()

        self.assertEquals(post_count_before, post_count_after)
        self.assertRedirects(res, expected_url)

    def test_author_can_edit_post(self):
        post = Post.objects.create(
            text='Not edited post',
            pub_date='2022-06-18 15:35:33.561887',
            author=TestPostsForms.user,
            country=TestPostsForms.country,
        )

        form_edited_data = TestPostsForms.form_edit_data
        res = self.auth_client.post(
            reverse(
                'travel_posts:post_edit',
                kwargs={'post_id': post.pk}
            ),
            data=form_edited_data,
            follow=True,
        )

        edited_post = Post.objects.filter(pk=post.pk)[0]

        self.assertEquals(edited_post.text, form_edited_data['text'])
        self.assertEquals(edited_post.country.pk, form_edited_data['country'])

    def test_guest_or_not_author_cant_edit_post(self):
        post = Post.objects.create(
            text='Not edited post',
            pub_date='2022-06-18 15:35:33.561887',
            author=TestPostsForms.user,
            country=TestPostsForms.country,
        )

        edit_url = reverse(
            'travel_posts:post_edit',
            kwargs={'post_id': post.pk},
        )
        expected_login_url = f'{reverse("users:login")}?next={edit_url}'

        form_edited_data = TestPostsForms.form_edit_data
        res = self.guest_client.post(
            edit_url,
            data=form_edited_data,
            follow=True,
        )

        edited_post = Post.objects.filter(pk=post.pk)[0]

        self.assertEquals(edited_post.text, post.text)
        self.assertEquals(edited_post.country.pk, post.country.pk)
        self.assertRedirects(res, expected_login_url)

        res = self.not_author_client.post(
            edit_url,
            data=form_edited_data,
            follow=True,
        )

        edited_post = Post.objects.filter(pk=post.pk)[0]

        self.assertEquals(edited_post.text, post.text)
        self.assertEquals(edited_post.country.pk, post.country.pk)
        self.assertRedirects(res, reverse("travel_posts:main"))
