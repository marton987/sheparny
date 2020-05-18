""" Events Models """
from django.db import models

from accounts.models import Account


class Event(models.Model):
    """ Events model """
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE)
    participants = models.ManyToManyField(Account, related_name='attends')

    def has_participant(self, account):
        """
        Helper function to validate if the provided account will attend the
        event
        :param account: Account instance
        :return: Boolean value describing if the user will attend the meeting
        """
        return self.participants.filter(pk=account.pk).exists()
