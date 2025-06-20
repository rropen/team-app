from django.db.models.signals import post_save
from django.dispatch import receiver
from teams_app.models import User, UserToken
import hashlib

@receiver(post_save, sender=User)
def create_user_token(sender, instance, **kwargs):
    try:
        UserToken.objects.get(pk=instance.id)
    except Exception as exception: # Token does not exist so new token should be created
        
        username = str(instance.username).encode() # Get the raw username string from request
        username_hash = hashlib.sha256(username).hexdigest() # Encrypt and get digest value

        user_token = UserToken(
            user_id=instance.id,
            username_hash=username_hash
        )
        user_token.save()

    # Token already exists so do nothing
