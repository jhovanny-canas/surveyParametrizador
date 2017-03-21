
//function siguiente(pregunta,idpregunta, preguntasiguiente)
//{
//   return  "{'"+ pregunta + "':" + idpregunta + ",'salto':'PASE(" + preguntasiguiente + ");'}";
//}
//
//function si(pregunta,idpregunta, operador, preguntasiguiente, valor)
//{
//   return "{'"+ pregunta + "':" + idpregunta + ",'salto': 'SI('P"+ idpregunta + operador + valor +"','PASE(" + preguntasiguiente + ")');'}";
//}
//
//function sino(pregunta, idpregunta,operador, preguntaverdader,preguntafalso, valor)
//{
//   return "{'"+ pregunta + "':" + idpregunta + ", 'salto':'SI('P" + idpregunta + operador + valor + "','PASE(" + preguntaverdader + ")','PASE(" + preguntafalso  +" )');'}";
//}


function siguiente(pregunta,idpregunta, preguntasiguiente)
{
    var pregJson ={};
    pregJson.numeropregunta = pregunta;
    pregJson.pregunta=idpregunta;
    pregJson.salto = 'PASE(' + preguntasiguiente + ');';
   return  pregJson;
}

function si(pregunta,idpregunta, operador, preguntasiguiente, valor)
{
    var pregJson ={};
    pregJson.numeropregunta = pregunta;
    pregJson.pregunta=idpregunta;
    pregJson.salto = "SI(' P" + idpregunta + operador + valor +"','PASE(" + preguntasiguiente + ")');";

   return pregJson;
}

