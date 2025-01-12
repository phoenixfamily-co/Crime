from django.db import models

from Order.models import OrderItem
from User.models import User


class CasePlay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    orderItem = models.ForeignKey(OrderItem, on_delete=models.CASCADE, blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('in_progress', 'In Progress'), ('completed', 'Completed'),
                                                      ('cancelled', 'Cancelled')],
                              default='in_progress')

    def __str__(self):
        return f"GamePlay of {self.orderItem.case.title} by {self.user.number}"


class CaeParticipant(models.Model):
    gameplay = models.ForeignKey(CasePlay, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Participant {self.participant.number} in GamePlay {self.gameplay.id}"


class GameResult(models.Model):
    gameplay = models.OneToOneField(CasePlay, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('success', 'Success'), ('failed', 'Failed')])

    def __str__(self):
        return f"Result of GamePlay {self.gameplay.id}"
