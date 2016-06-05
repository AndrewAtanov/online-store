/**
 * Created by andrew on 05.06.16.
 */

$(document).ready(function () {
    $.ajax({
        url: "/cart-total-price/",
        type: "GET",
        data: {"product_id": $(this).attr('id')},
        success: function (data) {
            $('#cart').attr('data-content', data);
        }
    });

    $('[data-toggle="popover"]').popover({
        placement: 'bottom',
        content: function () {
            $.ajax({
                url: "/cart-total-price/",
                type: "GET",
                data: {"product_id": $(this).attr('id')},
                success: function (data) {
                    $('#cart').attr('data-content', data);
                }
            });
            return $("#cart").attr('data-content');
        }
    });
});