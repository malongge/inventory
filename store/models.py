from django.contrib.auth.models import User
from django.db import models


class InfoModel(models.Model):
    address = models.CharField('联系地址', max_length=100, blank=True, null=True)
    phone_number = models.CharField('联系电话', max_length=20)
    add_date = models.DateField('添加日期', auto_now_add=True)

    class Meta:
        abstract = True


class Customer(InfoModel):
    """
    购买商品的客户
    """
    user_name = models.CharField('客户姓名', max_length=15)

    def __str__(self):
        return self.user_name + ': ' + self.phone_number

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'


class ModelServiceMixin(object):
    def _get_my_fields(self):
        return [f.name for f in self._meta.fields]


class Category(models.Model):
    """
    商品分类
    """
    remark = models.TextField('描述信息', blank=True, null=True)
    name = models.CharField('类别名称', max_length=20)
    add_date = models.DateField('添加日期', auto_now_add=True)
    super_category = models.ForeignKey("Category", verbose_name='所属分类', null=True, blank=True,
                                       related_name='parent_category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '类别'
        verbose_name_plural = '类别'
        ordering = ['add_date']


def set_user_name_verbose_name(class_name, parents, attributes):
    user_name = attributes.get('user_name', None)
    if user_name:
        user_name.verbose_name = '供货商姓名'
    return type(class_name, parents, attributes)


class Shop(InfoModel):
    """
    进货商
    """
    user_name = models.CharField('供货商姓名', max_length=15)
    shop_name = models.CharField('供货商名称', max_length=20, unique=True)
    shop_address = models.CharField('供货商地址', max_length=100)

    def __str__(self):
        return self.shop_name

    class Meta:
        verbose_name = '供货商'
        verbose_name_plural = '供货商'
        ordering = ['shop_name']


class Goods(ModelServiceMixin, models.Model):
    """
    商品
    """
    goods_name = models.CharField('商品名称', max_length=15, unique=True)
    average_price = models.DecimalField('进价', default=0, max_digits=10, decimal_places=2)
    last_price = models.DecimalField('售价', default=0, max_digits=10, decimal_places=2)
    unit_name = models.CharField('单位', max_length=10)
    updater = models.ForeignKey(User, editable=False, verbose_name='添加人')
    update_date = models.DateField('更新日期', auto_now_add=True)
    recent_sell = models.DateField('最近售出日期', blank=True, null=True)
    is_delete = models.BooleanField('下架', default=False)
    category = models.ManyToManyField(Category, verbose_name='所属类别')
    shop = models.ForeignKey(Shop, verbose_name='供应商名称', blank=True, null=True)
    remain = models.DecimalField('数目', max_digits=6, decimal_places=2, default=0)
    last_time = models.DateField('有效期', blank=True, null=True)

    def __str__(self):
        return self.goods_name

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['last_time', 'goods_name', 'update_date']

    @property
    def count(self):
        if self.num:
            return int(self.num) * self.last_price
        return 0

    def sell_amount(self):
        return self.remain * self.last_price

    def in_amount(self):
        return self.remain * self.average_price

    def own_amount(self):
        return self.sell_amount() - self.in_amount()

    sell_amount.short_description = '销售总价'
    in_amount.short_description = '进货总价'
    own_amount.short_description = '利润'


class GoodsAddRecord(models.Model):
    """
    增加库存的记录
    """
    goods = models.ForeignKey(Goods, verbose_name='商品名称', related_name='record_goods')
    shop = models.ForeignKey(Shop, verbose_name='供应商', related_name='record_shop')
    number = models.DecimalField('数目', max_digits=6, decimal_places=2)
    remark = models.TextField('说明信息', blank=True, null=True)
    updater = models.ForeignKey(User, verbose_name='操作员')
    date = models.DateTimeField('日期', auto_now_add=True)
    new_price = models.DecimalField('新进价', blank=True, null=True, max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = '增加库存记录'
        verbose_name_plural = '增加库存记录'
        ordering = ['goods', 'number']

    def __str__(self):
        return "%s--%s" % (self.shop, self.goods)


class ReturnRecord(models.Model):
    """
    退订单表
    """
    TYPE_IN_CHOICES = (
        (0, '操作失误'),
        (1, '退货'),
    )
    customer = models.ForeignKey(Customer, verbose_name='退货用户', blank=False, null=True, related_name='return_customer')
    goods = models.ForeignKey(Goods, verbose_name='商品名称', related_name='return_goods')
    shop = models.ForeignKey(Shop, verbose_name='供货商名称', related_name='return_shop')
    amount = models.DecimalField('数目', max_digits=6, decimal_places=2)
    type = models.IntegerField('退送原因', choices=TYPE_IN_CHOICES)
    updater = models.ForeignKey(User, verbose_name='操作员')
    date = models.DateTimeField('日期', auto_now_add=True)
    remark = models.TextField('说明信息', blank=True, null=True)
    reset_price = models.DecimalField('重置价格', blank=True, null=True, max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = '退货处理'
        verbose_name_plural = '退货处理'
        ordering = ['goods', 'amount']

    def __str__(self):
        return "%s--%s--%s" % (self.shop, self.goods, self.amount)


class TransferGoods(models.Model):
    """
    不进入库存
    """
    from_shop = models.ForeignKey(Shop, related_name='from_shop', verbose_name='供应商')
    to_shop = models.ForeignKey(Shop, related_name='to_name', verbose_name='销售商')
    goods = models.ForeignKey(Goods, verbose_name='商品名称')
    change_num = models.DecimalField('数目', max_digits=6, decimal_places=2)
    from_price = models.DecimalField('进价', default=0, max_digits=10, decimal_places=2)
    to_price = models.DecimalField('售价', default=0, max_digits=10, decimal_places=2)
    updater = models.ForeignKey(User, verbose_name='操作人员')
    date = models.DateTimeField('日期', auto_now_add=True)
    remark = models.TextField('说明信息', blank=True, null=True)

    class Meta:
        verbose_name = '直接交易记录'
        verbose_name_plural = '直接交易记录'
        ordering = ['goods', 'change_num']

    def __str__(self):
        return "%s--%s--%s--%s" % (self.from_shop, self.to_shop, self.goods, self.change_num)


class Report(models.Model):
    title = models.CharField('标题', max_length=100, default='志平电子配件销售清单')
    alias = models.CharField('模板名字', max_length=20, default='默认模板')
    ad = models.TextField('广告语')
    phone = models.CharField('电话号码', max_length=50, default='7566409 13755519477')
    address = models.CharField('地址', max_length=50, default='芦溪县凌云南路太阳城B栋良友旁')
    remark = models.TextField('附加信息', blank=True, null=True,
                              default='银行卡号: 6222.0215 0400 3618 261\n中国银行: 6216 6165 0600 0292 464')
    date = models.DateTimeField('日期', auto_now_add=True)
    tag = models.BooleanField('默认模板', default=True)

    def __str__(self):
        return self.alias

    class Meta:
        verbose_name = '设置清单'
        verbose_name_plural = '设置清单'
        ordering = ['-date']


class Order(models.Model):
    customer = models.ForeignKey(Customer, verbose_name='客户名称')
    all_price = models.DecimalField('总价', default=0, max_digits=10, decimal_places=2)
    all_profit = models.DecimalField('总利润', default=0, max_digits=10, decimal_places=2)
    is_delete = models.BooleanField('是否取消订单', default=False)
    updater = models.ForeignKey(User, verbose_name='操作人员')
    date = models.DateTimeField('日期', auto_now_add=True)
    report = models.ForeignKey(Report, verbose_name='清单模板')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '订单记录'
        verbose_name_plural = '订单记录'
        ordering = ['-date']


class ArrearsPrice(models.Model):
    arrears_price = models.DecimalField('欠款额', max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, verbose_name='客户姓名')
    is_arrears = models.BooleanField('清除欠款', default=False)  # 是否欠款
    date = models.DateTimeField('日期', auto_now_add=True)

    def __str__(self):
        return str(self.arrears_price)

    class Meta:
        verbose_name = '欠款记录'
        verbose_name_plural = '欠款记录'
        ordering = ['-date']


from django.db import connection


class SellRecordManager(models.Manager):
    def month_statistic(self, year):

        with connection.cursor() as cursor:
            sql_str = "select count(t.sell_num) as count, substr(t.date,6,2) as month, " \
                      "sum(t.sell_price * t.sell_num) as sell_total, sum(t.average_price * t.sell_num ) as average_total " \
                      "from store_goodssellrecord  as t where t.date like %s group by substr(t.date,1,7);"
            cursor.execute(sql_str, [year + '%'])
            result_list = []
            for row in cursor.fetchall():
                p = {'count': row[0], 'month': row[1], 'sells': row[2], 'averages': row[3]}
                result_list.append(p)
        return result_list

    def year_statistic(self):
        with connection.cursor() as cursor:
            sql_str = "select count(t.sell_num) as count, substr(t.date,1,4) as year, " \
                      "sum(t.sell_price * t.sell_num) as sell_total, sum(t.average_price * t.sell_num ) as average_total " \
                      "from store_goodssellrecord  as t group by substr(t.date,1,4);"
            cursor.execute(sql_str)
            result_list = []
            for row in cursor.fetchall():
                p = {'count': row[0], 'year': row[1], 'sells': row[2], 'averages': row[3]}
                result_list.append(p)
        return result_list

    def day_statistic(self, year):
        with connection.cursor() as cursor:
            sql_str = "select count(t.sell_num) as count, substr(t.date,1,10) as date, " \
                      "sum((t.sell_price  - t.average_price)* t.sell_num) as profit_total " \
                      "from store_goodssellrecord  as t where t.date like %s group by substr(t.date,1,10);"
            cursor.execute(sql_str, [year + '%'])
            result_list = []
            for row in cursor.fetchall():
                p = {'count': row[0], 'date': row[1], 'profits': row[2]}
                result_list.append(p)
        return result_list

from django.utils.html import format_html
class RecordHistory(models.Model):
    date = models.DateTimeField('日期', null=False, blank=False)
    customer = models.ForeignKey(Customer, verbose_name='客户姓名', related_name='record_customer', null=False, blank=False)
    report = models.ForeignKey(Report, related_name='record_report', null=True, blank=False)
    arrears = models.ForeignKey(ArrearsPrice, related_name='record_arrears', null=True, blank=True)


    def view_record(self):
        return format_html('<a href="/store/view_record/{}"><i class="icon-eye-open"></i></a>'.format(self.id))

    view_record.short_description = '查看订单'

    def __str__(self):
        return self.customer.user_name

    class Meta:
        verbose_name = '历史订单查看'
        verbose_name_plural = '历史订单查看'
        ordering = ['-date']


class GoodsSellRecord(models.Model):
    """
    卖出商品记录
    """
    goods = models.ForeignKey(Goods, verbose_name='商品名称', related_name='goods')
    sell_num = models.DecimalField('数目', max_digits=6, decimal_places=2)
    average_price = models.DecimalField('进价', null=True, blank=True, max_digits=10, decimal_places=2)
    sell_price = models.DecimalField('售价', null=True, blank=True, max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, verbose_name='客户姓名', related_name='customer', null=True, blank=True)
    remark = models.TextField('描述信息', blank=True, null=True)
    updater = models.ForeignKey(User, verbose_name='操作人员', related_name='admin')
    date = models.DateTimeField('日期', auto_now_add=True)
    arrears = models.ForeignKey(ArrearsPrice, verbose_name='欠款额', related_name='arrears', null=True, blank=True)
    record = models.ForeignKey(RecordHistory, related_name='report_many_record', null=True, blank=False)
    # def account_actions(self, obj):
    #     return format_html(
    #         '<a class="button" href="{}">Deposit</a>&nbsp;'
    #         '<a class="button" href="{}">Withdraw</a>',
    #         reverse('admin:account-deposit', args=[obj.pk]),
    #         reverse('admin:account-withdraw', args=[obj.pk]),
    #     )
    #
    # account_actions.short_description = 'Account Actions'
    # account_actions.allow_tags = True
    statistic_objects = SellRecordManager()
    objects = models.Manager()

    @property
    def profit(self):
        """
        获取利润
        :return:
        """
        profit = self.sell_num * (self.sell_price - self.average_price)
        return profit

    @property
    def receivable(self):
        """
        销售总额
        :return:
        """
        receivable = self.sell_num * self.sell_price
        return receivable

    class Meta:
        verbose_name = '销售记录'
        verbose_name_plural = '销售记录'
        ordering = ['-date', 'goods', 'sell_num']

    def __str__(self):
        return self.goods.goods_name
