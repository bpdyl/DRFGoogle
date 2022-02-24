from django.db import models
from django.utils import timezone
from DRFGoogle import settings
# Create your models here.
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from PIL import Image

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_author')
    published_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-published_date',)

    def __str__(self):
        return self.title

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, username, password, **extra_fields):
        """
        Create and save a User with the given email username and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The username must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,username = username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email,username, password, **extra_fields)

DEFAULT = 'user_photos/nouser.jpg'
class CustomUser(AbstractUser):
    options = (
            ('IT and Networks','IT and Networks'),
            ('UI/UX','UI/UX'),
            ('Web Development','Web Development'),
            ('Devops','Devops'),
        )
    GENDER_CHOICES = (("Male",'Male'),("Female",'Female'),("Other",'Other'))
    email                   = models.EmailField(_('email address'), unique=True)
    username                = models.CharField(max_length=30, unique=True)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    profile_image           = models.ImageField(max_length=255, upload_to='user_photos',blank=True, default=DEFAULT)
    address                 = models.CharField(max_length=100,null=True,blank=True)
    phone_number            = models.IntegerField(null=True,blank=True,max_length=10)
    gender                  = models.CharField(max_length=50,choices=GENDER_CHOICES, null=True)
    interest                = models.CharField(max_length=150,choices = options, null=True)
    profile_completed       = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        super().save(*args,**kwargs)
        SIZE = 300,300
        print("yaa samma chai ma ni ho hai")
        if self.profile_image and hasattr(self.profile_image, 'url'):
            print("its image path",self.profile_image.path)
            try:
                pic = Image.open(self.profile_image.path)
                print(" ma chai herna aako")
                pic.thumbnail(SIZE, Image.LANCZOS)
                pic.save(self.profile_image.path)
            except:
                print("i am here")
                self.profile_image.delete(save=False)  # delete old image file
                self.profile_image = DEFAULT
                self.save()
        else:
            print("testing if profile image exists or not")

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    @property
    def get_photo_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            print(self.profile_image.url)
            return self.profile_image.url
        else:
            print("/media/user_photos/nouser.jpg")
            return "/media/user_photos/nouser.jpg"



"""
curl -X POST -d "client_id=dJPU1GuE50wGzuzCc5vf2Lfd8LEqfM5jYZWX0LFC&client_secret=1fNDbZcYJHuL7BZK54jSFonWiHI8EL0VZ7YMm1jNxZ8os4SNjCWkBH33hHH07L572B59hYIDFi22F3LjPksg0QGtpIVKBkzIVcYSVkw3jY2et8iVLTBQur28IhtGmHTu&grant_type=password&username=bibek@gmail.com&password=bibek@123" http://localhost:8000/auth/token
"""