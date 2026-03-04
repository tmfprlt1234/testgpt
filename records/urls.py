from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('records/<int:record_id>/edit/', views.edit_record, name='edit_record'),
    path('records/<int:record_id>/delete/', views.delete_record, name='delete_record'),
]
