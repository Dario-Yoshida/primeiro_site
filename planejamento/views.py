from django.shortcuts import render
from perfil.models import Categoria
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime

# Create your views here.
def definir_planejamento(request):
    categorias = Categoria.objects.all()
    return render(request, 'definir_planejamento.html', {'categorias':categorias})


@csrf_exempt
def update_valor_categoria(request, id):
    valores = json.loads(request.body)
    novo_valor = valores["novo_valor"]

    categoria = Categoria.objects.get(id=id)
    categoria.valor_planejado = novo_valor
    categoria.save()

    return JsonResponse({'status': 'Sucesso'})


def ver_planejamento(request):
    categorias = Categoria.objects.all()
    #TODO: Realizar barra com total
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes = datetime.now().month
    mes_extenso = meses[mes-1]
    
    from extrato.models import Valores
    valores = Valores.objects.filter(data__month=mes).filter(tipo='S')
    total_categoria = 0
    for categoria in categorias:
        total_categoria += categoria.valor_planejado

    total_geral = 0
    for valor in valores:
        total_geral += valor.valor
    
    porcentagem = int((total_geral * 100) / total_categoria)
        
    return render(request, 'ver_planejamento.html', {'categorias': categorias, 'total_geral':total_geral, 'total_categoria':total_categoria, 'porcentagem':porcentagem, 'mes_extenso':mes_extenso})
