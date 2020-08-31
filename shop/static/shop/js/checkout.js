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
    if (document.getElementById('invoice-checkbox').checked){
        document.getElementById('invoice_form').style.display="none"
    }
})

function validateAddresses(){
    let deliveryRadio = document.querySelector('#delivery-address input[type=radio]:checked')
    let invoiceRadio = document.querySelector('#invoice-address input[type=radio]:checked')
    if (deliveryRadio != null && invoiceRadio != null) {
        document.getElementById('checkout-proceed').style.disabled = true;
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

function setRequired(elems, param){
    for (let i = 0; i < elems.length; i++){
            elems[i].required = param;
        }
}

function setBilling(ele) {
    let form = document.getElementById('invoice_form')
    let fields = form.getElementsByTagName('input')

    if (ele.checked){
        form.style.display="none"
        setRequired(fields, false)
    }else{
        document.getElementById('invoice_form').style.display="block"
        setRequired(fields, true)
    }
}
