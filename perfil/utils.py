from datetime import datetime

def calcula_total(obj, campo):
    total = 0
    for i in obj:
        total += getattr(i, campo)
    return total


def calcula_equilibrio_financeiro():
    from extrato.models import Valores
    gastos = Valores.objects.filter(data__month=datetime.now().month).filter(tipo='S')
    essenciais = gastos.filter(categoria__essencial=True)
    nao_essenciais = gastos.filter(categoria__essencial=False)

    total_essencial = calcula_total(essenciais, 'valor')
    total_nao_essencial = calcula_total(nao_essenciais, 'valor')

    total = total_nao_essencial + total_essencial

    try:
        percen_essencial = int((total_essencial / total) * 100)
        percen_nao_essencial = int((total_nao_essencial / total) * 100)
        return percen_essencial, percen_nao_essencial
    except:
        return 0,0
