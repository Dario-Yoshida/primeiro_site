from django.db import models
from datetime import datetime
from perfil.utils import calcula_total

class Categoria(models.Model):
    categoria = models.CharField(max_length=50)
    essencial = models.BooleanField(default=False)
    valor_planejado = models.FloatField(default=0)

    def __str__(self):
        return self.categoria
    
    def total_gasto(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(categoria__id=self.id).filter(data__month=datetime.now().month).filter(tipo='S')
        
        #def  = calcula_total(contas, 'valor')
        total_valor = calcula_total(valores, 'valor')
        return total_valor
    
    def total_geral(self):
        from extrato.models import Valores
        valores = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S')
        #def  = calcula_total(contas, 'valor')
        total_geral_valor = calcula_total(valores, 'valor')
        return total_geral_valor
    
    def calcula_percentual_gasto_por_categoria(self):
        return int((self.total_gasto() * 100) / self.valor_planejado)
    

class Conta(models.Model):
    banco_choice = (
        ('NU', 'Nubank'),
        ('CE', 'Caixa Economica'),
    )

    tipo_choice = (
        ('pf', 'Pessoa Física'),
        ('pj', 'Pessoa Jurídica')
    )

    apelido = models.CharField(max_length=50)
    banco = models.CharField(max_length=2, choices=banco_choice)
    tipo = models.CharField(max_length=2, choices=tipo_choice)
    valor = models.FloatField()
    icone = models.ImageField(upload_to="icones")

    def __str__(self):
        return self.apelido
      

