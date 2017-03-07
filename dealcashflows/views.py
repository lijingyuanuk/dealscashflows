# -*- coding: utf-8 -*-
import StringIO
import time
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from models import *


def index(request):
    return render_to_response('index.html', locals())


def find_deal(request):
    rs = []
    for deal in Deal.objects.order_by('id'):
        r = {
            'id': deal.id,
            'name': deal.name,
            'currency': deal.local_currency,
            'fund': deal.fund,
        }
        rs.append(r)

    return JsonResponse(rs, safe=False)


def find_cash(request):
    rs = []
    for cash in Cashflow.objects.order_by('id'):
        r = {
            'id': cash.id,
            'deal_id': cash.deal_id,
            'date': cash.value_date,
            'type': cash.cf_type,
            'cashflows': cash.cashflows,
        }
        rs.append(r)

    return JsonResponse(rs, safe=False)


def deal(request):
    name = request.POST.get('name')
    currency = request.POST.get('currency')
    fund = request.POST.get('fund')
    Deal.objects.create(
        name=name,
        local_currency=currency,
        fund=fund
    )
    return JsonResponse({"ok": True})


def delete_deal(request):
    id = request.POST.get('id')
    deal = Deal.objects.get(id=id)
    deal.delete()
    return JsonResponse({"ok": True})


def cash(request):
    deal_id = request.POST.get('deal_id')
    type = request.POST.get('type')
    date = request.POST.get('date')
    cashflows = request.POST.get('cashflows')
    print date
    ts = int(date[:-3])
    value_date = time.localtime(ts)
    value_date = time.strftime('%Y-%m-%d', value_date)
    Cashflow.objects.create(
        deal_id=deal_id,
        cf_type=type,
        value_date=value_date,
        cashflows=cashflows,
    )
    return JsonResponse({"ok": True})


def delete_cash(request):
    id = request.POST.get('id')
    cash = Cashflow.objects.get(id=id)
    cash.delete()
    return JsonResponse({"ok": True})

