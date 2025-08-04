
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .config import DONATION_TIERS
from .rcon_utils import give_privilege
from .mono_utils import find_payment
from .invoice_utils import create_invoice

def index(request):
    return render(request, 'index.html', {'tiers': DONATION_TIERS})

def generate_invoice(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        amount = int(request.POST['amount'])
        link = create_invoice(nickname, amount)
        return redirect(link) if link else HttpResponse("Не вдалося створити рахунок", status=500)

def donate(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        amount = int(request.POST['amount'])
        if amount in DONATION_TIERS:
            privilege = DONATION_TIERS[amount]
            if find_payment(amount):
                result = give_privilege(nickname, privilege)
                return HttpResponse(f"✅ Оплата {amount} грн підтверджена!<br>Привілей <b>{privilege}</b> видано гравцю <b>{nickname}</b>!<br><br>RCON: {result}")
            else:
                return HttpResponse("❌ Платіж не знайдено.", status=400)
        return HttpResponse("❌ Невірна сума!", status=400)
