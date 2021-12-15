from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Avg
from statistics import mean
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField


# Creating profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,blank=True)
    profile_pic = CloudinaryField('profile_pic')
    location = models.CharField(max_length=100,blank=True)
    
    def __str__(self):
        return str(self.user)
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
 #post   
class Post(models.Model):
    screenshot = CloudinaryField('image')
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    live_link = models.CharField(max_length=50,blank=True)
    author = models.ForeignKey(User,related_name='posts', on_delete=models.CASCADE)
    date_posted = models.DateField(default=timezone.now)
    
    
    def __str__(self):
        return self.title
    
    def save_post(self):
        self.save()
        
    def delete_post(self):
        self.delete()
    
        
    @classmethod    
    def get_posts(self):
        posts = Post.objects.all()
        return posts
    
    @classmethod    
    def search_post(self, search_title):
        posts= Post.objects.filter(title__icontains=search_title)
        return posts
    
    
class Rating(models.Model):
    post = models.ForeignKey(Post,related_name='ratings',on_delete=models.CASCADE)
    author = models.ForeignKey(User,related_name='rates',on_delete=models.CASCADE)
    design_rating = models.IntegerField(default=0,validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    usability_rating = models.IntegerField(default=0,validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    content_rating = models.IntegerField(default=0,validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    
    
    
    def __str__(self):
        return '{} by {}'.format(self.post, self.author)
   
      
    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['author', 'post'], name="unique_rating"),
    ]

    def save_rating(self):
        self.save()
    
    
    def rating_avg(self):
        rating = Rating.objects.filter(id=self.id)
        rating1= rating(avg1=Avg('design_rating'))
        rating2= rating.aggregate(avg2=Avg('usability_rating'))
        rating3= rating.aggregate(avg3=Avg('content_rating'))
        return rating
    