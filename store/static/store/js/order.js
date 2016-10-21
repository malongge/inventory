
(function ($) {
    $(document).ready(function ($) {

        var report_ids = {};
        var price_ids = {};

         // function deleteLink(thi) {
         //        console.log(thi);
         //    }

        $('#sidebar ul li:first').addClass('select');

        function showLoading() {

        }

        function hideLoading() {

        }




        $("#sidebar li").click(function () {

            var url = $(this).attr('value');


            $(this).addClass('select').siblings().removeClass("select");

            $.ajax({
                type: "get",
                url: url,
                beforeSend: function (XMLHttpRequest) {
                    showLoading();
                },
                success: function (data, textStatus) {
                    console.log(textStatus);
                    console.log(data);
                    var tbody = '';
                    data.forEach(function (obj) {
                        tbody += '<tr>';
                        tbody += '<td>' + obj.name + '</td>';
                        tbody += '<td><input value="' + obj.price + '" type="number"></td>';
                        tbody += '<td>' + obj.unit + '</td>';
                        tbody += '<td>' + obj.remain + '</td>';
                        tbody += '<td><input value="1" type="number">' +
                            '<a href="javascript:void(0);" class="addlink" name="'+obj.id+'">添加到清单</a></td></tr>';

                    });
                    $('.item-list tbody').html(tbody);
                    addLinkEvent();
                },
                complete: function (XMLHttpRequest, textStatus) {
                    hideLoading();
                },
                error: function () {
                    alert('程序出现错误，请检查网络， 或者请联系开发人员！！！')
                }
            });

        });



        function count_ids(name, num) {
            if(name in report_ids) {
                report_ids[name] = report_ids[name] + num;
            }
            else{
                report_ids[name] = num;
            }
        }

        function sub_ids(name, num) {

            if (report_ids[name] > num) {
                report_ids[name] = report_ids[name] - num;
            }
            else{
                delete report_ids[name];
            }
        }

        function addLinkEvent() {
        $(".item-list .addlink").click(function () {
            var item = $(this);
            console.log(item);
            var num = parseInt(item.siblings().val());
            var tds = item.parent().siblings();
            var data = [];
            tds.each(function () {
                if($(this).text()){
                data.push($(this).text());}
                else{
                    data.push($(this).children().val());
                }
                // console.log(data);
            });
            console.warn(num);
            if (num > parseInt(data[3]) || num == 0) {

                alert('购买的数量不能为0，也不能大于库存的数量');
            } else {
                var report = [];
                var name = data[0];
                report.push(name);
                report.push(num);
                var price = num * parseFloat(data[1]);
                report.push(price);

                var find_a = $('.report-list tbody tr').find("a[name='"+item.attr('name')+"']");
                // 以输入的实际价格为标准计算
                if (!!find_a.length){
                    var temp = $(find_a[0]).parent().siblings();
                    var n = $(temp[1]);
                    var p = $(temp[2]);
                    n.text(parseInt(n.text())+num);
                    p.text(price*(report_ids[item.attr('name')]+num));

                }else{
                    var append = '<tr>';
                report.forEach(function (val) {
                    append += '<td>' + val + '</td>';
                });
                append += '<td><a href="javascript:void(0);" class="deletelink" name="'+item.attr('name')+'"></a></td></tr>';
                $('.report .report-list tbody').append(append);
                }

                $(tds[3]).html(parseInt(data[3]) - num);
                count_ids(item.attr('name'), num);
                price_ids[item.attr('name')] = parseFloat(data[1]);

            }

            /* 直接显示总计价格计算 */
            $('.report .count-money p').html(function () {
                var count = 0;
                $('.report-list tbody tr').each(
                    function () {
                        count += parseFloat($(this)[0].children[2].textContent);
                    });
                return count;
            });

            if ($('.report').hasClass('nodisplay')) {
                $('.report').removeClass('nodisplay');
            }

        });
            // $('.deletelink').click(function () {
            //     var temp_name = $(this).attr('name');
            //     var temp_num =  parseInt($($(this).parent().siblings()[1]).text());
            //     console.log(report_ids);
            //     sub_ids(temp_name, temp_num);
            //     $(this).parent().parent().remove()
            // });
        }

        addLinkEvent();

        $(".report-list").delegate(".deletelink","click",function(){
            var temp_name = $(this).attr('name');
                var temp_num =  parseInt($($(this).parent().siblings()[1]).text());
                console.log(report_ids);
                sub_ids(temp_name, temp_num);
            delete price_ids[temp_name];
            var find_a = $('.item-list tbody tr').find("a[name='"+temp_name+"']");
                // 以输入的实际价格为标准计算
                if (!!find_a.length){
                    var temp = $(find_a[0]).parent().siblings();
                    var n = $(temp[3]);
                    n.text(parseInt(n.text())+temp_num);

                }
                $(this).parent().parent().remove();
            $('.report .count-money p').html(function () {
                var count = 0;
                $('.report-list tbody tr').each(
                    function () {
                        count += parseFloat($(this)[0].children[2].textContent);
                    });
                return count;
            });
        });


        function StandardPost (url,args)
        {
            // var body = $(document.body);
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
        }

        $('.print-link').click(function () {
            console.log(JSON.stringify(report_ids));
            var r=confirm("你确定要打印清单吗，确定的话会生成销售记录，并扣减商品数量！！！");
            if (r == true){
                var data = {};
            data['num'] = report_ids;
            data['price']= price_ids;
            StandardPost(window.report_url, JSON.stringify(data));
            report_ids = {};
            price_ids = {};
            }

        })
    });
})(django.jQuery);