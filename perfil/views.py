from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import calcula_total, calcula_equilibrio_financeiro
from datetime import datetime
from extrato.models import Valores

# Create your views here.
def home(request):
    from contas.models import ContaPaga, ContaPagar
    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day
    
    contas = Conta.objects.all()
    total_conta = calcula_total(contas, 'valor')

    valores = Valores.objects.filter(data__month=MES_ATUAL)
    entrada = valores.filter(tipo='E')
    total_entrada = calcula_total(entrada, 'valor')
    
    saida = valores.filter(tipo='S')
    total_saida = calcula_total(saida, 'valor')

    saldo_mes = total_entrada - total_saida

    percen_essencial, percen_nao_essencial = calcula_equilibrio_financeiro()


    contas_pagar = ContaPagar.objects.all()
    pagar = len(contas_pagar)
    valor_mes = 0
    for conta_pg in contas_pagar:
        valor_mes += conta_pg.valor

    valor_livre = total_entrada - valor_mes

    contas_pagas = ContaPaga.objects.filter(data_pagamento__month=MES_ATUAL).values('conta')
    pagas = len(contas_pagas)

    contas_vencidas = contas_pagar.filter(dia_pagamento__lt=DIA_ATUAL).exclude(id__in=contas_pagas)
    vencidas = len(contas_vencidas)

    contas_proximas_vencimento = contas_pagar.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gte=DIA_ATUAL).exclude(id__in=contas_pagas)
    proximas = len(contas_proximas_vencimento)

    return render(request, 'home.html', {'valor_livre':valor_livre, 'valor_mes':valor_mes, 'saldo_mes':saldo_mes, 'vencidas':vencidas, 'proximas':proximas, 'percen_nao_essencial':percen_nao_essencial, 'percen_essencial':percen_essencial, 'total_saida':total_saida, 'total_entrada': total_entrada, 'contas':contas, 'total_conta':total_conta})


def gerenciar(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    total_conta = calcula_total(contas, 'valor')
    
    return render(request, "gerenciar.html", {'contas':contas, 'total_conta':total_conta, 'categorias':categorias})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0 or len(banco.strip()) == 0 or len(tipo.strip()) == 0:
        # mensagem erro
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')

    conta = Conta(
        apelido=apelido,
        banco=banco,
        tipo=tipo,
        valor=valor,
        icone=icone
    )

    conta.save()
    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com Sucesso!')
    return redirect('/perfil/gerenciar/')

def deletar_banco(request, id):
    conta = Conta.objects.get(id=id)
    conta.delete()

    messages.add_message(request, constants.SUCCESS, 'Banco deletado com sucesso!')
    return redirect('/perfil/gerenciar/')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    #validar nome e (essencial = isinstance = True ou False)
    if len(nome.strip()) == 0 or not isinstance(essencial, bool):
        # mensagem erro
        messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar/')

    categoria = Categoria(
        categoria=nome,
        essencial=essencial
    )

    categoria.save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso')
    return redirect('/perfil/gerenciar/')


def update_categoria(request, id):
    categoria = Categoria.objects.get(id=id)
    categoria.essencial = not categoria.essencial
    categoria.save()

    return redirect('/perfil/gerenciar/')


def dashboard(request):
    dados = {}

    categorias = Categoria.objects.all()

    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria=categoria)
        for v in valores:
            total += v.valor
        dados[categoria.categoria] = total

    return render(request, 'dashboard.html', {'labels': list(dados.keys()), 'values': list(dados.values())})