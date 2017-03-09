from django.db import models

# Create your models here.
class seebug(models.Model):
    SSV_ID=models.CharField(max_length=50, unique=True,primary_key=True)
    Push_time=models.CharField(max_length=20)
    Level=models.CharField(max_length=20)
    Poc_name=models.CharField(max_length=200)
    Detail_link=models.CharField(max_length=100)


