from django.urls import path
from . import views

urlpatterns = [
    path('',                        views.workflow_home,      name='workflow_home'),
    path('add/',                    views.add_application,    name='add_application'),
    path('<int:pk>/',               views.detail,             name='detail'),
    path('<int:pk>/advance/',       views.advance_stage,      name='advance_stage'),
    path('<int:pk>/delete/',        views.delete_application, name='delete_application'),
    path('run/<str:name>/',         views.run_workflow,       name='run_workflow'),
]
