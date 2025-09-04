from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # participação do eleitor
     path('election/<int:election_id>/vote/', views.vote, name='vote'),
    path('vote/success/<str:vote_hash>/', views.vote_success, name='vote_success'),

    # rotas administrativas (customizadas)
    path('painel/election/create/', views.create_election, name='create_election'),
    path('painel/election/<int:election_id>/options/', views.manage_options, name='manage_options'),
    path('painel/election/<int:election_id>/voters/', views.manage_voters, name='manage_voters'),
    path('painel/dashboard/', views.dashboard, name='dashboard'),

    #rotas navbar ajuda
    path('help/', views.help_page, name='help'),
]

