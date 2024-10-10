$(document).on("click", "#add-button", function(e) {
    e.preventDefault();
    const cartAddUrl = $(this).data('url');
    const productId = $(this).val(); // Asegúrate de que este selector sea correcto
    const productQuantity = $("#cantidad option:selected").val(); // Usa .val() si necesitas el valor
    alert(productId);
    alert(productQuantity);

    $.ajax({
        url: cartAddUrl,
        type: 'POST',
        data: {
            product_id: productId,
            product_quantity: productQuantity,
            csrfmiddlewaretoken: "{{ csrf_token }}", // Asegúrate de que esta sintaxis funcione en tu contexto
            action: "post"
        },
        success: function(json) {
            console.log(json);
            // Aquí podrías añadir lógica para actualizar la interfaz de usuario
        },
        error: function(xhr, errmsg, err) {
            console.log(`Error en la solicitud: ${xhr.status} - ${xhr.statusText}`);
        }
    });
});

