from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # participação do eleitor
    path('vote/<int:election_id>/<str:token>/', views.vote, name='vote'),
    path('vote/success/<str:vote_hash>/', views.vote_success, name='vote_success'),

    # rotas administrativas (para implementar depois)
    path('admin/election/create/', views.create_election, name='create_election'),
    path('admin/election/<int:election_id>/options/', views.manage_options, name='manage_options'),
    path('admin/election/<int:election_id>/voters/', views.manage_voters, name='manage_voters'),
    path('admin/dashboard/', views.dashboard, name='dashboard'),
]
