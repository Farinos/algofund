from datetime import datetime, timedelta
from django.db import models
import time

# Create your models here.
class Pool(models.Model):
    '''Class representing pool to collect funds'''
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    # smart contract id
    applicationIndex = models.CharField(max_length=200, unique=True, blank=True) # this field will be populated once the contract is deployed
    minAmount = models.IntegerField(default=100)
    expiryTime = models.DateField(default=datetime.today() + timedelta(days=1))
    # pip install Pillow to use ImageField
    image = models.ImageField(upload_to='pictures', blank=True)

    def __str__(self) -> str:
        return f'Name: {self.name} AppIndex: {self.applicationIndex}'

class Fund(models.Model):
    '''Class representing funding for a pool'''
    senderMnemonic = models.CharField(max_length=200)
    amount = models.IntegerField(default=100)

class FundWithdraw(models.Model):
    '''Class containing mnemonic of the user who want to withdraw funds from a pool'''
    requesterMnemonic = models.CharField(max_length=200)