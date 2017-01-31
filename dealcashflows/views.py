# -*- coding: utf-8 -*-
import StringIO

import BeautifulSoup
import time
import xlwt
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


def login(request):
    msg = ''
    next_url = request.GET.get('next', '/')
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        next_url = request.POST.get('next', '/')
        user = auth.authenticate(username=username, password=password)
        print username, password
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(next_url)
        else:
            msg = u'username or password error'
    return render_to_response('login.html', locals())


def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect("/")


@login_required
def password(request):
    msg = ''
    if request.method == 'POST':
        password = request.POST.get('password', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        user = request.user

        if not user.check_password(password):
            msg = u'old password error'

        if password1 != password2:
            msg = u'two passwords not the same'

        if not msg:
            user.set_password(password1)
            user.save()
            return HttpResponseRedirect('/login/')

    return render_to_response('password.html', locals())


def output(request):
    data = request.POST.get('data')
    begin_index = int(request.POST.get('begin_index', 0))
    end_index = int(request.POST.get('end_index', -1))

    wb = xlwt.Workbook()
    ws = wb.add_sheet('output')

    soup = BeautifulSoup.BeautifulSoup(data)

    thead_soup = soup.find('thead')
    th_soups = thead_soup.findAll('th')
    th_soups = th_soups[begin_index:end_index]

    j = 0
    for th_soup in th_soups:
        th = th_soup.getText()
        ws.write(0, j, th)
        j += 1

    tbody_soup = soup.find('tbody')
    tr_soups = tbody_soup.findAll('tr')

    i = 1
    for tr_soup in tr_soups:
        td_soups = tr_soup.findAll('td')
        td_soups = td_soups[begin_index:end_index]

        j = 0
        for td_soup in td_soups:
            td = td_soup.getText()
            ws.write(i, j, td)
            j += 1

        i += 1

    s = StringIO.StringIO()
    wb.save(s)
    s.seek(0)
    data = s.read()
    response = HttpResponse(data)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="output.xls"'

    return response
