$('.update-cart').on('click', function (){
    let productId = this.dataset.product
    let action = this.dataset.action
    if (user === 'AnonymousUser'){
        addCookieItem(productId, action);
        $.ajax({
            url: 'add_to_cart/',
            type: 'POST',
            data: {
                'productId': productId,
                'csrfmiddlewaretoken': csrftoken,
            }, success: function(data){

            }
        })
    }else{
        $.ajax({
            url: 'add_to_cart/',
            type: 'POST',
            data: {
                'productId': productId,
                'action': action,
                'csrfmiddlewaretoken': csrftoken,
            },success: function (data){
                if (data['product_qty'] > 0){
                    $('#product-quantity-' + productId).text(data['product_qty']);
                    $('#item-total-' + productId).text(data['product_total']);
                }else{
                    console.log('remove item')
                    document.getElementById('item-data-' + productId.toString()).remove()
                }
                $.ajax({
                    url: 'get_cart_data/',
                    type: 'GET',
                    success: function(data){
                        $('#cart-total').text(data['cart_items']);
                        $('#cart-items-number').text(data['cart_items']);
                        $('#cart-total-price').text(data['cart_total']);
                    }
                })
            }
        })
    }
})
$('.add-to-cart').on('click', function (){
    let productId = this.dataset.product
    let action = this.dataset.action
    if (user === 'AnonymousUser'){
        addCookieItem(productId, action);
    }else{
        $.ajax({
        url: '/cart/add_to_cart/',
        type: 'POST',
        data: {
            'productId': productId,
            'action': action,
            'csrfmiddlewaretoken': csrftoken,
        },success: function (data){
            if (data['product_qty'] > 0){
                $('#cart-total').text(data['cart_items']);
            }
        }
    })
    }


})

function addCookieItem(productId, action){
    console.log('User not logged in');
    if (action === 'add'){
        if (cart[productId] === undefined){
            cart[productId] = {'quantity': 1}
        }else{
            cart[productId]['quantity'] += 1;
        }
        $('#product-quantity-' + productId).text(cart[productId]['quantity']);
    }
    if (action === 'remove'){
        cart[productId]['quantity'] -= 1;
        if (cart[productId]['quantity'] <= 0){
            console.log('Remove item')
            delete cart[productId]
            removeItem(productId);
        }else{
            $('#product-quantity-' + productId).text(cart[productId]['quantity']);
        }
    }
    if (action === 'delete'){
        delete cart[productId]
        removeItem(productId);
    }


    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
}

function removeItem(productId){
    document.getElementById('item-data-' + productId.toString()).remove()
}
