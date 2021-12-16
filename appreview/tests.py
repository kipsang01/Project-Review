from django.test import TestCase
from .models import  Post,Rating, Profile
from django.contrib.auth.models import User

# Create your tests here.
class PostTestClass(TestCase):
    
    # Set up method
    def setUp(self):
        self.user1 = User(username='psang',first_name='Enock',last_name ='kipsang',email='psang254@gmail.com',password ='sjsiuwueufbccn')
        self.post1 = Post(screenshot='scrn.jpg',title='wed',description='talk web app',author=self.user1,live_link = 'www.weblink.com')
        self.rating1= Rating(author =self.user1,post=self.post1,design_rating =8, usability_rating = 8,content_rating=8)
        
    # Testing  instance
    def test_instance(self):
        self.assertTrue(isinstance(self.user1,User))
        self.assertTrue(isinstance(self.post1,Post))
        self.assertTrue(isinstance(self.rating1,Rating))
        
        
    # Testing Save Method
    def test_save_method(self):
        self.user1.save()
        self.post1.save_post()
        self.rating1.save_rating()
        users = User.objects.all()
        posts = Post.objects.all()
        ratings = Rating.objects.all()
        self.assertTrue(len(posts) > 0)
        self.assertTrue(len(users) > 0)
        self.assertTrue(len(ratings) > 0)
     
      # Testing Delete Method   
    def test_delete(self):
        self.user1.save()
        self.post1.save_post()
        post = Post.get_object_or_404(Post,id =1)
        post.delete()
        posts = Post.objects.all()
        self.assertTrue(len(posts)==0)
        
        
      # Test get all images 
    def test_get_all_images(self):
        self.post2 = Post(screenshot='scrn2.jpg',title='talkie',description='talkweb application',author=self.user1,live_link = 'www.weblink2.com')
         
        self.user1.save()
        self.post1.save_post()
        self.post2.save_post()
        posts = Post.get_posts()
        self.assertTrue(len(posts) == 2)