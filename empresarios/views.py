from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants

from investidores.models import PropostaInvestimento
from .models import Documento, Empresas, Metricas
from .utils import valida_cnpj, valida_site


# Create your views here.


@login_required(login_url='/user/logar')  # type: ignore
def cadastrar_empresa(request):
    if request.method == "GET":
        return render(request, 'cadastrar_empresa.html', {'tempo_existencia': Empresas.tempo_existencia_choices, 'areas': Empresas.area_choices, 'publicos_alvo': Empresas.publico_alvo_choices})
    elif request.method == "POST":
        nome = request.POST.get('nome')
        cnpj = request.POST.get('cnpj')
        site = request.POST.get('site')
        tempo_existencia = request.POST.get('tempo_existencia')
        descricao = request.POST.get('descricao')
        data_final = request.POST.get('data_final')
        percentual_equity = request.POST.get('percentual_equity')
        estagio = request.POST.get('estagio')
        area = request.POST.get('area')
        publico_alvo = request.POST.get('publico_alvo')
        valor = request.POST.get('valor')
        pitch = request.FILES.get('pitch')
        logo = request.FILES.get('logo')

        if not nome:
            messages.add_message(request, constants.ERROR,
                                 'O nome é obrigatório')
            return redirect(reverse('cadastrar_empresa'))
        if not cnpj:
            messages.add_message(request, constants.ERROR,
                                 'O CNPJ é obrigatório')
            return redirect(reverse('cadastrar_empresa'))

        if not descricao:
            messages.add_message(request, constants.ERROR,
                                 'A descrição é obrigatória')
            return redirect(reverse('cadastrar_empresa'))
        if not data_final:
            messages.add_message(request, constants.ERROR,
                                 'A data final é obrigatória')
            return redirect(reverse('cadastrar_empresa'))
        if not percentual_equity:
            messages.add_message(request, constants.ERROR,
                                 'O percentual de equity é obrigatório')
            return redirect(reverse('cadastrar_empresa'))
        if not estagio:
            messages.add_message(request, constants.ERROR,
                                 'O estágio é obrigatório')
            return redirect(reverse('cadastrar_empresa'))

        if estagio not in [ocpao[0] for ocpao in Empresas.estagio_choices]:

            messages.add_message(request, constants.ERROR,
                                 'Selecione um estágio válido')
            return redirect(reverse('cadastrar_empresa'))

        if not valida_cnpj(request, cnpj):
            return redirect(reverse('cadastrar_empresa'))

        if not site:
            messages.add_message(request, constants.ERROR,
                                 'O site é obrigatório')
            return redirect(reverse('cadastrar_empresa'))
        if not valida_site(request, site):
            return redirect(reverse('cadastrar_empresa'))
        if not valor:
            messages.add_message(request, constants.ERROR,
                                 'O valor é obrigatório')
            return redirect(reverse('cadastrar_empresa'))

        if not pitch:
            messages.add_message(request, constants.ERROR,
                                 'Selecione um arquivo de pitch')

            return redirect(reverse('cadastrar_empresa'))
        if not logo:
            messages.add_message(request, constants.ERROR,
                                 'Selecione um arquivo de logo')

            return redirect(reverse('cadastrar_empresa'))
        if not tempo_existencia:
            messages.add_message(request, constants.ERROR,
                                 'Selecione um tempo de existência')
        if tempo_existencia not in [ocpao[0] for ocpao in Empresas.tempo_existencia_choices]:

            messages.add_message(request, constants.ERROR,
                                 'Selecione um tempo de existência válido')
            return redirect(reverse('cadastrar_empresa'))

        if not area:
            messages.add_message(request, constants.ERROR,
                                 'Selecione uma área')
            return redirect(reverse('cadastrar_empresa'))

        if area not in [ocpao[0] for ocpao in Empresas.area_choices]:
            messages.add_message(request, constants.ERROR,
                                 'Selecione uma área válida')
            return redirect(reverse('cadastrar_empresa'))

        if not publico_alvo:
            messages.add_message(request, constants.ERROR,
                                 'Selecione um público alvo')
        if publico_alvo not in [ocpao[0] for ocpao in Empresas.publico_alvo_choices]:
            messages.add_message(request, constants.ERROR,
                                 'Selecione um público alvo válido')
            return redirect(reverse('cadastrar_empresa'))
        try:
            empresa = Empresas(
                user=request.user,
                nome=nome,
                cnpj=cnpj,
                site=site,
                tempo_existencia=tempo_existencia,
                descricao=descricao,
                data_final_captacao=data_final,
                percentual_equity=percentual_equity,
                estagio=estagio,
                area=area,
                publico_alvo=publico_alvo,
                valor=valor,
                pitch=pitch,
                logo=logo
            )
            empresa.save()
        except:
            messages.add_message(request, constants.ERROR,
                                 'Erro interno do sistema')
            return redirect(reverse('cadastrar_empresa'))

        messages.add_message(request, constants.SUCCESS,
                             'Empresa criada com sucesso')
        return redirect(reverse('cadastrar_empresa'))


