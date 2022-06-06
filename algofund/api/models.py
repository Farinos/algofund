from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Pool(models.Model):
    '''Class representing pool to collect funds'''
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    # smart contract id
    applicationIndex = models.CharField(max_length=200)
    # pip install Pillow to use ImageField
    image = models.ImageField(upload_to='pictures')

    def __str__(self) -> str:
        return f'Name: {self.name} AppIndex: {self.applicationIndex}'