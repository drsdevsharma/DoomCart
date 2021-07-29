$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})



$('.plus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var element = this.parentNode.children[2]
    var icon = this.parentNode.children[1]
    var productDiscountPrice = this.parentNode.parentNode.children[3].children[1]

    $.ajax({
        type:'GET',
        url: '/product/plus_cart/',
        data : {id : id},
        success: function(data){
            if (data.quantity > 0) {
                icon.innerHTML = '<i class="fas fa-minus-square fa-lg"></i>'
            }
            element.innerText = data.quantity
            document.getElementById("amount").innerText = "Rs. " + data.amount + ".0"
            document.getElementById("totalAmount").innerText = "Rs. " + data.totalAmount + ".0"
            productDiscountPrice.innerHTML = '<span><strong>Rs. ' + data.productAmount + '.0' +'</strong></span>'

        }
    })
}) 



$('.minus-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var element = this.parentNode.children[2]
    var icon = this.parentNode.children[1]
    var productDiscountPrice = this.parentNode.parentNode.children[3].children[1]

    $.ajax({
        type:'GET',
        url: '/product/minus_cart/',
        data : {id : id},
        success: function(data){
            if (data.quantity == 0) {
                element.parentNode.parentNode.parentNode.parentNode.remove()
            }else{
                element.innerText = data.quantity
            }
            if (data.quantity == 1) {
                icon.innerHTML = '<i class="fas fa-trash-alt fa-lg"></i>'
                
            }
            document.getElementById("amount").innerText = "Rs. " + data.amount + ".0"
            if (data.shippingCost > 0) {
                document.getElementById("shippingCost").innerText = "Rs. " + data.shippingCost + ".0"
                
            }
            document.getElementById("totalAmount").innerText = "Rs. " + data.totalAmount + ".0"
            document.getElementById("lblCartCount").innerText = data.cart_value
            productDiscountPrice.innerHTML = '<span><strong>Rs. ' + data.productAmount + '.0' +'</strong></span>'

        }
    })
}) 




$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var element = this
    $.ajax({
        type:'GET',
        url: '/product/remove_cart/',
        data : {id : id},
        success: function(data){
            document.getElementById("amount").innerText = "Rs. " + data.amount + ".0"
            document.getElementById("shippingCost").innerText = "Rs. " + data.shippingCost + ".0"
            document.getElementById("totalAmount").innerText = "Rs. " + data.totalAmount + ".0"
            element.parentNode.parentNode.parentNode.parentNode.remove()
            document.getElementById("lblCartCount").innerText = data.cart_value


        }
    })
}) 