@login_required(login_url='/user/logar/')
def listar_empresas(request):
    if request.method == "GET":

        empresas = Empresas.objects.filter(user=request.user)
        return render(request, 'listar_empresas.html', {'empresas': empresas})

    elif request.method == "POST":
        nome = request.POST.get('empresa')
        empresas = Empresas.objects.filter(nome__icontains=nome, user=request.user)
        return render(request, 'listar_empresas.html', {'empresas': empresas})
        

@login_required(login_url='/user/logar/')
def empresa(request, id):

    empresa = Empresas.objects.get(id=id)
    if request.method == "GET":
        documentos = Documento.objects.filter(empresa=empresa)
        proposta_investimentos = PropostaInvestimento.objects.filter(
            empresa=empresa)
        percentual_vendido = 0
        for pi in proposta_investimentos:
            if pi.status == 'PA':
                percentual_vendido += pi.percentual

        proposta_investimentos_enviada = proposta_investimentos.filter(
            status='PE')
        total_captado = sum(proposta_investimentos.filter(status='PA').values_list('valor', flat=True))
        valuation_atual = (100 * float(total_captado)) / float(percentual_vendido) if percentual_vendido != 0 else 0
        return render(request, 'empresa.html', {'empresa': empresa, 'documentos': documentos, 'proposta_investimentos_enviada': proposta_investimentos_enviada,'percentual_vendido':int(percentual_vendido),'total_captado':total_captado,'valuation_atual':valuation_atual })


def add_doc(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    arquivo = request.FILES.get('arquivo')
    extensao = arquivo.name.split('.')

    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR,
                             "Essa empresa não é sua")
        return redirect(reverse('listar_empresas'))

    if extensao[1] != 'pdf':
        messages.add_message(request, constants.ERROR, "Envie apenas PDF's")
        return redirect(f'/empresarios/empresa/{empresa.id}')

    if not arquivo:
        messages.add_message(request, constants.ERROR, "Envie um arquivo")
        return redirect(f'/empresarios/empresa/{empresa.id}')

    documento = Documento(
        empresa=empresa,
        titulo=titulo,
        arquivo=arquivo
    )
    documento.save()
    messages.add_message(request, constants.SUCCESS,
                         "Arquivo cadastrado com sucesso")
    return redirect(f'/empresarios/empresa/{empresa.id}')


def excluir_dc(request, id):
    documento = Documento.objects.get(id=id)
    if documento.empresa.user != request.user:
        messages.add_message(request, constants.ERROR,
                             "Essa empresa não é sua")
        return redirect(reverse('listar_empresas'))
    documento.delete()
    messages.add_message(request, constants.SUCCESS,
                         "Documento excluído com sucesso")
    return redirect(f'/empresarios/empresa/{documento.empresa.id}')


def add_metrica(request, id):
    empresa = Empresas.objects.get(id=id)
    titulo = request.POST.get('titulo')
    valor = request.POST.get('valor')
    if empresa.user != request.user:
        messages.add_message(request, constants.ERROR,
                             "Essa empresa não é sua")
        return redirect(reverse('listar_empresas'))

    metrica = Metricas(
        empresa=empresa,
        titulo=titulo,
        valor=valor
    )
    metrica.save()

    messages.add_message(request, constants.SUCCESS,
                         "Métrica cadastrada com sucesso")
    return redirect(f'/empresarios/empresa/{empresa.id}')


def gerenciar_proposta(request, id):
    acao = request.GET.get('acao')
    pi = PropostaInvestimento.objects.get(id=id)

    if acao == 'aceitar':
        messages.add_message(request, constants.SUCCESS, 'Proposta aceita')
        pi.status = 'PA'
    elif acao == 'recusar':
        messages.add_message(request, constants.SUCCESS, 'Proposta recusada')
        pi.status = 'PR'

    pi.save()
    return redirect(f'/empresarios/empresa/{pi.empresa.id}')
