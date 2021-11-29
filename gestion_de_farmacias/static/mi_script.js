// esto corrije el tipo del campo imput 'id_vencimiento' en el formulario para crear recetas
// por alguna razon no quiere cambiar el type a date
window.onload = function() {


    //document.getElementById('id_vencimiento').type = 'date';
    //document.getElementById('id_fecha_de_nacimiento').type = 'date';
    //document.getElementById('id_telefono').type = 'tel';
    //document.getElementById('id_fecha_de_nacimiento').type = 'date';
    let input_vencimiento = document.getElementById('id_vencimiento');
    if (input_vencimiento) {
        input_vencimiento.type = 'date';
    }

    let input_fecha_de_nacimiento = document.getElementById('id_fecha_de_nacimiento');
    if (input_fecha_de_nacimiento) {
        input_fecha_de_nacimiento.type = 'date';
    }

    let input_telefono = document.getElementById('id_telefono');
    if (input_telefono) {
        input_telefono.type = 'tel';
        //input_telefono.setAttribute("max", 999999999);
        //input_telefono.setAttribute("min",99999999);
    }


}



//=========================================
//BUSCADOR DE MEDICAMENTOS =================
//=========================================
/*function buscar_medicamento() {
    //alert("funca el onkeyup")
    // Declare variables
    var input, filter, table, tr, td, i, txtValue_nombre_comercial, txtValue_laboratorio, txtValue_principio_activo;
    input = document.getElementById("medicamento_buscado");
    filter = input.value.toUpperCase();
    table = document.getElementById("tabla_de_medicamentos");
    tr = table.getElementsByTagName("tr");

    //el bucle for evalua a cada una de las filas de la tabla
    for (i = 0; i < tr.length; i++) {
        //captura el elemento de la columna nombre_comercial
        td_nombre_comercial = tr[i].getElementsByTagName("td")[0];
        //captura el elemento de la columna laboratorio
        td_laboratorio = tr[i].getElementsByTagName("td")[2];
        //captura el elemento de la columna principio_activo
        td_principio_activo = tr[i].getElementsByTagName("td")[3];

        if (td_nombre_comercial || td_laboratorio || td_principio_activo) {
            txtValue_nombre_comercial = td_nombre_comercial.textContent || td_nombre_comercial.innerText;
            txtValue_laboratorio = td_laboratorio.textContent || td_laboratorio.innerText;
            txtValue_principio_activo = td_principio_activo.textContent || td_principio_activo.innerText;
            if (txtValue_nombre_comercial.toUpperCase().indexOf(filter) > -1 || txtValue_laboratorio.toUpperCase().indexOf(filter) > -1 || txtValue_principio_activo.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }

    }
}



//=========================================
//BUSCADOR DE USUARIOS =================
//=========================================
function buscar_usuario() {
    // Declare variables
    var input, filter, table, tr, td, i, txtValue_cedula_de_identidad, txtValue_usuario, txtValue_nombre, txtValue_apellido;
    input = document.getElementById("usuario_buscado");
    filter = input.value.toUpperCase();
    table = document.getElementById("tabla_de_usuarios");
    tr = table.getElementsByTagName("tr");

    //el bucle for evalua a cada una de las filas de la tabla
    for (i = 0; i < tr.length; i++) {
        //captura el elemento de la columna cedula_de_identidad
        td_cedula_de_identidad = tr[i].getElementsByTagName("td")[0];
        //captura el elemento de la columna usuario
        td_usuario = tr[i].getElementsByTagName("td")[2];
        //captura el elemento de la columna nombre
        td_nombre = tr[i].getElementsByTagName("td")[3];
        //captura el elemento de la columna apellido
        td_apellido = tr[i].getElementsByTagName("td")[4];

        if (td_cedula_de_identidad || td_usuario || td_nombre || td_apellido) {
            txtValue_cedula_de_identidad = td_cedula_de_identidad.textContent || td_cedula_de_identidad.innerText;
            txtValue_usuario = td_usuario.textContent || td_usuario.innerText;
            txtValue_nombre = td_nombre.textContent || td_nombre.innerText;
            txtValue_apellido = td_apellido.textContent || td_apellido.innerText;
            if (txtValue_cedula_de_identidad.toUpperCase().indexOf(filter) > -1 || txtValue_usuario.toUpperCase().indexOf(filter) > -1 || txtValue_nombre.toUpperCase().indexOf(filter) > -1 || txtValue_apellido.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }

    }
}*/

$(document).ready(function() {
    $('#tabla_de_medicamentos').DataTable({
        // order [1,'asc'] significa que la columna con index 1 se va a ordenar de forma ascendente
        order: [
            [1, 'asc']
        ]
    });
    $('#tabla_de_usuarios').DataTable({
        order: [
            [2, 'asc']
        ]
    });
    $('#tabla_de_farmacias').DataTable();
    $('#tabla_de_stock').DataTable({
        order: [
            [0, 'desc']
        ]
    });
    $('#tabla_de_stock_acumulado').DataTable({
        order: [
            [0, 'asc']
        ]
    });
    $('#tabla_de_stock_nacional').DataTable({
        order: [
            [2, 'asc']
        ]
    });
    //$('#tabla_de_stock_acumulado').DataTable();
    $('#tabla_de_recetas').DataTable({
        order: [
            [0, 'desc']
        ]
    });
    $('#tabla_de_disponibilidad_en_farmacias').DataTable({
        order: [
            [0, 'desc']
        ]
    });
    //$('#tabla_de_recetas').DataTable();
});