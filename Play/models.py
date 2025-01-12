from django.db import models

from Order.models import OrderItem
from Product.models import Suspect
from User.models import User


class CasePlay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # orderItem = models.ForeignKey(OrderItem, on_delete=models.CASCADE, blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('in_progress', 'In Progress'), ('completed', 'Completed'),
                                                      ('cancelled', 'Cancelled')],
                              default='in_progress')


class CaeParticipant(models.Model):
    gameplay = models.ForeignKey(CasePlay, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Participant {self.participant.number} in GamePlay {self.gameplay.id}"


class GameResult(models.Model):
    gameplay = models.ForeignKey(CasePlay, on_delete=models.CASCADE, blank=True, null=True)
    suspect = models.ForeignKey(Suspect, on_delete=models.CASCADE, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=[('success', 'Success'), ('failed', 'Failed')])

    def __str__(self):
        return f"Result of GamePlay"
