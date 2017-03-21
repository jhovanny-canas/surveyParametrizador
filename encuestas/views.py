import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from .models import Encuesta,TipoPregunta, Pregunta, valuesPreguntas, tipoVariable, UserProfile
from django.db.models import Max
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_exempt
from encuestas.forms import UserForm


#login del prtal
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('/survey/')
            else:
                return HttpResponse("Your Django Hackathon account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'survey/login.html', {})

#pagina de logout
def user_logout(request):
    logout(request)
    return redirect('/login')



#pagina de registro

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            return render(request,
            'survey/register.html',{'user_form': user_form, 'registered': registered},)
        else:
            print user_form.errors
            return render(request,
            'survey/register.html',{'user_form': user_form, 'registered': registered},)
    else:
        user_form = UserForm()
        print user_form
        return render(request,
            'survey/register.html',{'user_form': user_form, 'registered': registered},)

#PAGINA DE INICIO
@login_required(login_url='/login/')
def index(request):
    return render(request, 'survey/home.html')
def home(request):
    pass


#SE CREA UNA NUEVA ENCUESTA, VALIDACION BASICA POR POST
@login_required(login_url='/login/')
def nuevaencuesta(request):
    if request.method == "GET":
        return render(request, 'survey/addencuesta.html')
    if request.method=="POST":
        if request.POST['nameencuesta'] and request.POST['descripcion']:
            encuestanueva=Encuesta()
            encuestanueva.nombre = request.POST['nameencuesta']
            encuestanueva.descripcion = request.POST['descripcion']
            encuestanueva.save()
            return redirect('/survey/configurar/%d' % encuestanueva.id)
        else:
            return render(request, 'survey/addencuesta.html', {'error_form':'Los campos no pueden ser vacios'})


#PAGINA QUE RECIBE LA ENCUESTA CREADA O NUEVA
@login_required(login_url='/login/')
@permission_required('encuestas.add_pregunta',login_url='/login/' )
def survey_setup(request, id_encuesta):
    encuesta = get_object_or_404(Encuesta, pk=id_encuesta)
    preguntas = encuesta.pregunta_set.all()
    return render(request, 'survey/homeEncuesta.html', {'encuesta': encuesta, 'preguntas': preguntas})

#lista todas las encuestas realziadas
#@login_required(login_url='/login/')
@permission_required('encuestas.add_encuesta',login_url='/login/' )
def survey(request):
    encuestas = Encuesta.objects.all()
    return render(request, 'survey/survey.html', {'encuestas':encuestas})

def deletesurvey(request,id_encuesta):
    encuesta = get_object_or_404(Encuesta, pk =id_encuesta)
    encuesta.delete()
    encuestas = Encuesta.objects.all()
    return render(request, 'survey/survey.html', {'encuestas':encuestas})


def maximoPregunta(id_encuesta):
    maximo = Pregunta.objects.filter(encuesta=id_encuesta).aggregate(Max('numeroPregunta'))
    return 1 if maximo['numeroPregunta__max'] is None else maximo['numeroPregunta__max'] + 1

def maximoRespuesta(id_pregunta):
    maximo=valuesPreguntas.objects.filter(numeroPregunta=id_pregunta).aggregate(Max('valor_id'))
    return 1 if maximo['valor_id__max'] is None else maximo['valor_id__max'] + 1



@permission_required('encuestas.add_pregunta',login_url='/login/' )
def addquestion(request, id_encuesta):
    paginas={"1": 'survey/questionTipeText.html', "2": 'survey/questionTypeNumber.html', "3": 'survey/questionTypeRadio.html', "4":'survey/questionTypeCheck.html', "5": 'survey/questionTypeFecha.html',
                "6": 'survey/questionTypeCanvas.html', "7": 'survey/questionTypeFoto.html', "8": 'survey/questionTypeAudio.html'}
    tipoPregunta = request.POST.get('typeQuestion')
    if request.POST.get('agregarpregunta'):

        encuesta=get_object_or_404(Encuesta, pk=id_encuesta)
        maxId = maximoPregunta(id_encuesta)
        pregunta = Pregunta(numeroPregunta=maxId, encuesta=encuesta)
        pregunta.save()
        data={'configuracion': maxId, 'consecutivo': pregunta.pk, 'tipo': tipoPregunta}
        request.session['consecutivo'] = pregunta.pk
        request.session['configuracion'] = maxId
        request.session['typequestion'] = tipoPregunta

        return render(request, paginas[tipoPregunta], data)

    if request.POST.get('cancel'):

        Pregunta.objects.get(id=request.POST.get('idquestion')).delete()
        del request.session['consecutivo']
        del request.session['configuracion']
        del request.session['typequestion']
        return redirect('/survey/configurar/%d' % int(id_encuesta))

    elif request.POST.get('agregar'):
        pregunta = Pregunta.objects.get(id=request.POST.get('idquestion'))
        pregunta.label=request.POST.get('txtPregunta')
        pregunta.textAyuda=request.POST.get('txtrecomendaciones')
        variable = tipoVariable.objects.get(id=request.POST.get('typeVariable'))
        a = TipoPregunta.objects.get(id=request.POST.get('typequestion'))
        pregunta.tipoPregunta = a
        pregunta.tipovariable=variable
        pregunta.minvalue = request.POST.get('minvalue')
        pregunta.maxvalue = request.POST.get('maxvalue')
        pregunta.save()
        del request.session['consecutivo']
        del request.session['configuracion']
        del request.session['typequestion']
        return redirect('/survey/configurar/%d' % int(id_encuesta))

    if request.method == "GET":
        if request.session['consecutivo'] is not None:
            return render(request, paginas[request.session['typequestion']], {'configuracion': request.session['configuracion'],'consecutivo':request.session['consecutivo']})
        else:
            return redirect('/survey/configurar/%d' % int(id_encuesta))

def addRespuesta(request, id_pregunta):
    pregunta =Pregunta.objects.get(id=id_pregunta)
    idmax = maximoRespuesta(id_pregunta)
    respuesta = valuesPreguntas(numeroPregunta=pregunta, valor_id=idmax, descripcion_valor=request.POST.get('txtnewopcion'))
    respuesta.save()
    totalrespuestas = valuesPreguntas.objects.filter(numeroPregunta=id_pregunta).values()
    nuevo = list(totalrespuestas)
    return HttpResponse(json.dumps(nuevo))



def deleteRespuesta(request, id_respuesta):
    respuesta= get_object_or_404(valuesPreguntas, pk=id_respuesta)
    preguntabase= respuesta.numeroPregunta
    secuencia = respuesta.valor_id
    respuesta.delete()
    registrossinactualizar = valuesPreguntas.objects.filter(numeroPregunta=preguntabase, valor_id__gt=secuencia).order_by('valor_id')
    for registro in registrossinactualizar:
        registro.valor_id = registro.valor_id-1;
        registro.save()
    totalrespuestas = valuesPreguntas.objects.filter(numeroPregunta=preguntabase).values()
    nuevo = list(totalrespuestas)
    return HttpResponse(json.dumps(nuevo))

def deletePregunta(request,id_encuesta, id_pregunta):
    encuesta = get_object_or_404(Encuesta, pk=id_encuesta)
    pregunta = get_object_or_404(Pregunta, pk=id_pregunta, encuesta=id_encuesta)
    if request.method == "POST":
        if request.POST.get('eliminar'):
            consecutivo = pregunta.numeroPregunta
            pregunta.delete()
            registrossinactualizar = Pregunta.objects.filter(encuesta=id_encuesta, numeroPregunta__gt=consecutivo).order_by('numeroPregunta')
            for registro in registrossinactualizar:
               registro.numeroPregunta = registro.numeroPregunta-1;
               registro.save()
            return redirect('/survey/configurar/%d' % int(id_encuesta))
    return render(request, 'survey/confirmarEliminarPregunta.html', {'pregunta':pregunta})


def editquestion(request, id_encuesta, id_pregunta):
    pregunta = get_object_or_404(Pregunta, pk=id_pregunta, encuesta=id_encuesta)
    if request.method =='POST':
        pregunta.label = request.POST.get('txtPregunta')
        pregunta.textAyuda = request.POST.get('txtrecomendaciones')
        pregunta.minvalue = request.POST.get('minvalue')
        pregunta.maxvalue = request.POST.get('maxvalue')
        pregunta.save()
        return redirect('/survey/configurar/%d' % int(id_encuesta))

    valores = valuesPreguntas.objects.filter(numeroPregunta=pregunta.id)
    return render(request, 'survey/editquestion.html', {'pregunta': pregunta, 'valores': valores})


        #asi se trabaja con json en python http://stackoverflow.com/questions/12353288/python-json-get-values
        # data = json.loads('{"lat":444, "lon":555}')
        # print data
        #print x['lat']
        # for key, value in data.items():
        #     print key, value

def flow(request, id_encuesta):
    if request.method == 'POST':
        resultados = request.POST.items()
        ret = request.POST
        list = json.loads(ret['parameter'])
        print list
        for x in list:
            pregunta = Pregunta.objects.get(pk= x['pregunta'])
            pregunta.salto= x['salto']
            pregunta.save()
    encuesta= get_object_or_404(Encuesta,pk=id_encuesta)
    preguntas=encuesta.pregunta_set.all()
    return render(request, 'survey/flow.html', {'preguntas': preguntas, 'id_encuesta':id_encuesta})



#flujo basico/ se recive los post como llegan
def flownormal(request, id_encuesta):
    if request.method == 'POST':
        resultados = request.POST.items()
        rangoPreguntas= (len(resultados)-1)/2
        for x in range(1,rangoPreguntas+1):
            parametroCon = "pregunta["+ str(x) +"].actual"
            idpregunta=request.POST.get(parametroCon)
            pregunta=Pregunta.objects.get(pk=idpregunta)
            saltoconse = "pregunta["+ str(x) +"].preguntadestino"
            pregunta.next = request.POST.get(saltoconse)
            pregunta.salto = "PASE(" + request.POST.get(saltoconse) +");"
            pregunta.save()
    encuesta= get_object_or_404(Encuesta,pk=id_encuesta)
    preguntas=encuesta.pregunta_set.all()
    return render(request, 'survey/flujobasico.html', {'preguntas': preguntas})



def flowavanzado(request, id_encuesta):
    if request.method == 'POST':
        resultados = request.POST.items()
        print(len(resultados))
        print(resultados)
        parametr = json.loads(request.POST.get('parameter'))
        for valor in parametr:
            pregunta =Pregunta.objects.get(pk=valor['pregunta'])
            pregunta.salto =  valor['salto']
            pregunta.save()
    encuesta= get_object_or_404(Encuesta,pk=id_encuesta)
    preguntas=encuesta.pregunta_set.all()
    return render(request, 'survey/flujoavanzado.html', {'preguntas': preguntas,'id_encuesta':id_encuesta})

