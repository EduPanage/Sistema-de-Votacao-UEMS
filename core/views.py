from django.shortcuts import render, get_object_or_404, redirect
from .models import Election, Option, Voter, Vote
from django.utils import timezone
import hashlib

def home(request):
    now = timezone.now()
    elections = Election.objects.filter(is_published=True, start_date__lte=now, end_date__gte=now)
    return render(request, "core/home.html", {"elections": elections})

def vote(request, election_id):
    voter = request.voter
    election = voter.election

    if request.method == 'POST':
        option_id = request.POST.get('option')
        option = get_object_or_404(Option, id=option_id, election=election)

        vote_obj, created = Vote.objects.update_or_create(
            election=election,
            voter=voter,
            defaults={'option': option}
        )

        vote_str = f"{voter.id}-{option.id}-{timezone.now().timestamp()}"
        vote_obj.vote_hash = hashlib.sha256(vote_str.encode()).hexdigest()
        vote_obj.save()

        voter.has_voted = True
        voter.save()

        return render(request, 'core/vote_success.html', {'vote_hash': vote_obj.vote_hash})

    return render(request, 'core/vote.html', {'election': election, 'voter': voter})
