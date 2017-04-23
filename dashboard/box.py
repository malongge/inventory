from __future__ import unicode_literals

from store.models import GoodsSellRecord, Goods
from suit_dashboard.box import Box, Item


#
# class BoxMachine(Box):
#     def get_title(self):
#         return _('Machine')
#
#     def get_description(self):
#         return _('Information about the hosting machine for my website.')
#
#     # The get_items function is the main function here. It will define
#     # what are the contents of the box.
#     def get_items(self):
#         # Retrieve and format uptime (will not work on Windows)
#         # with open('/proc/uptime') as f:
#         s = timedelta(seconds=3).total_seconds()
#         uptime = _('%d days, %d hours, %d minutes, %d seconds') % (
#             s // 86400, s // 3600 % 24, s // 60 % 60, s % 60)
#
#         # Create a first item (box's content) with the machine info
#         item_info = Item(
#             html_id='sysspec', name=_('System specifications'),
#             display=Item.AS_TABLE,
#             # Since we use AS_TABLE display, value must be a list of tuples
#             value=(
#                 (_('Hostname'), platform.node()),
#                 (_('System'), '%s, %s, %s' % (
#                     platform.system(),
#                     ' '.join(platform.linux_distribution()),
#                     platform.release())),
#                 (_('Architecture'), ' '.join(platform.architecture())),
#                 (_('Processor'), platform.processor()),
#                 (_('Python version'), platform.python_version()),
#                 (_('Uptime'), uptime)
#             ),
#             classes='table-bordered table-condensed '
#                     'table-hover table-striped'
#         )
#
#         # Retrieve RAM and CPU data
#         ram = psutil.virtual_memory().percent
#         cpu = psutil.cpu_percent()
#
#         # Green, orange, red or grey color for usage/idle
#         green, orange, red, grey = '#00FF38', '#FFB400', '#FF3B00', '#EBEBEB'
#
#         ram_color = green  # default
#         if ram >= 75:
#             ram_color = red
#         elif ram >= 50:
#             ram_color = orange
#
#         cpu_color = green  # default
#         if cpu >= 75:
#             cpu_color = red
#         elif cpu >= 50:
#             cpu_color = orange
#
#         # Now create a chart to display CPU and RAM usage
#         chart_options = {
#             'chart': {
#                 'type': 'bar',
#                 'height': 200,
#             },
#             'title': {
#                 'text': _('RAM and CPU usage')
#             },
#             'xAxis': {
#                 'categories': [_('CPU usage'), _('RAM usage')]
#             },
#             'yAxis': {
#                 'min': 0,
#                 'max': 100,
#                 'title': {
#                     'text': _('Percents')
#                 }
#             },
#             'tooltip': {
#                 'percentageDecimals': 1
#             },
#             'legend': {
#                 'enabled': False
#             },
#             'plotOptions': {
#                 'series': {
#                     'stacking': 'normal'
#                 }
#             },
#             'series': [{
#                 'name': _('CPU idle'),
#                 'data': [{'y': 100 - cpu, 'color': grey}, {'y': 0}],
#             }, {
#                 'name': _('CPU used'),
#                 'data': [{'y': cpu, 'color': cpu_color}, {'y': 0}],
#             }, {
#                 'name': _('RAM free'),
#                 'data': [{'y': 0}, {'y': 100 - ram, 'color': grey}],
#             }, {
#                 'name': _('RAM used'),
#                 'data': [{'y': 0}, {'y': ram, 'color': ram_color}],
#             }]
#         }
#
#         # Create the chart item
#         item_chart = Item(
#             html_id='highchart-machine-usage',
#             name=_('Machine usage'),
#             value=chart_options,
#             display=Item.AS_HIGHCHARTS)
#
#         # Return the list of items
#         return [item_info, item_chart]


