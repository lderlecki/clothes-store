$('#delivery-address input[type=radio], #invoice-address input[type=radio]').on('click', function () {
    $('.address-brick').removeClass('selected');
    $('.address-brick:has(input[type=radio]:checked)').addClass('selected');
    let deliveryRadio = document.querySelector('#delivery-address input[type=radio]:checked')
    let invoiceRadio = document.querySelector('#invoice-address input[type=radio]:checked')

    if (deliveryRadio != null && invoiceRadio != null) {
        document.getElementById('checkout-proceed').disabled = false;
    } else {
        document.getElementById('checkout-proceed').disabled = true;
    }
})

$('document').ready(function (){
    if (validateAddresses()){
        document.getElementById('checkout-proceed').disabled = false;
    }
})

function validateAddresses(){
    let deliveryRadio = document.querySelector('#delivery-address input[type=radio]:checked')
    let invoiceRadio = document.querySelector('#invoice-address input[type=radio]:checked')
    if (deliveryRadio != null && invoiceRadio != null) {
        document.getElementById('checkout-proceed').disabled = true;
        return true
    } else {
        return false
    }
}

function validateCheckoutForm() {
    if (validateAddresses()) {
        return true
    } else {
        alert('Select both shipping and invoice addresses.')
        document.getElementById('checkout-proceed').disabled = true;
        return false
    }
}
