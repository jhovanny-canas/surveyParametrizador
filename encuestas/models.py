from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # Override the __unicode__() method to return out something meaningful!
    def __unicode__(self):
        return self.user.username


class Encuesta(models.Model):
    nombre=models.CharField(max_length=100)
    descripcion= models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class  TipoPregunta(models.Model):
    TIPO_PREGUNTA=(('1','Text'), ('2','Radio'), ('3','Check'), ('4','Date'),('5','canvas'),('6','foto'),('7','audio'),)
    tipopregunta=models.CharField(choices=TIPO_PREGUNTA, max_length=2)

    def __str__(self):
        return self.tipopregunta

class tipoVariable(models.Model):
    id_tipovariable = models.IntegerField()
    descripcion = models.CharField(max_length=100)
    class Meta:
         unique_together = (('id_tipovariable', 'descripcion'),)

    def __str__(self):
        return "{}{}".format(self.id_tipovariable, self.descripcion)


class Pregunta(models.Model):
    numeroPregunta = models.IntegerField()
    label = models.CharField(max_length=200)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE)
    tipoPregunta = models.ForeignKey(TipoPregunta, null=True)
    textAyuda = models.CharField(max_length=500)
    tipovariable = models.ForeignKey(tipoVariable, null=True)
    minvalue = models.IntegerField(null=True)
    maxvalue = models.IntegerField(null=True)
    salto= models.CharField(null=True,max_length=1000)
    next= models.IntegerField(null=True)

    def __str__(self):
        return '{}{}{}'.format(self.numeroPregunta, self.label, self.tipoPregunta)

    # class Meta:
    #     unique_together = (('numeroPregunta','encuesta'),)


class valuesPreguntas(models.Model):
    numeroPregunta=models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    valor_id=models.IntegerField()
    descripcion_valor=models.CharField(max_length=100)

    def __str__(self):
        return '{}{}{}'.format(self.numeroPregunta, self.valor_id, self.descripcion_valor)














