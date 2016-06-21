/**
 * Created by andrew on 30.03.16.
 */

$(document).ready(function () {
    $("button.add").click(function () {
        var cur_btn = $(this);
        $.ajax({
            url: "/add-to-cart/",
            type: "GET",
            data: {"product_id": $(this).attr('id')},
            success: function (data) {
                cur_btn.wrap("<span class='label label-success add-to-cart-resp'></span>");
                cur_btn.replaceWith(data);
            }
        });
    });
});