function sino(pregunta, idpregunta,operador, preguntaverdader,preguntafalso, valor)
{

    var pregJson ={};
    pregJson.numeropregunta = pregunta;
    pregJson.pregunta=idpregunta;
    pregJson.salto = "SI('P" + idpregunta + operador + valor + "','PASE(" + preguntaverdader + ")','PASE(" + preguntafalso  +" )');";
   return  pregJson;
}
$(function() {


    $("#enviar_flow").on('click', function(){
    var parametros =[];

    $(".logicaEncabezado").each(function(index){
        var numeropregunta = $(this).attr('data-idpreg');
        var idpregunta = $(this).attr('data-number-preg');
        var siguientepreg = $(this).children('select').val();
        var $logica = $(this).children(".logicaPreg");
        var $hijologica =$logica.find(".configuralogica");
        var $hijologicafondo =$hijologica.find(".panellogica");
        var  operador = $hijologicafondo.find(".base").val();
        var  preguntaverdadero = $hijologicafondo.find(".preginicio").val();
        var  preguntafalso = $hijologicafondo.find(".terminus").val();
        var  texto = $hijologicafondo.find(".valcondicion").val();
        if($hijologica.length==0)
        {
           parametros.push(siguiente(numeropregunta, idpregunta, siguientepreg));

        }

        if(preguntafalso===undefined && $hijologica.length>0 && preguntaverdadero===undefined)
        {
          parametros.push(siguiente(numeropregunta,idpregunta,  siguientepreg));
        }

         if(preguntafalso===undefined && $hijologica.length>0 && preguntaverdadero!==undefined)
        {
          parametros.push(si(numeropregunta,idpregunta,  operador, preguntaverdadero, texto));
        }

        if(preguntafalso!==undefined && $hijologica.length>0)
        {
           parametros.push(sino(numeropregunta,idpregunta,  operador, preguntaverdadero, preguntafalso, texto));
        }

    });

        $('#flow_form').on('submit', function(e) { //use on if jQuery 1.7+
        e.preventDefault();  //prevent form from submitting
        var data = $("#login_form :input").serializeArray();
        //use the console for debugging, F12 in Chrome, not alerts
    });
        console.log(parametros);
        var encuesta= $("#encuesta").val();

        $.ajax({
        type: 'POST',
        url: '/survey/configurar/flujo/' + encuesta,
        data:{ 'parameter':JSON.stringify(parametros),
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function ajaxSuccess(data, textStatus, jqXHR) {

           },
           dataType: 'JSON'

    });



    });

   $('.logica').on('click', function(){
       var $pregu = $(this).parents('.logicaEncabezado');
       var idpregunta=$(this).parent().attr('data-number-preg');
       var numeroPregunta=$(this).parent().attr('data-idpreg');
        var $select = $pregu.find('select');
       var $selecciones = $select.clone();
       var $preguntaNumero= $pregu.find('p');
       var valores = $select.text();
       $select.hide();

       //oculta el boton de logica y agrega el panel para el ingreso de laspreguntas
       $(this).parent().append('<div class="configuralogica">' +
           '<input type="button" class="si" value="SI"> <input type="button" class="sino" value="Si No">  <br>' +
           '<div class="panellogica"   name="panellogica" >' +
           '</div> <br>' +
           '<input type="button" class="cancelar" value="cancelar"> <input type="button" value="guardar">' +
           '</div>');

           $('.si').on('click', function()
       {
           $(this).hide();

           var $contenedor = $(this).parent();
           var otroboton = $contenedor.find(".sino");
           otroboton.prop('disabled',true);
           var $divlogica = $contenedor.children('.panellogica');
            var operadores='<select class="base">' +
                '<option name="==">==</option>' +
                '<option name="!=">!=</option>' +
                '<option name="<="><=</option>' +
                '<option name=">=">>=</option>' +
                '</select>'+
                 '<input type="text" class="valcondicion" required> <strong> Seguir a pregunta # </strong>'
                ;
           $divlogica.append($divlogica.val() + '<div><strong> Si' + $preguntaNumero.text() + '</strong>' +
               ' ' + operadores + '<select class="preginicio">' + $selecciones.html() + '   </select>' +
                   '<a href="#" class="eliminarlogica"> Eliminar </a></div>'

           );
           $('.eliminarlogica').on('click', function(e)

           {
                    e.preventDefault();
                   $(this).parent().remove();
                    $contenedor.children('.sino').prop("disabled",false);
                    $contenedor.children('.si').show();
               });


       });


        $('.sino').on('click', function()
       {

           $(this).hide();
           var $contenedor = $(this).parent();
           var otroboton = $contenedor.find(".si");
           otroboton.prop('disabled',true);
           var $divlogica = $contenedor.children('.panellogica');
            var operadores='<select class="base">' +
                '<option name="==">==</option>' +
                '<option name="!=">!=</option>' +
                '<option name="<="><=</option>' +
                '<option name=">=">>=</option>' +
                '</select>'+
                 '<input type="text" class="valcondicion" required> <strong> Seguir a pregunta # </strong>'
                ;
           $divlogica.append($divlogica.val() + '<div><strong> Si' + $preguntaNumero.text() + '</strong>' +
               ' ' + operadores + '<select class="preginicio">' + $selecciones.html() + '   </select> <strong> De otra forma ir a la pregunta </strong>' +
                   '<select class="terminus"> ' + $selecciones.html() + '</select>' +
                   '<a href="#" class="eliminarlogica"> Eliminar </a></div>'

           );
           $('.eliminarlogica').on('click', function(e)

           {
                    e.preventDefault();
                   $(this).parent().remove();
                    $contenedor.children('.si').prop("disabled",false);
                    $contenedor.children('.sino').show();

               });

            $('.preginicio').change(function()
            {

                var id = $(this).val();
                alert(id);
                var $opcionesdos=$(this).data('options', $(this).find('option').clone());

                //var options =  $opcionesdos.data('options').filter('[value= ' + id + ']');
                var options =  $opcionesdos.data('options').filter( function()
                {
                    return  $(this).attr("value") >= id;

                });

                var $padre =$(this).parent();
                var $selecterminus = $padre.find('.terminus');

                $selecterminus.html(options);




            });




       });

          $('#siguiente').on('click', function()
       {

       });



          $(this).hide();

        $('.cancelar').on('click', function(){
         var $btnlogica =   $(this).parents('.logicaPreg');
         var $padre = $(this).parents('.logicaEncabezado');
          var $selectpri = $padre.find('select');
            $selectpri.show();
            $(this).parent().remove();
        $btnlogica.children('.logica').show();



    });

   });







var tipopregunta =$("#typequestion").val();

    if (tipopregunta>2)
    {
     $('#div-values').hide();
    $("#minvalue").val(0);
    $("#maxvalue").val(5);

    }


$('.addopcion').on('click', function(e){
var dato= $('#txtnewopcion').val();
var pregunta = $('#idquestion').val();
    $.ajax({
        type: 'POST',
        url: '/survey/configurar/addopcion/' + pregunta,
        data:{'txtnewopcion':dato,
        'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
        },
        success: function ajaxSuccess(data, textStatus, jqXHR) {

            $('#txtnewopcion').val('');
            var datos= $.parseJSON(data);
               var output='<ul>';
                for(var i in datos)
            {
                output+='<li>' + datos[i].descripcion_valor + '--' +  datos[i].valor_id + ' <input type="button" id=' + datos[i].id + ' class="eliminarop" value="eliminar"/></li>';
            }

                output+="</ul>";
            $('#div-opciones').html(output);

               //$(e.target).parent().html(data);
           },
           dataType: 'html'

    });

});


//esta opcion se ajusto por que el boton se encuentra dentro del div, entonces no funciona si no es con esta sintaxis or ser crea dinamiecamente
$("#div-opciones").on('click','.eliminarop' , function(e) {

    var respuesta = $(this).attr('id');
    $.ajax({
        url: '/survey/configurar/retiraropcion/' + respuesta,
        type: 'POST',

        data: {'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val() },
                        success: function ajaxSuccess(data, textStatus, jqXHR) {

                            var datos = $.parseJSON(data);
                            var output = '<ul>';
                            for (var i in datos)

                                    {
                                        output += '<li>' + datos[i].descripcion_valor + '--' + datos[i].valor_id + ' <input type="button" id=' + datos[i].id + ' class="eliminarop" value="eliminar"/></li>';
                                    }

                            output += "</ul>";
                            $('#div-opciones').html(output);
                            //$(e.target).parent().html(data);
                        },
        dataType: 'html'
    });


});


});



//
//$(window).on('keypress keydown keyup', function(e){
//
//    if(e.keyCode==116)
//    {
//        e.preventDefault();
//        return false;
//