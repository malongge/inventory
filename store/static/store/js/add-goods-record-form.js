/**
 * Created by long on 2016/12/17.
 */

(function($){

    var show_input_price = {
        init_dom: function () {
            this.dom = {
                goods: $('#id_goods_1'),
                price: $('#id_new_price')
            };
        },
        init_handler: function () {
            var that = this;
            this.dom.price.attr('placeholder', '点击输入框获取原价');
            this.dom.price.click(function () {
                that.show_price();
            });

        },
        show_price: function () {
            var goods_id = this.dom.goods.attr('value');
            if(!goods_id)
                return;
            var that = this;
            $.get('goods/'+goods_id, function (data) {
                that.dom.price.val(JSON.parse(data).fields.average_price);
            })
        },
        init: function () {
            this.init_dom();
            this.init_handler()


        }

    };

     $(document).ready(function() {
        show_input_price.init();
    });



})(django.jQuery);