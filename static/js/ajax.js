
$(document).on("click", "#add-button", function(e) {
    e.preventDefault();
    const cartAddUrl = $(this).data('url');
    const csrf = $(this).data('csrf');
    const productId = $(this).val(); 
    const productQuantity = $("#cantidad option:selected").val();

    $.ajax({
        url: cartAddUrl,
        type: 'POST',
        data: {
            product_id: productId,
            product_quantity: productQuantity,
            csrfmiddlewaretoken: csrf,
            action: "post"
        },
        success: function(json) {
          //  console.log(json);
            document.getElementById("cart-qty").textContent = json.qty;
        },
        error: function(xhr, errmsg, err) {
            console.log(`Error en la solicitud: ${xhr.status} - ${xhr.statusText}`);
        }
    });
});

$(document).on("click", ".delete-button", function(e) {
    e.preventDefault();
    const cartDeleteUrl = $(this).data('url');
    const csrf = $(this).data('csrf');
    const productId = $(this).data('index'); 

    $.ajax({
        url: cartDeleteUrl,
        type: 'POST',
        data: {
            product_id: productId,
            csrfmiddlewaretoken: csrf,
            action: "post"
        },
        success: function(json) {
            // console.log(json);
            location.reload(true);
            document.getElementById("cart-qty").textContent = json.qty;
            document.getElementById("total").textContent = json.total;

        },
        error: function(xhr, errmsg, err) {
            console.log(`Error en la solicitud: ${xhr.status} - ${xhr.statusText}`);
        }
    });
});

$(document).on("click", ".update-button", function(e) {
    e.preventDefault();
    const cartUpdateUrl = $(this).data('url');
    const csrf = $(this).data('csrf');
    const productId = $(this).data('index'); 
    const productQuantity = $("#select" + productId +" option:selected").text();

    $.ajax({
        url: cartUpdateUrl,
        type: 'POST',
        data: {
            product_id: productId,
            product_quantity: productQuantity,
            csrfmiddlewaretoken: csrf,
            action: "post"
        },
        success: function(json) {
            // console.log(json);
            location.reload(true);
            document.getElementById("cart-qty").textContent = json.qty;
            document.getElementById("total").textContent = json.total;

        },
        error: function(xhr, errmsg, err) {
            console.log(`Error en la solicitud: ${xhr.status} - ${xhr.statusText}`);
        }
    });
});



document.addEventListener('DOMContentLoaded', function() {
    $(function () {
        $('[data-toggle="tooltip"]').tooltip();
    });
    function timer(){
        var message_timeout = document.getElementById("message-timer");
        if (message_timeout){
            setTimeout(function()
            {
                message_timeout.style.display = "none";
            }, 2500);
        }
    }
    timer();  // Llama a la función una vez que el DOM está completamente cargado
});

$(document).on("click", ".save-btn", function(e) {
    e.preventDefault();
    const categoryUpdate = $(this).data('url');
    const csrf = $(this).data('csrf');
    const categoryId = $(this).val(); 
    const category_name = $("#name" + categoryId).val();  
    const category_slug = $("#slug" + categoryId).val();  
    //console.log(categoryUpdate);
    //console.log(csrf);
    //console.log(categoryId);
    //console.log(category_slug);
    //console.log(category_name);

    $.ajax({
        url: categoryUpdate,
        type: 'POST',
        data: {
            category_id: categoryId,
            category_name: category_name,
            category_slug: category_slug,
            csrfmiddlewaretoken: csrf,
            action: "post"
        },
        success: function(json) {
            console.log(json);
            location.reload(true);
        },
        error: function(xhr, errmsg, err) {
            console.log(`Error en la solicitud: ${xhr.status} - ${xhr.statusText}`);
        }
    });
});

$(document).on("click", ".add-btn", function(e) {
    e.preventDefault();
    const categoryAdd = $(this).data('url');
    const csrf = $(this).data('csrf'); 
    const category_name = $("#new-name").val();  
    const category_slug = $("#new-slug").val();  
    console.log(categoryAdd);
    console.log(csrf);
    console.log(category_slug);
    console.log(category_name);

    $.ajax({
        url: categoryAdd,
        type: 'POST',
        data: {
            category_name: category_name,
            category_slug: category_slug,
            csrfmiddlewaretoken: csrf,
            action: "post"
        },
        success: function(json) {
            console.log(json);
            location.reload(true);
        },
        error: function(xhr, errmsg, err) {
            console.log(`Error en la solicitud: ${xhr.status} - ${xhr.statusText}`);
        }
    });
});