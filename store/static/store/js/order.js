(function($){

    var OrderReport = {
        init_dom: function () {
            this.dom = {
                sidebar: $('#obj-sidebar'),
                itemlist: $('#obj-item-list tbody'),
                errornote: $('#obj-error-note p')
            };
            $('#obj-sidebar ul li:first').addClass('obj-select');
            this.dom.errornote.hide();
            // 标记库存不足
            this.alertStore();
            this.showErrorNote('标红色的商品为库存量不足(默认小于 5 为库存不足)');
        },
        showLoading: function () {

        },
        hideLoading: function() {

        },
        showErrorNote: function (text) {
            this.dom.errornote.text(text);
            this.dom.errornote.show();
            var that = this;
            setTimeout(function() {
                that.dom.errornote.fadeOut(400)
            }, 5000);
        },
        alertStore: function () {
            this.dom.itemlist.children().each(
                function(){
                    var store = $(this).children()[3];
                    var num = parseInt($(store).text());
                    if(num < 5){
                        $(this).addClass('obj-red-tr');
                    }
                }

                );
        },

        append_list: function (data) {
             var tbody = '';
                    data.forEach(function (obj) {
                        if(parseInt(obj.remain) < 5) {
                            tbody += '<tr class="obj-red-tr">';
                        }else{
                            tbody += '<tr>';
                        }
                        tbody += '<td>' + obj.name + '</td>';
                        tbody += '<td><input value="' + obj.price + '" type="number"></td>';
                        tbody += '<td>' + obj.unit + '</td>';
                        tbody += '<td>' + obj.remain + '</td>';
                        tbody += '<td><input value="1" type="number">' +
                            '<a href="javascript:void(0);" class="addlink" name="'+obj.id+'">添加到清单</a></td></tr>';

                    });
                    this.dom.itemlist.html(tbody);
        },
        remove_select: function () {
            this.dom.sidebar.find('.obj-select').each(function () {
                $(this).removeClass('obj-select');
            })
        },

        show_item_list: function (li_dom) {
            var url = li_dom.attr('value');
            li_dom.addClass('obj-select').siblings().removeClass("obj-select");
            var that = this;
            $.ajax({
                type: "get",
                url: url,
                beforeSend: function (XMLHttpRequest) {
                    that.showLoading();
                },
                success: function (data, textStatus) {
                   that.append_list(data)
                },
                complete: function (XMLHttpRequest, textStatus) {
                    that.hideLoading();
                },
                error: function () {
                    that.showErrorNote('程序出现错误，请检查网络， 或者请联系开发人员！！！')
                }
            });
        },
        init_handler: function () {
            var that = this;
            this.dom.sidebar.delegate("li","click",function(){
                that.show_item_list($(this));
            });
        },
        init: function (params) {
            this.params = params || {};
            this.init_dom();
            this.init_handler();
            this.ItemList.init();

        }

    };

	this.OrderReport = OrderReport;
})(django.jQuery);