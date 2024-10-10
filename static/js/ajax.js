
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
