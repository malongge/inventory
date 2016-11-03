(function($){

    var StyleChange = {
        init_dom: function () {
            this.dom = {
                remain: $('.field-remain'),
                averagePrice: $('.field-average_price'),
                lastPrice: $('.field-last_price')
            };
        },
        change_color: function (dom, className, bigOne) {
            dom.each(function(){
                 var val = parseInt($(this).text());
                if(val < bigOne)
                $(this).addClass(className);
            });
        },
        init_handler: function () {
            this.change_color(this.dom.remain,'remain-low',5);
            this.change_color(this.dom.averagePrice, 'average-price-warn', 0.01);
            this.change_color(this.dom.lastPrice, 'last-price-warn', 0.01);
        },
        init: function (params) {
            this.params = params || {};
            this.init_dom();
            this.init_handler()


        }

    };

     $(document).ready(function() {
        StyleChange.init();
    });



})(django.jQuery);