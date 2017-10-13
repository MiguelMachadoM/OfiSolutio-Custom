$(document).ready(function () {
    $('.oe_website_sale').each(function () {
        var oe_website_sale = this;
        var ajust_quantity_min = function(quantity, min) {
            if (quantity == 0)
                return quantity;

            if (min != 0) {
                if (quantity < min) {
                    quantity = min;
                }
                if (quantity % min != 0) {
                    quantity = quantity - (quantity % min);
                }
            }
            return quantity;
        }

        $(oe_website_sale).off('click', 'a.js_add_cart_json');
        $(oe_website_sale).on('click', 'a.js_add_cart_json', function (ev) {
            ev.preventDefault();
            if ($(this).hasClass('disabled'))
                return;

            var $link = $(ev.currentTarget);
            var $input = $link.parent().parent().find("input");
            var min = parseFloat($input.data("min") || 0);
            var max = parseFloat($input.data("max") || Infinity);
            if (min != 0) {
                var quantity = ($link.has(".fa-minus").length ? -min : min) + parseFloat($input.val(),10);
            } else {
                var quantity = ($link.has(".fa-minus").length ? -1 : 1) + parseFloat($input.val(),10);
            }

            if (quantity == 0)
                $input.val(0);
            else
                $input.val(quantity > min ? (quantity < max ? quantity : max) : min);

            $('input[name="'+$input.attr("name")+'"]').val(quantity > min ? (quantity < max ? quantity : max) : min);
            $input.change();
            return false;
        });

        $(oe_website_sale).off("change", ".js_add_cart_variants input.js_quantity");
        $(oe_website_sale).on("change", ".js_add_cart_variants input.js_quantity", function () {
            var $input = $(this);
            var value = parseInt($input.val(), 10);
            var min = parseFloat($input.data("min") || 0);

            value = ajust_quantity_min(value, min);
            $input.val(value);
        });

        $(oe_website_sale).off("change", ".oe_cart input.js_quantity");
        $(oe_website_sale).on("change", ".oe_cart input.js_quantity", function () {
            var $input = $(this);
            var value = parseInt($input.val(), 10);
            var line_id = parseInt($input.data('line-id'),10);
            var min = parseFloat($input.data("min") || 0);

            value = ajust_quantity_min(value, min);
            $input.val(value);

            if (isNaN(value))
                value = 0;

            $("a.js_add_cart_json").addClass("disabled");

            openerp.jsonRpc("/shop/cart/update_json", 'call', {
                'line_id': line_id,
                'product_id': parseInt($input.data('product-id'),10),
                'set_qty': value})
                .then(function (data) {
                    if (!data.quantity) {
                        location.reload();
                        return;
                    }
                    $("a.js_add_cart_json").removeClass("disabled");
                    var $q = $(".my_cart_quantity");
                    $q.parent().parent().removeClass("hidden", !data.quantity);
                    $q.html(data.cart_quantity).hide().fadeIn(100);

                    $input.val(data.quantity);
                    $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
                    $("#cart_total").replaceWith(data['website_sale.total']);
                });
        });
    });
});
