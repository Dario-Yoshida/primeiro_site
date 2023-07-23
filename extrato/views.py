from django.shortcuts import render, redirect
from perfil.models import Conta, Categoria
from django.http import HttpResponse, FileResponse
from .models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime, timedelta
from django.template.loader import render_to_string
import os
from django.conf import settings
#from weasyprint import HTML
from io import BytesIO

def novo_valor(request):
    if request.method == 'GET':
        contas = Conta.objects.all()
        categorias = Categoria.objects.all()
        return render(request, 'novo_valor.html', {'contas':contas, 'categorias':categorias})
    elif request.method == "POST":
        valor = request.POST.get('valor')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta = request.POST.get('conta')
        tipo = request.POST.get('tipo')
        
        if len(valor.strip()) == 0 or len(categoria.strip()) == 0 or len(data.strip()) == 0 or len(conta.strip()) == 0 or len(tipo.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos obrigatórios!!')
            return redirect('/extrato/novo_valor')
        
        valores = Valores(
            valor=valor,
            categoria_id=categoria,
            descricao=descricao,
            data=data,
            conta_id=conta,
            tipo=tipo,
        )

        valores.save()

        conta = Conta.objects.get(id=conta)

        if tipo == 'E':
            conta.valor += int(valor)
        else:
            conta.valor -= int(valor)

        conta.save()

        #TODO mensagem de acordo com o tipo
        if tipo == 'S':
            mensagem = 'Saida '
        else:
            mensagem = 'Entrada '

        messages.add_message(request, constants.SUCCESS, f'{mensagem} cadastrada com sucesso')
        return redirect('/extrato/novo_valor')
    

def view_extrato(request):
    contas = Conta.objects.all()
    categorias = Categoria.objects.all()
    valores = Valores.objects.all()
    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')
    periodo_get = request.GET.get('periodo')

    #TODO: colocar um botão para zerar o filtro
    zerar_get = request.GET.get('zerar')
    if zerar_get:
        return render(request, 'view_extrato.html', {'valores':valores, 'contas':contas, 'categorias':categorias})
    
    #TODO: filtrar por periodo
    if periodo_get:
        dias = int(periodo_get)
        hoje = datetime.now()
        data_inicio = datetime.now() - timedelta(dias)
        valores = valores.filter(data__range=(data_inicio, hoje))

    
    if conta_get:
        valores = valores.filter(conta__id=conta_get)
    if categoria_get:
        valores = valores.filter(categoria__id=categoria_get)

    return render(request, 'view_extrato.html', {'valores':valores, 'contas':contas, 'categorias':categorias})


#def exportar_pdf(request):
 #   valores = Valores.objects.filter(data__month=datetime.now().month)

   # path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    #template_render = render_to_string(path_template, {'valores':valores})

    #path_output = BytesIO()

   # HTML(string=template_render).write_pdf(path_output)

    #path_output.seek(0)
    #return FileResponse(path_output, filename="extrato.pdf")