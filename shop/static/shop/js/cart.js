$('.update-cart').on('click', function (){
    let productId = this.dataset.product
    let action = this.dataset.action
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

})
$('.add-to-cart').on('click', function (){
    let productId = this.dataset.product
    let action = this.dataset.action
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
})

