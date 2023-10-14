from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from .models import User, UserProfile



    
@receiver(post_save, sender= User)
def post_save_prifile_receiver(sender, instance, created, **kwargs):
        print(created)
        if created:
            UserProfile.objects.get_or_create(user=instance)
            print("user profile is created")
        else:
            try:
                profile = UserProfile.objects.get( user= instance)
                profile.save()
            except:
                UserProfile.objects.create(user=instance)
                print("the user was not exixt. i create new one.")
                print("user is updated!")
                
@receiver(pre_save , sender= User)
def pre_save_profile_user(sender, instance, **kwargs):
    print(instance.username, "this user is being save!")