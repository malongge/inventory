(function($){
    var OrderReport = this.OrderReport || {}, that = OrderReport;

    $.fn.slideFadeToggle = function(easing, callback) {
        return this.animate({ opacity: 'toggle', height: 'toggle' }, 'fast', easing, callback);
    };

    OrderReport.ItemList = {
        StandardPost: function (url,args)
        {
        var form = $("<form method='post' style='display: none;'></form>");
        form.attr({"action":url});
            var input = $("<input type='hidden'>");
            input.attr({"name":'data_list'});
            input.val(args);
            form.append(input);
            var token = $("<input type='hidden'>");
            token.attr({'name': 'csrfmiddlewaretoken'});
            token.val(window.CSRF_TOKEN);
            form.append(token);
            form.appendTo(document.body);
            form.submit();
            document.body.removeChild(form[0]);
        },
        init_dom: function () {
            this.dom = {
                addLink: $('#obj-item-list .addlink'),
                itemList: $('#obj-item-list'),
                report: $('#obj-report-item'),
                reportList: $('#obj-report-list'),
                reportListTb: $('#obj-report-list tbody'),
                countMoney: $('#obj-count-money p'),
                printLink: $('#obj-print-link a'),
                searchButton: $('#obj-search'),
                searchText: $('#searchbar'),
                chooseUser: $('#choose_user'),
                userNameLabel: $('#user_name'),
                arrearsPrice: $('#arrears_price'),
                popPanel: $('.pop-panel'),
                shade: $('#shade-block'),
                userSearch: $('#user-search'),
                userSearchBody: $('.table-body'),
                userSearchText: $('#search-user-bar'),
                changeUserInfo: $('.choose-user-info'),
                exitLink: $('#exit-panel')
            };

            this.hideReportList();
        },
        hideReportList: function () {
            if(this.isEmpty(this.cache_items)){
                   this.dom.report.addClass('obj-no-display');
                }
        },
        showReportList: function() {
             if (this.dom.report.hasClass('obj-no-display')) {
                this.dom.report.removeClass('obj-no-display');
            }
        },
        init_handler: function () {
            var that = this;
            this.dom.itemList.delegate("a","click",function(){
                that.add_item($(this));
            });
            this.dom.reportList.delegate("a","click",function(){
                that.deleteItem($(this));
            });
            this.dom.userSearchBody.delegate("a", "click", function () {
                that.dom.userNameLabel.text($(this).attr('name'));
                that.dom.shade.css('display', 'none');
            });
            this.dom.exitLink.click(function () {
                that.dom.shade.css('display', 'none');
            });
            this.dom.printLink.click(function () {
                var data = {};
                data['user'] = that.dom.userNameLabel.text();
                if (!data['user']){
                    alert('请选择一个客户，然后再打印');
                    return
                }

                data['arrears'] = that.dom.arrearsPrice.val();
                try{
                if (data['arrears']){
                    parseFloat(data['arrears']).toPrecision(3)
                }
            }
            catch(Exception){
                return
            }
            // console.log(JSON.stringify(report_ids));
                var r=confirm("你确定要打印清单吗，确定的话会生成销售记录，并扣减商品数量！！！");
                if (r == true){

                    data['list_data'] = that.cache_items;
                    that.StandardPost($(this).attr('name'), JSON.stringify(data));
            }


        });
            this.dom.chooseUser.click(function () {
                var here = this;
                that.show_shade();
                // that.dom.chooseUser.slideFadeToggle(
                //     function () {
                //         here.addClass('obj-no-display');
                //     }
                // )
            });

            this.dom.userSearch.click(function () {
               that.search_user();
            });

            this.dom.searchButton.click(function () {
                that.search_item();
            })
        },
        append_users: function (data) {
            var pre = '<table class="table"><thead><tr><td>客户姓名</td><td>联系方式</td><td></td></tr></thead>' +
                    '<tbody>';
            var end = '</tbody></table>';

            var tbody = pre;
                    data.forEach(function (obj) {
                        tbody += '<tr><td>' + obj.name + '</td>';
                        tbody += '<td>' + obj.phone + '</td>';
                        tbody += '<td><a href="javascript:void(0);"  name="'+obj.name+'">选择</a></td></tr>';
                    });
            tbody += end;
                    this.dom.userSearchBody.html(tbody);

        },
        search_user: function () {
             var url = this.dom.userSearch.attr('name');
            var search_text = this.dom.userSearchText.val();
            if (!search_text) {
                alert('请输入查询内容');
                return
            }

            var that = this;
            $.ajax({
                type: "get",
                url: url,
                // headers: {
                //     csrfmiddlewaretoken: window.CSRF_TOKEN
                // },
                data: {
                    search_text: search_text
                },
                beforeSend: function (XMLHttpRequest) {
                },
                success: function (data, textStatus) {
                    if (data.length < 1){
                        that.dom.userSearchBody.html('<p>没有找到用户</p>');
                    return
                    }
                    that.append_users(data);
                },
                complete: function (XMLHttpRequest, textStatus) {
                },
                error: function () {
                    alert('程序出现错误，请检查网络， 或者请联系开发人员！！！');
                }
            });
        },
        show_panel: function () {
            this.dom.popPanel.css('display', 'block');
        },

        show_shade: function () {
            this.dom.shade.addClass('shade-block');
            this.dom.shade.css('width', document.documentElement.scrollWidth+"px");
            this.dom.shade.css('height', document.documentElement.scrollHeight+"px");
            this.dom.shade.css('display', 'block');
            this.show_panel();
        },

        search_item: function () {
            var url = this.dom.searchButton.attr('name');
            var search_text = this.dom.searchText.val();
            if (!search_text) {
                that.showErrorNote('请填写搜索内容！');
                return
            }
            $.ajax({
                type: "get",
                url: url,
                // headers: {
                //     csrfmiddlewaretoken: window.CSRF_TOKEN
                // },
                data: {
                    search_text: search_text
                },
                beforeSend: function (XMLHttpRequest) {
                    that.showLoading();
                },
                success: function (data, textStatus) {
                    if (data.length < 1){
                        that.dom.itemlist.html('');
                    that.showErrorNote('没有搜索到商品！');
                    return
                    }
                    that.append_list(data);
                    that.remove_select();
                },
                complete: function (XMLHttpRequest, textStatus) {
                    that.hideLoading();
                },
                error: function () {
                    that.showErrorNote('程序出现错误，请检查网络， 或者请联系开发人员！！！')
                }
            });
        },

        change_item: function (obj, name) {

            var find_a = this.dom.reportList.find('a[name="' + name + '"]');
            var temp = $(find_a[0]).parent().siblings();
            var n = $(temp[1]);
            var p = $(temp[2]);
            n.text(obj['num']);
            p.text(obj['price']*obj['num']);
        },
        add_item: function (addLink) {
            var tr_obj = {};
            var name = addLink.attr('name');
            tr_obj['num'] = parseFloat(addLink.siblings().val());
            var tds = addLink.parent().siblings();
            var data = [];
            // 对于价格增加可修改项
            tds.each(function () {
                if($(this).text()){
                data.push($(this).text());}
                else{
                    data.push($(this).children().val());
                }
            });
            tr_obj['alias'] = data[0];
            tr_obj['price'] = parseFloat(data[1]).toPrecision(3);

            if (tr_obj['num'] < 0.01 || tr_obj['num'] > parseFloat(data[3]).toPrecision(3)) {
                that.showErrorNote('购买的数量不能为0，也不能大于库存的数量');
            }
            else {
                // 库存数量应该是减去当前选中的量
                tr_obj['store_num'] = parseFloat(data[3]).toPrecision(3) - tr_obj['num'];

                // 当用户选择已经存在的项时，直接修改已有的项
                if (name in this.cache_items){
                    tr_obj['num'] = this.cache_items[name]['num'] + tr_obj['num'];

                    this.change_item(tr_obj, name);
                }else{

                    // 循环添加 tr 减少代码量
                    var report = [];
                    report.push(tr_obj['alias']);
                    report.push(tr_obj['num']);
                    report.push(tr_obj['num'] * tr_obj['price']);

                    var append = '<tr>';
                report.forEach(function (val) {
                    append += '<td>' + val + '</td>';
                });
                append += '<td><a href="javascript:void(0);" class="deletelink" name="'+name+'"></a></td></tr>';
                this.dom.reportListTb.append(append);
                }
                // 将添加的元素放到对象中

                this.cache_items[name] = tr_obj;

                // 修改库存数量的显示
                $(tds[3]).html(tr_obj['store_num']);

                // 计算并显示总价格
                this.countPrice();
            }

        },
        deleteItem: function(deleteLink) {
            var name = deleteLink.attr('name');
            var obj = this.cache_items[name];
            var find_a = this.dom.itemList.find('a[name="' + name + '"]');
            var temp = $(find_a[0]).parent().siblings();
            var n = $(temp[3]);
            n.text(obj['store_num'] + obj['num']);
            deleteLink.parent().parent().remove();
            delete this.cache_items[name];
            this.countMoney();
            this.hideReportList();

        },
        isEmpty: function (obj) {
            for(var name in obj)
            {
                return false;
            }
            return true;
        },

        countMoney: function () {
            var that  = this;

            /* 直接显示总计价格计算 */
            this.dom.countMoney.html(function () {
                if(that.isEmpty(that.cache_items)){
                    return 0;
                }
                var count = 0;
                $.each(that.cache_items,
                    function (key, value) {
                        count += value['num'] * value['price'];
                    });
                return count;
            });
        },
        countPrice: function () {

            this.countMoney();
            this.showReportList();
        },
        init: function () {
            this.cache_items = {};
            this.init_dom();
            this.init_handler();
        }
    };

	this.OrderReport = OrderReport;
})(Suit.$);