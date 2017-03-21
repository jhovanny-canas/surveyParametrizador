  
function condiciones(pregunta,idpregunta, condiciones)
{
   return "{'"+ pregunta + "':" + idpregunta + ",'salto':'PASE(" + condiciones + ");'}";
}


$(document).ready(function() {

 $("form").submit(function(e){
        e.preventDefault();
        var parametros =[];
       $(".logicaEncabezado").each(function(index) {
        var numeropregunta = $(this).attr('data-idpreg');
        var idpregunta = $(this).attr('data-number-preg');
        var siguientepreg = $(this).children('select').val();
        var $logica = $(this).children(".logicaPreg");
        var cajadetexto =  $logica.find(".txtlogica").val();
         var  param = {};
         param.pregunta=  idpregunta;
         param.salto = cajadetexto;
         parametros.push(param)  ;
       });
         var encuesta= $("#encuesta").val();
     console.log(encuesta);

         $.ajax({
        type: 'POST',
        url: '/survey/configurar/flujoavanzado/' + encuesta,
        data:{ 'parameter':JSON.stringify(parametros),
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function ajaxSuccess(data, textStatus, jqXHR) {

           },
           dataType: 'JSON'

    });


        return false;
});

$('.si').on("click", function(e)
{
    var $textarea= $(this).parents('.logicaPreg').find('.txtlogica');
    var valor = $.trim($textarea.val());
    $textarea.val(valor + "SI('','PASE()');");
});

    $('.pase').on("click", function(e)
{
    var $textarea= $(this).parents('.logicaPreg').find('.txtlogica');
    var valor = $.trim($textarea.val());
    $textarea.val(valor + "PASE();");
});

$('.sino').on("click", function(e)
{

    var $textarea= $(this).parents('.logicaPreg').find('.txtlogica');
    var valor = $.trim($textarea.val());
    console.log(valor);
    $textarea.val(valor + "SI('','PASE()','PASE()');");


});

$('.cargar').on("click", function(e)
{
    var $textarea= $(this).parents('.logicaPreg').find('.txtlogica');
    var valor = $.trim($textarea.val());
    $textarea.val(valor + "VARIABLES{}");


});


$('.ocultar').on("click", function(e)
{
    var $textarea= $(this).parents('.logicaPreg').find('.txtlogica');
    var valor = $.trim($textarea.val());
    $textarea.val(valor + "OCULTAR('','');");



});

$('.sisi').on("click", function(e)
{
    var $textarea= $(this).parents('.logicaPreg').find('.txtlogica');
    var valor = $.trim($textarea.val());
    $textarea.val(valor + "SI(Y('',''),'');");
});


$('.mensaje').on("click", function(e)
{
    var $textarea= $(this).parents('.logicaPreg').find('.txtlogica');
    var valor = $.trim($textarea.val());
    $textarea.val(valor + " MSJ='';");


});


$('.alerta').on("click", function(e)
{
    var $textarea= $(this).parents('.logicaPreg').find('.txtlogica');
    var valor = $.trim($textarea.val());
    $textarea.val(valor + "INICIO{ALERTA('INGRESA EL MENSAJE AQUI!!!');};");

});


$('.unica').on("click", function(e)
{
    var $textarea= $(this).parents('.logicaPreg').find('.txtlogica');
    var valor = $.trim($textarea.val());
    $textarea.val(valor + "SI(Y('UNICA(pregunta,valor)==1'),'PASE()','ALERTA(mensaje si es error)');");

});

$('.siselect').on("click", function(e)
{
    var $textarea= $(this).parents('.logicaPreg').find('.txtlogica');
    var valor = $.trim($textarea.val());
    $textarea.val(valor + "SI('SELECCIONI(pregunta!!,valor!!)!=1','PASE()');");

});


    $("#enviar").on('click', function(e){
    //e.preventDefault();

    $(".logicaEncabezado").each(function(index){

        var numeropregunta = $(this).attr('data-idpreg');
        var idpregunta = $(this).attr('data-number-preg');
        var siguientepreg = $(this).children('select').val();
        var $logica = $(this).children(".logicaPreg");
        var cajadetexto =  $logica.find(".txtlogica").val();

      console.log(condiciones(numeropregunta, idpregunta, cajadetexto));

      /*      $.ajax({
        type: 'POST',
        url: '/survey/configurar/flujo/' + encuesta,
        data:{ 'parameter':JSON.stringify(parametros),
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function ajaxSuccess(data, textStatus, jqXHR) {

           },
           dataType: 'JSON'

    });*/

    });


    });




});