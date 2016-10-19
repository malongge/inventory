(function ($) {
    $(document).ready(function ($) {

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
                        tbody += '<td>' + obj.price + '</td>';
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

        var report_ids = {};

        function count_ids(name, num) {
            if(name in report_ids) {
                report_ids[name] = report_ids[name] + num;
            }
            else{
                report_ids[name] = num;
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
                data.push($(this).text());
            });
            console.warn(num);
            if (num > parseInt(data[3]) || num == 0) {

                alert('购买的数量不能为0，也不能大于库存的数量');
            } else {
                var report = [];
                var name = data[0];
                report.push(name);
                report.push(num);
                var price = num * parseInt(data[1]);
                report.push(price);


                var append = '<tr>';
                report.forEach(function (val) {
                    append += '<td>' + val + '</td>';
                });
                append += '<td><a href="javascript:void(0);" class="deletelink"></a></td></tr>';
                $('.report .report-list tbody').append(append);
                $(tds[3]).html(parseInt(data[3]) - num);
                count_ids(item.attr('name'), num);
            }



            /* 直接显示总计价格计算 */
            $('.report .count-money p').html(function () {
                var count = 0;
                $('.report-list tbody tr').each(
                    function () {
                        count += parseInt($(this)[0].children[2].textContent);
                    });
                return count;
            });

            if ($('.report').hasClass('nodisplay')) {
                $('.report').removeClass('nodisplay');
            }

        })}

        addLinkEvent();

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
            StandardPost(window.report_url, JSON.stringify(report_ids));
            report_ids = {}
        })
    });
})(django.jQuery);