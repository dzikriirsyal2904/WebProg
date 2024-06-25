from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape, mark_safe
import uuid

class AccountUser(models.Model):
    account_user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    account_user_related_user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_user_fullname = models.CharField(max_length=255, null=False, editable=False)
    account_user_student_number = models.CharField(max_length=20, null=False)
    account_user_created_by = models.CharField(max_length=255, null=False)
    account_user_created_date = models.DateTimeField(editable=False, null=False, auto_now_add=True)
    account_user_updated_by = models.CharField(max_length=255, null=True)
    account_user_updated_date = models.DateTimeField(editable=False, null=False, auto_now=True)

    def str(self):
        return str(self.account_user_related_user)

    def unicode(self):
        return str(self.account_user_related_user)

    @property
    def friendly_profile(self):
        return mark_safe(u"%s <%s> %s %s %s %s %s %s" % (
            escape(self.account_user_id),
            escape(self.account_user_related_user),
            escape(self.account_user_fullname),
            escape(self.account_user_student_number),
            escape(self.account_user_created_by),
            escape(self.account_user_created_date),
            escape(self.account_user_updated_by),
            escape(self.account_user_updated_date)
        ))

    class Meta:
        ordering = ('account_user_related_user',)
        indexes = [
            models.Index(fields=['account_user_id', 'account_user_related_user']),
        ]