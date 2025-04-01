from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from blog.models import Post
from django.utils import timezone

# Create your tests here.
class SignupTests(TestCase):
    def test_signup_get(self):
        response =self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/signup.html')

    def test_signup_post(self):
        response = self.client.post(reverse('signup'), {
            'uname':'testuser',
            'uemail':'testuser@example.com',
            'upassword':'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())


class LoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_login_get(self):
        response =self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/login.html')

    def test_login_post_valid(self):
        response = self.client.post(reverse('login'), {
            'uname':'testuser',
            'upassword':'password123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'uname':'testuser',
            'upassword':'wrongpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')


class SignoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_logout(self):
        self.client.login(username='testuser', password='password123')
        response =self.client.get(reverse('signout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        self.assertFalse('_auth_user_id' in self.client.session)


class HomeTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(title='Test Post', content='Test Content', category='General', author=self.user)

    def test_home(self):
        response =self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')
        self.assertContains(response, 'Test Post')


class NewPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_new_post_get(self):
        self.client.login(username='testuser', password='password123')
        response =self.client.get(reverse('newpost'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/newpost.html')

    def test_new_post(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('newpost'), {
            'title':'New Post',
            'content':'This is a New Post',
            'category':'General'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post').exists())


class MyPostTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        self.user_post = Post.objects.create(title='User Post', content='User Content', category='General', author=self.user)
        self.other_user_post = Post.objects.create(title='Other User Post', content='Other User Content', category='General', author=self.other_user)

    def test_mypost(self):
        self.client.login(username='testuser', password='password123')
        response =self.client.get(reverse('mypost'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/mypost.html')
        self.assertContains(response, 'User Post')
        self.assertNotContains(response, 'Other User Post')


class SearchTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post1 = Post.objects.create(title='Post 1', content='Content 1', category='Tech', author=self.user)
        self.post2 = Post.objects.create(title='Post 2', content='Content 2', category='Health', author=self.user)

    def test_search(self):
        response =self.client.get(reverse('search'), {'search':'Tech'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post 1')
        self.assertNotContains(response, 'Post 2')


class UpdateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(post_id=4, title='New Title', content='New Content', category='Updated', author=self.user)

    def test_update_get(self):
        self.client.login(username='testuser', password='password123')
        response =self.client.post(reverse('update', kwargs={'post_id':self.post.post_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/update.html')

    def test_update_post(self):
        self.client.login(username='testuser', password='password123')
        response =self.client.post(reverse('update', kwargs={'post_id':self.post.post_id}),{
            'title':'New Title',
            'content':'New Content',
            'category':'Updated'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.title, 'New Title')
        self.assertEqual(self.post.content, 'New Content')
        self.assertEqual(self.post.category, 'Updated')


class DeleteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.post = Post.objects.create(post_id=4, title='Test Post', content='Test Content', category='General', author=self.user)

    def test_delete_get(self):
        self.client.login(username='testuser', password='password123')
        response =self.client.get(reverse('delete', kwargs={'post_id':self.post.post_id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/delete.html')

    def test_delete_post(self):
        self.client.login(username='testuser', password='password123')
        response =self.client.post(reverse('delete', kwargs={'post_id':self.post.post_id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(post_id=self.post.post_id).exists())


class PostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_post(self):
        post = Post.objects.create(title='Test Post', content='Test Content', category='General', author=self.user)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'Test Content')
        self.assertEqual(post.category, 'General')
        self.assertIsNotNone(post.date_posted)

    def test_post_str_method(self):
        post = Post.objects.create(title='Test Post', content='Test Content', category='General', author=self.user)
        self.assertEqual(str(post), 'Test Post')

    def test_post_soft_delete(self):
        post = Post.objects.create(title='Test Post', content='Test Content', category='General', author=self.user) 
        self.assertFalse(post.is_deleted)
        post.soft_delete()
        self.assertTrue(post.is_deleted)

    def test_post_restore(self):
        post = Post.objects.create(title='Test Post', content='Test Content', category='General', author=self.user) 
        post.soft_delete()
        self.assertTrue(post.is_deleted) 
        post.restore()
        self.assertFalse(post.is_deleted)


class SoftDeleteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_soft_delete(self):
        post = Post.objects.create(title='Test Post', content='Test Content', category='General', author=self.user) 
        self.assertFalse(post.is_deleted)
        post.soft_delete()
        self.assertTrue(post.is_deleted)

    def test_restore(self):
        post = Post.objects.create(title='Test Post', content='Test Content', category='General', author=self.user) 
        post.soft_delete()
        self.assertTrue(post.is_deleted) 
        post.restore()
        self.assertFalse(post.is_deleted)

    
class NonDeletedModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_non_deleted(self):
        post1 = Post.objects.create(title='Test Post 1', content='Test Content', category='General', author=self.user) 
        post1.soft_delete()
        post2 = Post.objects.create(title='Test Post 2', content='Test Content', category='General', author=self.user) 
        non_deleted_posts = Post.objects.all()
        self.assertEqual(non_deleted_posts.count(), 2)





