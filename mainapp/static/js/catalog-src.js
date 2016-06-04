/**
 * Created by andrew on 27.02.16.
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


    $("span.delete").click(function(){
        var cur_el = $(this);
        $.ajax({
            url: "/remove-from-cart/",
            type: "GET",
            data: {"item": $(this).attr('id')},
            success: function (data) {
                cur_el.parent().parent().remove();
                console.log(data)
            }
        });
    });


    var fltr = $('#filter');
    fltr.popover({ html : true});
    fltr.attr('data-content', '<form class="form-horizontal" role="form"> <div class="row"> <div class="col-md-4"> <label for="inputType" class="control-label">Цена</label> </div> </div> <div class="form-group"> <div class="col-md-12"> <div class="form-group row"> <label for="inputKey" class="col-md-1 control-label">от</label> <div class="col-md-4"> <input type="text" class="form-control" id="usr"> </div> <label for="inputValue" class="col-md-1 control-label">до</label> <div class="col-md-4"> <input type="text" class="form-control" id="usr"> </div> </div> </div> </div> </form>');
    fltr.popover();
});