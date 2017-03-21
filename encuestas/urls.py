from django.conf.urls import url
from .import views

app_name = 'encuestas'

urlpatterns = [
    #pagina de inicio sin nada
    url(r'^$', views.index, name='index'),
    #pagina de registro
    url(r'^register/$', views.register, name='register'),
    #pagina de login
    url(r'^login/$', views.user_login, name='login'),
    #pagina de logouth
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^$', views.index, name='index'),
    url(r'^$', views.home, name='home'),
    url(r'^nueva_encuesta/$', views.nuevaencuesta, name='nuevaencuesta'),
    #survey/
    url(r'^survey/$', views.survey, name='survey'),
    #survey/encuesta_id
    url(r'^survey/configurar/(?P<id_encuesta>[0-9]+)/$', views.survey_setup, name='survey_setup'),
    #survey/deletesurvey/numero_encuesta
    url(r'^survey/deletesurvey/(?P<id_encuesta>[0-9]+)/$', views.deletesurvey, name='survey_delete'),
    #survey/configurar/numero_encuesta/addquestion
    url(r'^survey/configurar/(?P<id_encuesta>[0-9]+)/addquestion$', views.addquestion, name='survey_setup_addquestion'),
    #survey/configurar/addopcion/numero_pregunta
    url(r'^survey/configurar/addopcion/(?P<id_pregunta>[0-9]+)$', views.addRespuesta, name='survey_setup_addoption'),
    #survey/configurar/retiraropcion/id_respuesta
    url(r'^survey/configurar/retiraropcion/(?P<id_respuesta>[0-9]+)$', views.deleteRespuesta, name='survey_setup_removeoption'),
    #survey/configurar/eliminarpregunta/id_encuesta/id_pregunta
    url(r'^survey/configurar/eliminarpregunta/(?P<id_encuesta>[0-9]+)/(?P<id_pregunta>[0-9]+)$', views.deletePregunta, name='survey_setup_delquestion'),
    #survey/configurar/editpregunta/id_encuesta/id_pregunta
    url(r'^survey/configurar/editpregunta/(?P<id_encuesta>[0-9]+)/(?P<id_pregunta>[0-9]+)$', views.editquestion, name='survey_setup_editquestion'),
    #survey/configurar/flujo/id_encuesta basico
    url(r'^survey/configurar/flujo/(?P<id_encuesta>[0-9]+)', views.flow, name='survey_setup_flow'),
    #survey/configurar/flujo/id_encuesta  consecutivo
    url(r'^survey/configurar/flujobasico/(?P<id_encuesta>[0-9]+)', views.flownormal, name='survey_setup_flow_basico'),
    #survey/configurar/flujo/id_encuesta  avanzado
    url(r'^survey/configurar/flujoavanzado/(?P<id_encuesta>[0-9]+)', views.flowavanzado, name='survey_setup_flow_avanzado'),
]


