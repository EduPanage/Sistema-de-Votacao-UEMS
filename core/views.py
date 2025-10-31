from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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

    return render(request, "core/pages/home.html", {
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
    return render(request, "core/elections/election_list.html", {
        "elections": elections, 
        "title": "Eleições Ativas"
    })


def list_future_elections(request):
    now = timezone.now()
    elections = Election.objects.filter(
        is_published=True,
        start_date__gt=now
    ).order_by('start_date')
    return render(request, "core/elections/election_list.html", {
        "elections": elections, 
        "title": "Eleições Futuras"
    })


def list_closed_elections(request):
    now = timezone.now()
    elections = Election.objects.filter(
        is_published=True,
        end_date__lt=now
    ).order_by('-end_date')
    return render(request, "core/elections/election_list.html", {
        "elections": elections, 
        "title": "Eleições Encerradas"
    })


@login_required
def vote(request, election_id):
    # Busca a eleição
    election = get_object_or_404(Election, id=election_id)
    
    # Verifica se a eleição está ativa
    now = timezone.now()
    if not election.is_published:
        messages.error(request, 'Esta eleição ainda não foi publicada.')
        return redirect('home')
    
    if now < election.start_date:
        messages.warning(request, f'Esta eleição ainda não começou. Início: {election.start_date.strftime("%d/%m/%Y %H:%M")}')
        return redirect('home')
    
    if now > election.end_date:
        messages.info(request, 'Esta eleição já foi encerrada. Você pode ver os resultados.')
        return redirect('election_results', election_id=election.id)
    
    # Verifica se o usuário logado é um eleitor válido para esta eleição
    try:
        voter = Voter.objects.get(
            election=election, 
            email__iexact=request.user.email
        )
    except Voter.DoesNotExist:
        messages.error(
            request, 
            f'Você não está autorizado a votar nesta eleição. '
            f'Seu e-mail ({request.user.email}) não está na lista de eleitores. '
            f'Entre em contato com o administrador se achar que isso é um erro.'
        )
        return render(request, 'core/pages/error.html', {
            'message': 'Você não está autorizado a votar nesta eleição.',
            'details': f'E-mail usado: {request.user.email}'
        })

    # Verifica se o eleitor já votou
    if voter.has_voted:
        messages.warning(request, 'Você já votou nesta eleição!')
        return render(request, 'core/voting/already_voted.html', {'election': election})

    # Lógica para processar o voto (POST)
    if request.method == 'POST':
        option_id = request.POST.get('option')
        if not option_id:
            messages.error(request, 'Por favor, selecione uma opção antes de votar.')
            options = election.options.all()
            return render(request, 'core/voting/vote.html', {
                'election': election,
                'options': options,
                'voter': voter
            })
        
        option = get_object_or_404(Option, id=option_id, election=election)
        
        # Cria o voto
        vote_obj = Vote.objects.create(
            election=election,
            voter=voter, 
            option=option
        )
        
        # Gera o hash (comprovante)
        vote_str = f"{voter.id}-{option.id}-{timezone.now().timestamp()}"
        vote_obj.vote_hash = hashlib.sha256(vote_str.encode()).hexdigest()
        vote_obj.save()
        
        # Marca o eleitor como "já votou"
        voter.has_voted = True
        voter.save()
        
        messages.success(request, 'Voto registrado com sucesso! Guarde seu comprovante.')
        return redirect("vote_success", vote_hash=vote_obj.vote_hash)

    # Renderiza a página de votação (GET)
    options = election.options.all()
    return render(request, 'core/voting/vote.html', {
        'election': election,
        'options': options,
        'voter': voter
    })


def vote_success(request, vote_hash):
    # Se o hash for 'already_voted', renderiza uma mensagem diferente
    if vote_hash == 'already_voted':
        return render(request, 'core/voting/already_voted.html')
    return render(request, 'core/voting/vote_success.html', {'vote_hash': vote_hash})


# =========================
#   Rotas administrativas
# =========================

@login_required
def create_election(request):
    """RF001 - Criação de eleição"""
    if request.method == 'POST':
        form = ElectionForm(request.POST, request.FILES)
        if form.is_valid():
            election = form.save(commit=False)
            election.created_by = request.user
            election.save()
            messages.success(request, 'Eleição criada com sucesso! Agora adicione os candidatos/opções.')
            return redirect('manage_options', election_id=election.id)
    else:
        form = ElectionForm()
    
    return render(request, 'core/elections/create_election.html', {'form': form})


@login_required
def manage_options(request, election_id):
    """RF002 - Definição de candidatos/opções"""
    election = get_object_or_404(Election, id=election_id)

    # Adicionar nova opção
    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.election = election
            option.save()
            messages.success(request, f'Opção "{option.name}" adicionada com sucesso!')
            return redirect('manage_options', election_id=election.id)
    else:
        form = OptionForm()

    options = election.options.all()
    return render(request, 'core/elections/manage_options.html', {
        'election': election,
        'options': options,
        'form': form
    })


@login_required
def delete_option(request, option_id):
    """Deletar uma opção/candidato"""
    option = get_object_or_404(Option, id=option_id)
    election_id = option.election.id
    option_name = option.name
    
    if request.method == 'POST':
        option.delete()
        messages.success(request, f'Opção "{option_name}" removida com sucesso!')
    
    return redirect('manage_options', election_id=election_id)


@login_required
def manage_voters(request, election_id):
    """RF003 / RF016 - Cadastro e gerenciamento de eleitores"""
    election = get_object_or_404(Election, id=election_id)

    if request.method == 'POST':
        form = VoterForm(request.POST)
        if form.is_valid():
            voter = form.save(commit=False)
            voter.election = election
            voter.vote_token = uuid.uuid4().hex
            voter.save()
            messages.success(request, f'Eleitor "{voter.name}" adicionado com sucesso!')
            return redirect('manage_voters', election_id=election.id)
    else:
        form = VoterForm()

    voters = election.voters.all()
    return render(request, 'core/elections/manage_voters.html', {
        'election': election,
        'voters': voters,
        'form': form
    })


@login_required
def delete_voter(request, voter_id):
    """Deletar um eleitor"""
    voter = get_object_or_404(Voter, id=voter_id)
    election_id = voter.election.id
    voter_name = voter.name
    
    if request.method == 'POST':
        voter.delete()
        messages.success(request, f'Eleitor "{voter_name}" removido com sucesso!')
    
    return redirect('manage_voters', election_id=election_id)


@login_required
def publish_election(request, election_id):
    """Publicar eleição - torna visível no home e notifica eleitores"""
    election = get_object_or_404(Election, id=election_id)
    
    if request.method == 'POST':
        # Validações antes de publicar
        if election.options.count() == 0:
            messages.error(request, 'Não é possível publicar uma eleição sem candidatos/opções!')
            return redirect('manage_options', election_id=election.id)
        
        if election.voters.count() == 0:
            messages.error(request, 'Não é possível publicar uma eleição sem eleitores!')
            return redirect('manage_voters', election_id=election.id)
        
        # Publica a eleição
        election.is_published = True
        election.save()
        
        # Envia e-mails para todos os eleitores
        send_election_notification(election)
        
        messages.success(request, f'🎉 Eleição "{election.theme}" publicada com sucesso! E-mails enviados para {election.voters.count()} eleitores.')
        return redirect('home')
    
    return redirect('manage_voters', election_id=election_id)


def send_election_notification(election):
    """Envia e-mail de notificação para todos os eleitores"""
    from django.conf import settings
    
    # URL base do site
    site_url = 'http://localhost:8000'  # Mudar para domínio real em produção
    vote_url = f"{site_url}/election/{election.id}/vote/"
    
    # Tipo de eleição legível
    election_type = 'Voto Único' if election.type == 'single' else 'Voto Múltiplo'
    
    # Formatar datas
    start_date = election.start_date.strftime('%d/%m/%Y às %H:%M')
    end_date = election.end_date.strftime('%d/%m/%Y às %H:%M')
    
    # Para cada eleitor
    for voter in election.voters.all():
        # Renderiza o template HTML
        html_message = render_to_string('core/emails/email_notification.html', {
            'voter_name': voter.name,
            'voter_email': voter.email,
            'election_theme': election.theme,
            'election_description': election.description,
            'election_type': election_type,
            'start_date': start_date,
            'end_date': end_date,
            'vote_url': vote_url,
        })
        
        # Versão em texto simples (fallback)
        plain_message = strip_tags(html_message)
        
        # Assunto do e-mail
        subject = f'Nova Eleição: {election.theme}'
        
        try:
            # Envia o e-mail
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[voter.email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            # Log do erro (não interrompe o processo)
            print(f"Erro ao enviar e-mail para {voter.email}: {str(e)}")


def election_results(request, election_id):
    """Exibir resultados da eleição"""
    election = get_object_or_404(Election, id=election_id)
    
    # Busca todas as opções da eleição e conta os votos para cada uma
    results = election.options.annotate(vote_count=Count('vote')).order_by('-vote_count')
    
    # Calcula total de votos
    total_votes = sum(result.vote_count for result in results)
    
    # Calcula porcentagem para cada opção
    for result in results:
        if total_votes > 0:
            result.percentage = (result.vote_count / total_votes) * 100
        else:
            result.percentage = 0
    
    return render(request, 'core/results/results.html', {
        'election': election,
        'results': results,
        'total_votes': total_votes,
    })


@login_required
def dashboard(request):
    """RF015 - Dashboard de monitoramento"""
    # Estatísticas gerais
    total_elections = Election.objects.filter(created_by=request.user).count()
    active_elections = Election.objects.filter(
        created_by=request.user,
        is_published=True,
        start_date__lte=timezone.now(),
        end_date__gte=timezone.now()
    ).count()
    
    # Eleições do usuário
    my_elections = Election.objects.filter(created_by=request.user).order_by('-start_date')
    
    return render(request, 'core/admin/dashboard.html', {
        'total_elections': total_elections,
        'active_elections': active_elections,
        'my_elections': my_elections,
    })


def help_page(request):
    """Página de ajuda"""
    return render(request, 'core/pages/help.html')