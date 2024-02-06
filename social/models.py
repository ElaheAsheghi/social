from django.db import models
from django.contrib.auth.models import AbstractUser
from taggit.managers import TaggableManager
from django.urls import reverse

# Create your models here.


#User Model
class User(AbstractUser):
    
    date_of_birth = models.DateField(blank= True, null= True)
    bio = models.TextField(blank= True, null= True)
    photo = models.ImageField(upload_to="account_images/", blank= True, null= True)
    job = models.CharField(max_length= 250, blank= True, null= True)
    phone = models.CharField(max_length= 11, blank= True, null= True)
    following = models.ManyToManyField('self', through='Contact', related_name='followers', symmetrical=False)

    def get_absolute_url(self):
        return reverse('social:user_detail', args=[self.username])


#Post Model
class Post(models.Model):
   
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts", verbose_name="نویسنده")
    description = models.TextField(verbose_name="متن پست")
    image = models.ImageField(upload_to='post_images/%Y/%m/%d', blank=True, null=True)
    tags = TaggableManager()
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    saved_by = models.ManyToManyField(User, related_name='saved_posts')
    #DATE
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])    
        ]

        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def get_absolute_url(self):
        return reverse('social:post_detail', args=[self.id])
        
    def __str__(self):
        return self.description
    
    def delete(self, using=None, keep_parents=False):
        if self.image:
            self.image.delete()
        super().delete()
    

#Comment Model
class Comment(models.Model):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="پست")
    name = models.CharField(max_length=250, verbose_name="نام")
    body = models.TextField(verbose_name="کامنت")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [models.Index(fields=['created'])]
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت ها"

    def __str__(self):
        return f"{self.name} : {self.post}"
    

#M2M Table For Follow
class Contact(models.Model):
   
    user_from = models.ForeignKey(User, related_name='rel_from_set', on_delete=models.CASCADE) #the user who follows someone
    user_to = models.ForeignKey(User, related_name='rel_to_set', on_delete=models.CASCADE) #the user who followed by someone
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def __str__(self):
        return f"{self.user_from} follows {self.user_to}"