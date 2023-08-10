from django.db import models

from users.models import ClientUser, SupportSystemUser


class Ticket(models.Model):

    STATUS_CHOICES = [
        ('solved', 'Solved'),
        ('unsolved', 'Unsolved'),
        ('frozen', 'Frozen'),
    ]

    creator = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unsolved')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.creator} | {self.subject}"


class BaseMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.pk} | {self.ticket} | {self.message} | {self.user.email}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.parent_message:
            self.ticket = self.parent_message.ticket
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)


class SupportSystemMessage(BaseMessage):
    user = models.ForeignKey(SupportSystemUser, on_delete=models.CASCADE)
    parent_message = models.ForeignKey("ClientMessage", on_delete=models.CASCADE,
                                       null=True, blank=True, related_name="client_replies")


class ClientMessage(BaseMessage):
    user = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    parent_message = models.ForeignKey("SupportSystemMessage", on_delete=models.CASCADE,
                                       null=True, blank=True, related_name="support_replies")
