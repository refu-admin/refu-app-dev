from django.db import models

# Create your models here.
class User(models.Model):
    
    GENDER_CHOICES = (
        (1, '男性'),
        (2, '女性'),
        (3, 'その他'),
    )
    
    Name = models.CharField(max_length=100)
    age = models.IntegerField()
    contactdate = models.DateField()
    gender = models.IntegerField(verbose_name='性別', choices=GENDER_CHOICES, blank=True, null=True)

class OAuthTokenTemp(models.Model):
    id = models.BigIntegerField(primary_key=True)
    oauth_token = models.CharField(max_length=255, db_index=True, unique=True)
    oauth_token_secret = models.CharField(max_length=255, db_index=True, unique=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["oauth_token", "oauth_token_secret"],
                name="oauth_unique"
            ),
        ]