from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Participação do eleitor
    path('election/<int:election_id>/vote/', views.vote, name='vote'),
    path('vote/success/<str:vote_hash>/', views.vote_success, name='vote_success'),
    path('election/<int:election_id>/results/', views.election_results, name='election_results'),
    
    # Rotas administrativas (customizadas)
    path('painel/election/create/', views.create_election, name='create_election'),
    path('painel/election/<int:election_id>/options/', views.manage_options, name='manage_options'),
    path('painel/election/<int:election_id>/voters/', views.manage_voters, name='manage_voters'),
    path('painel/election/<int:election_id>/publish/', views.publish_election, name='publish_election'),
    path('painel/dashboard/', views.dashboard, name='dashboard'),
    
    # Rotas de exclusão
    path('painel/option/<int:option_id>/delete/', views.delete_option, name='delete_option'),
    path('painel/voter/<int:voter_id>/delete/', views.delete_voter, name='delete_voter'),

    # Rotas navbar ajuda
    path('help/', views.help_page, name='help'),
]