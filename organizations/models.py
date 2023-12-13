from datetime import timedelta
from django.conf import settings
from allauth.account.adapter import get_adapter
from django.contrib.sites.shortcuts import get_current_site

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone


class Organization(models.Model):
    slug = models.SlugField(max_length=16, blank=False, unique=True)
    name = models.CharField(max_length=64, blank=True)
    description = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    contact = models.JSONField(blank=True, default=dict)

    owner = models.ForeignKey(get_user_model(), null=True,
                              blank=True, on_delete=models.SET_NULL, related_name='+')

    def __str__(self):
        return self.slug

    class Meta:
        default_permissions = ()


class Membership(models.Model):
    WORKER = 'worker'
    SUPERVISOR = 'supervisor'
    MAINTAINER = 'maintainer'
    OWNER = 'owner'

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             null=True, related_name='memberships')

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE,
                                     related_name='members')
    is_active = models.BooleanField(default=False)
    joined_date = models.DateTimeField(null=True)
    role = models.CharField(max_length=16, choices=[
        (WORKER, 'Worker'),
        (SUPERVISOR, 'Supervisor'),
        (MAINTAINER, 'Maintainer'),
        (OWNER, 'Owner'),
    ])

    class Meta:
        default_permissions = ()
        unique_together = ('user', 'organization')


class Invitation(models.Model):
    key = models.CharField(max_length=64, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    sent_date = models.DateTimeField(null=True)
    owner = models.ForeignKey(
        get_user_model(), null=True, on_delete=models.SET_NULL)
    membership = models.OneToOneField(Membership, on_delete=models.CASCADE)

    @property
    def organization_id(self):
        return self.membership.organization_id

    @property
    def expired(self):

        # for checking if the invitation sent date is None
        if self.sent_date is None:
            return False

        expiration_date = self.sent_date + timedelta(
            days=settings.ORG_INVITATION_EXPIRY_DAYS,
        )
        return expiration_date <= timezone.now()

    @property
    def organization_slug(self):
        return self.membership.organization.slug

    def send(self, request):
        target_email = self.membership.user.email
        self.sent_date = timezone.now()
        self.save()

    def accept(self, date=None):
        if not self.membership.is_active:
            self.membership.is_active = True
            if date is None:
                self.membership.joined_date = timezone.now()
            else:
                self.membership.joined_date = date
            self.membership.save()

    class Meta:
        default_permissions = ()