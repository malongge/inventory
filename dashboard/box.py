from __future__ import unicode_literals
import platform
import psutil
from django.utils.translation import ugettext as _
from suit_dashboard.box import Box, Item
from datetime import timedelta

class BoxMachine(Box):
    def get_title(self):
        return _('Machine')

    def get_description(self):
        return _('Information about the hosting machine for my website.')

    # The get_items function is the main function here. It will define
    # what are the contents of the box.
    def get_items(self):
        # Retrieve and format uptime (will not work on Windows)
        # with open('/proc/uptime') as f:
        s = timedelta(seconds=3).total_seconds()
        uptime = _('%d days, %d hours, %d minutes, %d seconds') % (
                s // 86400, s // 3600 % 24, s // 60 % 60, s % 60)

        # Create a first item (box's content) with the machine info
        item_info = Item(
            html_id='sysspec', name=_('System specifications'),
            display=Item.AS_TABLE,
            # Since we use AS_TABLE display, value must be a list of tuples
            value=(
                (_('Hostname'), platform.node()),
                (_('System'), '%s, %s, %s' % (
                    platform.system(),
                    ' '.join(platform.linux_distribution()),
                    platform.release())),
                (_('Architecture'), ' '.join(platform.architecture())),
                (_('Processor'), platform.processor()),
                (_('Python version'), platform.python_version()),
                (_('Uptime'), uptime)
            ),
            classes='table-bordered table-condensed '
                    'table-hover table-striped'
        )

        # Retrieve RAM and CPU data
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()

        # Green, orange, red or grey color for usage/idle
        green, orange, red, grey = '#00FF38', '#FFB400', '#FF3B00', '#EBEBEB'

        ram_color = green  # default
        if ram >= 75:
            ram_color = red
        elif ram >= 50:
            ram_color = orange

        cpu_color = green  # default
        if cpu >= 75:
            cpu_color = red
        elif cpu >= 50:
            cpu_color = orange

        # Now create a chart to display CPU and RAM usage
        chart_options = {
            'chart': {
                'type': 'bar',
                'height': 200,
            },
            'title': {
                'text': _('RAM and CPU usage')
            },
            'xAxis': {
                'categories': [_('CPU usage'), _('RAM usage')]
            },
            'yAxis': {
                'min': 0,
                'max': 100,
                'title': {
                    'text': _('Percents')
                }
            },
            'tooltip': {
                'percentageDecimals': 1
            },
            'legend': {
                'enabled': False
            },
            'plotOptions': {
                'series': {
                    'stacking': 'normal'
                }
            },
            'series': [{
                'name': _('CPU idle'),
                'data': [{'y': 100 - cpu, 'color': grey}, {'y': 0}],
            }, {
                'name': _('CPU used'),
                'data': [{'y': cpu, 'color': cpu_color}, {'y': 0}],
            }, {
                'name': _('RAM free'),
                'data': [{'y': 0}, {'y': 100 - ram, 'color': grey}],
            }, {
                'name': _('RAM used'),
                'data': [{'y': 0}, {'y': ram, 'color': ram_color}],
            }]
        }

        # Create the chart item
        item_chart = Item(
            html_id='highchart-machine-usage',
            name=_('Machine usage'),
            value=chart_options,
            display=Item.AS_HIGHCHARTS)

        # Return the list of items
        return [item_info, item_chart]