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
    }


}