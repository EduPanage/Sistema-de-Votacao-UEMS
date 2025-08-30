from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Election, Option, Voter, Vote
from .forms import ElectionForm, OptionForm, VoterForm
import hashlib
import uuid

def home(request):
    now = timezone.now()

    ativas = Election.objects.filter(
        is_published=True,
        start_date__lte=now,
        end_date__gte=now
    ).order_by('end_date')

    futuras = Election.objects.filter(
        is_published=True,
        start_date__gt=now
    ).order_by('start_date')

    encerradas = Election.objects.filter(
        is_published=True,
        end_date__lt=now
    ).order_by('-end_date')

    return render(request, "core/home.html", {
        "ativas": ativas,
        "futuras": futuras,
        "encerradas": encerradas
    })


def vote(request, election_id, token):
    # autenticação do eleitor via token
    voter = get_object_or_404(Voter, election_id=election_id, vote_token=token)
    election = voter.election

    if request.method == 'POST':
        option_id = request.POST.get('option')
        option = get_object_or_404(Option, id=option_id, election=election)

        # cria ou atualiza voto (re-votação)
        vote_obj, created = Vote.objects.update_or_create(
            election=election,
            voter=voter,
            defaults={'option': option}
        )

        # gera hash único do voto (comprovante)
        vote_str = f"{voter.id}-{option.id}-{timezone.now().timestamp()}"
        vote_obj.vote_hash = hashlib.sha256(vote_str.encode()).hexdigest()
        vote_obj.save()

        # marca eleitor como "já votou"
        voter.has_voted = True
        voter.save()

        return redirect("vote_success", vote_hash=vote_obj.vote_hash)

    return render(request, 'core/vote.html', {'election': election, 'voter': voter})


def vote_success(request, vote_hash):
    return render(request, 'core/vote_success.html', {'vote_hash': vote_hash})


# =========================
#   Rotas administrativas
# =========================

def create_election(request):
    # RF001 - criação de eleição
    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # depois podemos redirecionar para dashboard
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


def dashboard(request):
    # RF015 - dashboard de monitoramento
    return HttpResponse("Dashboard administrativo (em construção)")


#Pagina help.html pertencente a rota help/navbar
def help_page(request):
    return render(request, 'core/help.html')
