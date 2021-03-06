# Generated by Django 4.0.1 on 2022-02-20 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthTokenTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oauth_token', models.CharField(db_index=True, max_length=255, unique=True)),
                ('oauth_token_secret', models.CharField(db_index=True, max_length=255, unique=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='oauthtokentemp',
            constraint=models.UniqueConstraint(fields=('oauth_token', 'oauth_token_secret'), name='oauth_unique'),
        ),
    ]
