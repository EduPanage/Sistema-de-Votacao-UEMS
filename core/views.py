from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count
from .models import Election, Option, Voter, Vote
from .forms import ElectionForm, OptionForm, VoterForm
import hashlib
import uuid

def home(request):
    now = timezone.now()

    # Limita a 4 eleições por categoria
    ativas = Election.objects.filter(
        is_published=True,
        start_date__lte=now,
        end_date__gte=now
    ).order_by('end_date')[:4]

    futuras = Election.objects.filter(
        is_published=True,
        start_date__gt=now
    ).order_by('start_date')[:4]

    encerradas = Election.objects.filter(
        is_published=True,
        end_date__lt=now
    ).order_by('-end_date')[:4]

    # Novos destaques: 3 eleições mais recentes encerradas
    recentes = Election.objects.filter(
        is_published=True,
        end_date__lt=now
    ).order_by('-end_date')[:3]

    # Verifica se há mais de 4 eleições por categoria (para botão "Ver Mais")
    show_more_active = Election.objects.filter(
        is_published=True, start_date__lte=now, end_date__gte=now
    ).count() > 4
    show_more_future = Election.objects.filter(
        is_published=True, start_date__gt=now
    ).count() > 4
    show_more_closed = Election.objects.filter(
        is_published=True, end_date__lt=now
    ).count() > 4

    return render(request, "core/home.html", {
        "ativas": ativas,
        "futuras": futuras,
        "encerradas": encerradas,
        "recentes": recentes,  
        "show_more_active": show_more_active,
        "show_more_future": show_more_future,
        "show_more_closed": show_more_closed,
    })

def list_active_elections(request):
    now = timezone.now()
    elections = Election.objects.filter(
        is_published=True,
        start_date__lte=now,
        end_date__gte=now
    ).order_by('end_date')
    return render(request, "core/election_list.html", {"elections": elections, "title": "Eleições Ativas"})


def list_future_elections(request):
    now = timezone.now()
    elections = Election.objects.filter(
        is_published=True,
        start_date__gt=now
    ).order_by('start_date')
    return render(request, "core/election_list.html", {"elections": elections, "title": "Eleições Futuras"})


def list_closed_elections(request):
    now = timezone.now()
    elections = Election.objects.filter(
        is_published=True,
        end_date__lt=now
    ).order_by('-end_date')
    return render(request, "core/election_list.html", {"elections": elections, "title": "Eleições Encerradas"})


@login_required
def vote(request, election_id):
    # Busca a eleição
    election = get_object_or_404(Election, id=election_id)
    
    # 1. Verifica se o usuário logado é um eleitor válido para esta eleição
    try:
        voter = Voter.objects.get(election=election, email=request.user.email)
    except Voter.DoesNotExist:
        # Se o e-mail do usuário logado não estiver na lista de eleitores
        # pode redirecionar para uma página de erro ou mostrar uma mensagem
        return render(request, 'core/error.html', {'message': 'Você não está autorizado a votar nesta eleição.'})

    # 2. Verifica se o eleitor já votou
    if voter.has_voted:
        return render(request, 'core/already_voted.html', {'election': election})

    # Lógica para processar o voto (POST)
    if request.method == 'POST':
        option_id = request.POST.get('option')
        option = get_object_or_404(Option, id=option_id, election=election)
        
        # Cria o voto
        vote_obj = Vote.objects.create(election=election,voter=voter, option=option
        )
        
        # Gera o hash (comprovante)
        vote_str = f"{voter.id}-{option.id}-{timezone.now().timestamp()}"
        vote_obj.vote_hash = hashlib.sha256(vote_str.encode()).hexdigest()
        vote_obj.save()
        
        # Marca o eleitor como "já votou"
        voter.has_voted = True
        voter.save()
        
        return redirect("vote_success", vote_hash=vote_obj.vote_hash)

    # Renderiza a página de votação (GET)
    options = election.options.all()
    return render(request, 'core/vote.html', {'election': election,'options': options,'voter': voter})


def vote_success(request, vote_hash):
    # Se o hash for 'already_voted', renderiza uma mensagem diferente
    if vote_hash == 'already_voted':
        return render(request, 'core/vote_already_voted.html')
    return render(request, 'core/vote_success.html', {'vote_hash': vote_hash})


# =========================
#   Rotas administrativas
# =========================

@login_required
def create_election(request):
    # RF001 - criação de eleição
    if request.method == 'POST':
        form = ElectionForm(request.POST, request.FILES)
        if form.is_valid():
            election = form.save(commit=False)
            election.created_by = request.user
            election.save()
            # Redireciona para a página de gerenciamento de opções
            return redirect('manage_voters', election_id=election.id)
    else:
        form = ElectionForm()
    
    return render(request, 'core/create_election.html', {'form': form})


def manage_options(request, election_id):
    # RF002 - definição de candidatos/opções
    election = get_object_or_404(Election, id=election_id)

    # adicionar nova opção
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.election = election
            option.save()
            return redirect('manage_options', election_id=election.id)
    else:
        form = OptionForm()

    options = election.options.all()
    return render(request, 'core/manage_options.html', {
        'election': election,
        'options': options,
        'form': form
    })


def manage_voters(request, election_id):
    # RF003 / RF016 - cadastro e gerenciamento de eleitores
    election = get_object_or_404(Election, id=election_id)

    if request.method == 'POST':
        form = VoterForm(request.POST)
        if form.is_valid():
            voter = form.save(commit=False)
            voter.election = election
            voter.vote_token = uuid.uuid4().hex  # gera token único
            voter.save()
            return redirect('manage_voters', election_id=election.id)
    else:
        form = VoterForm()

    voters = election.voters.all()
    return render(request, 'core/manage_voters.html', {
        'election': election,
        'voters': voters,
        'form': form
    })

def election_results(request, election_id):
    # Busca a eleição
    election = get_object_or_404(Election, id=election_id)
    
    # Busca todas as opções da eleição e conta os votos para cada uma
    results = election.options.annotate(vote_count=Count('vote')).order_by('-vote_count')
    
    return render(request, 'core/results.html', {
        'election': election,
        'results': results,
    })


def dashboard(request):
    # RF015 - dashboard de monitoramento
    return HttpResponse("Dashboard administrativo (em construção)")


#Pagina help.html pertencente a rota help/navbar
def help_page(request):
    return render(request, 'core/help.html')
