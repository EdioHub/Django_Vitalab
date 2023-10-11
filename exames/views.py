from django.shortcuts import render, redirect
from .models import TiposExames, PedidosExames, SolicitacaoExame
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import constants


@login_required
def solicitar_exames(request):
    tipos_exames = TiposExames.objects.all()
    if request.method == "GET":
        return render(request, 'solicitar_exames.html', {'tipos_exames': tipos_exames})
    else:
        exames_id = request.POST.getlist('exames')

        solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
        # preco_total = solicitacao_exames.aggregate(total=Sum('preco'))['total']
        preco_total = 0
        for i in solicitacao_exames:
            if i.disponivel:
                preco_total += i.preco
        # print(preco_total)

        return render(request, 'solicitar_exames.html', {'solicitacao_exames': solicitacao_exames, 'preco_total': preco_total, 'tipos_exames': tipos_exames})


@login_required
def fechar_pedido(request):
    exames_id = request.POST.getlist('exames')
    solicitacao_exames = TiposExames.objects.filter(id__in=exames_id)
    # print(exames_id)
    pedido_exame = PedidosExames(
        usuario=request.user,
        data=datetime.now()
    )

    pedido_exame.save()

    for exame in solicitacao_exames:
        solicitacao_exames_temp = SolicitacaoExame(
            usuario=request.user,
            exame=exame,
            status="E"
        )
        solicitacao_exames_temp.save()
        pedido_exame.exames.add(solicitacao_exames_temp)

    pedido_exame.save()

    messages. add_message(request, constants.SUCCESS,
                          ('Pedido de exame realizado com sucesso'))

    return redirect('/exames/gerenciar_pedidos')


def gerenciar_pedidos(request):
    return render(request, 'gerenciar_pedidos.html')