class BoxSellStatistics(Box):
    def __init__(self, **kwargs):
        self.year = kwargs.get('year', '2016')
        super(BoxSellStatistics, self).__init__(**kwargs)

    # def get_title(self):
    #     return '商品盈利表'

    def get_description(self):
        return '统计 {} 全年各个月份盈利情况'.format(self.year)

    # The get_items function is the main function here. It will define
    # what are the contents of the box.
    def get_items(self):
        data = GoodsSellRecord.statistic_objects.month_statistic(self.year)
        # value

        monthes = []
        sell_counts = []
        average_counts = []
        profit_counts = []
        for val in data:
            monthes.append(val['month'])
            # sells = Decimal(val['sells']).quantize(Decimal('0.00'))
            sells = round(val['sells'], 2)
            sell_counts.append(sells)
            averages = round(val['averages'], 2)
            average_counts.append(averages)
            profit_counts.append(round(sells - averages, 2))
        values = [{'name': '销售总额', 'data': sell_counts},
                  {'name': '进价总额', 'data': average_counts},
                  {'name': '利润总额', 'data': profit_counts}]

        # # Create a first item (box's content) with the machine info
        # item_info = Item(
        #     html_id='sell-statistic-table',
        #     display=Item.AS_HIGHCHARTS,
        #     # Since we use AS_TABLE display, value must be a list of tuples
        #     value=data
        #     ,
        #     classes='table-bordered table-condensed '
        #             'table-hover table-striped'
        # )

        chart_options = {
            'chart': {
                'type': 'bar'
            },
            'title': {
                'text': '{} 全年盈利图表'.format(self.year)
            },
            'subtitle': {
                'text': '全年总销售额--{} ,总利润--{}'.format(sum(sell_counts), sum(profit_counts))
            },
            'xAxis': {
                'categories': monthes,
                'title': {
                    'text': '月份'
                }
            },
            'yAxis': {
                'min': 0,
                'title': {
                    'text': '单位（元）',
                    'align': 'high'
                },
                'labels': {
                    'overflow': 'justify'
                }
            },
            'tooltip': {
                'headerFormat': '<b>{point.x}月份</b><br>',
                'valuePrefix': '￥',
                'valueSuffix': '元'
            },
            'plotOptions': {
                'bar': {
                    'dataLabels': {
                        'enabled': True
                    }
                }
            },
            'legend': {
                'layout': 'vertical',
                'align': 'right',
                'verticalAlign': 'top',
                'x': -40,
                'y': 100,
                'floating': True,
                'borderWidth': 1,
                'backgroundColor': "((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF')",
                'shadow': True
            },
            'credits': {
                'enabled': False
            },
            'series': values
        }

        # Create the chart item
        item_chart = Item(
            html_id='highchart-{}-sell-statistics'.format(self.year),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


class DaySellStatistics(BoxSellStatistics):
    # def get_title(self):
    #     return '趋势走向表'

    def get_description(self):
        return '在 {} 年中盈利的走向图'.format(self.year)

    # The get_items function is the main function here. It will define
    # what are the contents of the box.
    def get_items(self):
        data = GoodsSellRecord.statistic_objects.day_statistic(self.year)
        # value
        days = []
        months = []
        for val in data:
            # print(val)
            # days.append([datetime.strptime(val['date'], '%Y-%m-%d'), val['profits']])
            months.append(val['date'].split('-')[1])
            days.append([val['date'], val['profits']])
        # print(days)
        # monthes = []
        # sell_counts = []
        # average_counts = []
        # profit_counts = []
        # for val in data:
        #     monthes.append(val['month'])
        #     # sells = Decimal(val['sells']).quantize(Decimal('0.00'))
        #     sells = round(val['sells'], 2)
        #     sell_counts.append(sells)
        #     averages = round(val['averages'], 2)
        #     average_counts.append(averages)
        #     profit_counts.append(sells - averages)
        # values = [{'name': '销售总额', 'data': sell_counts},
        #           {'name': '进价总额', 'data': average_counts},
        #           {'name': '利润总额', 'data': profit_counts}]

        # # Create a first item (box's content) with the machine info
        # item_info = Item(
        #     html_id='sell-statistic-table',
        #     display=Item.AS_HIGHCHARTS,
        #     # Since we use AS_TABLE display, value must be a list of tuples
        #     value=data
        #     ,
        #     classes='table-bordered table-condensed '
        #             'table-hover table-striped'
        # )

        chart_options = {
            # 'chart': {
            #     'type': 'spline'
            # },
            'title': {
                'text': '{} 年利润走势图'.format(self.year)
            },
            'xAxis': {
                'categories': months,
                'tickInterval': 7,
                'labels': {  # don't display the dummy year
                    'align': 'right',
                    'rotation': -30

                },
                'title': {
                    'text': '间隔为1周，时间刻度月份'
                }
            },
            'yAxis': {
                'title': {
                    'text': '数额(元)'
                },
                'min': 0
            },
            'tooltip': {
                'headerFormat': '<b>{series.name}</b><br>',
                'pointFormat': '{point.y:.2f}'
            },
            'plotOptions': {
                'spline': {
                    'marker': {
                        'enabled': True
                    }
                }
            }, 'credits': {
                'enabled': False
            },
            'series': [{
                'name': '利润',
                'data': days

            }]

        }
        # Create the chart item
        item_chart = Item(
            html_id='highchart-{}-day-statistics'.format(self.year),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]


# class CategoryBox(Box):
#     def __init__(self):
#         pass
class RemainStatisticBox(Box):
    def get_description(self):
        return '库存统计图'



    def get_items(self):
        ret = Goods.statistic_objects.remain_statistic()
        print(ret)
        sum_remain = sum([sum(val['data']) for val in ret['value']])
        chart_options = {
            # 'chart': {
            #     'type': 'bar'
            # },
            'title': {
                'text': '按年统计库存'
            },
            'subtitle': {
                'text': '总库存量 {}'.format(sum_remain)
            },
            'xAxis': {
                'categories': ret['x']},
            'yAxis': {
                'title': {
                    'text': '价格 (￥)'
                },
                # 'plotLines': [{
                #     'value': 0,
                #     'width': 10000,
                #     # 'color': '#808080'
                # }]
            },
            'tooltip': {
                # 'headerFormat': '<b>{point.x}月份</b><br>',
                # 'valuePrefix': '￥',
                'valueSuffix': '元'
            },
            'legend': {
                'layout': 'vertical',
                'align': 'right',
                'verticalAlign': 'middle',
                'borderWidth': 1,
                # 'backgroundColor': "((Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF')",
                'shadow': True
            },
            'credits': {
                'enabled': False
            },
            'series': ret['value']
        }

        item_chart = Item(
            html_id='highchart-remain-statistics',
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_chart]
