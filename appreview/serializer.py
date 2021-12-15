from rest_framework import serializers
from .models import Profile, Post

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields = ('user','profile_pic','bio','location')
        
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model= Post
        fields = ('screenshot','title','author','live_link','date_posted')