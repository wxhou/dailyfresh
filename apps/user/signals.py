#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

logger = logging.getLogger('debug')


@receiver(post_save, sender=get_user_model())
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        logger.debug("signals create user<{}> token".format(instance.username))
        Token.objects.create(user=instance)
