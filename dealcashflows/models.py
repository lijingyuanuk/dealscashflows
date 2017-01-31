# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone


class Deal(models.Model):

    CURRENCY_CHOICES = (
        ('GBP', 'GBP'),
        ('USD', 'USD'),
        ('EUR', 'EUR'),
        ('RMB', 'RMB'),
    )

    name = models.CharField(max_length=255, blank=True)
    local_currency = models.CharField(max_length=50, choices=CURRENCY_CHOICES, default='GBP')
    fund = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return self.name


class Cashflow(models.Model):
    CF_TYPE_CHOICES = (
        ('Equity', 'Equity'),
        ('Proceeds', 'Proceeds'),
    )

    deal = models.ForeignKey(Deal)
    value_date = models.DateField(default=timezone.now)
    cf_type = models.CharField(max_length=50, choices=CF_TYPE_CHOICES, default='Equity')
    cashflows = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.cashflows)
