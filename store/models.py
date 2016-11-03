from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.
def modify_fields(**kwargs):
    def wrap(cls):
        for field, prop_dict in kwargs.items():
            for prop, val in prop_dict.items():
                setattr(cls._meta.get_field(field), prop, val)
        return cls
    return wrap


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


class Category(models.Model):
    """
    商品分类
    """
    remark = models.TextField('描述信息', blank=True, null=True)
    name = models.CharField('类别名称', max_length=20)
    add_date = models.DateField('添加日期', auto_now_add=True)
    super_category = models.ForeignKey("self", verbose_name='所属分类', null=True, blank=True)

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


# class Shop(InfoModel):
#     """
#     进货商
#     """
#     # user_name = models.CharField('供货商姓名', max_length=15)
#     shop_name = models.CharField('供货商名称', max_length=20)
#     shop_address = models.CharField('供货商地址', max_length=100)
#
#     def __str__(self):
#         return self.shop_name
#
#     class Meta:
#         verbose_name = '供货商'
#         verbose_name_plural = '供货商'
#         ordering = ['shop_name']


class Shop(InfoModel):
    """
    进货商
    """
    user_name = models.CharField('供货商姓名', max_length=15)
    shop_name = models.CharField('供货商名称', max_length=20)
    shop_address = models.CharField('供货商地址', max_length=100)

    def __str__(self):
        return self.shop_name

    class Meta:
        verbose_name = '供货商'
        verbose_name_plural = '供货商'
        ordering = ['shop_name']


class Goods(models.Model):
    """
    商品
    """
    goods_name = models.CharField('商品名称', max_length=15, unique=True)
    average_price = models.FloatField('进价', default=0)
    last_price = models.FloatField('售价', default=0)
    unit_name = models.CharField('单位', max_length=10)
    add_people = models.ForeignKey(User, editable=False, verbose_name='添加人')
    update_date = models.DateField('更新日期', auto_now_add=True)
    recent_sell = models.DateField('最近售出日期', blank=True, null=True)
    is_delete = models.BooleanField('下架', default=False)
    category = models.ManyToManyField(Category, verbose_name='所属类别')
    shop = models.ForeignKey(Shop, verbose_name='供应商名称', blank=True, null=True)
    remain = models.IntegerField('库存量', default=0)
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
        # current_receipt_purchase_amounts = Purchase.objects.filter(receipt__id=request.id).values_list('price',flat=True)
        # total_amount = sum(current_receipt_purchase_amounts)
        # return total_amount
    def in_amount(self):
         return self.remain * self.average_price

    def own_amount(self):
        return self.sell_amount() - self.in_amount()

    sell_amount.short_description = '销售总价'
    in_amount.short_description = '进货总价'
    own_amount.short_description = '利润'






# class GoodsShop(Goods):
#     """
#     库存
#     """
#     in_price = models.FloatField('新进价', blank=True, null=True)
#
#     def __str__(self):
#         return "%s--%s" % (self.shop, self.goods)
#
#     class Meta:
#         verbose_name = '库存'
#         verbose_name_plural = '库存'
#         ordering = ['goods', 'remain']


class GoodsAddRecord(models.Model):
    """
    增加库存的记录
    """
    goods = models.ForeignKey(Goods, verbose_name='商品名称')
    shop = models.ForeignKey(Shop, verbose_name='供应商')
    number = models.IntegerField('数目')
    remark = models.TextField('说明信息', blank=True, null=True)
    updater = models.ForeignKey(User, verbose_name='操作员')
    date = models.DateTimeField('日期', auto_now_add=True)
    new_price = models.FloatField('新进价', blank=True, null=True)

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
    goods = models.ForeignKey(Goods, verbose_name='商品名称')
    shop = models.ForeignKey(Shop, verbose_name='供货商名称')
    amount = models.IntegerField(verbose_name='数量')
    type = models.IntegerField('退送原因', choices=TYPE_IN_CHOICES)
    updater = models.ForeignKey(User, verbose_name='操作员')
    date = models.DateTimeField('日期', auto_now_add=True)
    remark = models.TextField('说明信息', blank=True, null=True)

    class Meta:
        verbose_name = '退送库存记录'
        verbose_name_plural = '退送库存记录'
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
    change_num = models.IntegerField('交易数量')
    from_price = models.FloatField('进价', default=0)
    to_price = models.FloatField('售价', default=0)
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
    all_price = models.FloatField('总价', default=0)
    all_profit = models.FloatField('总利润', default=0)
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


class GoodsSellRecord(models.Model):
    """
    卖出商品记录
    """
    goods = models.ForeignKey(Goods, verbose_name='商品名称', related_name='goods')
    sell_num = models.IntegerField('销售数目')
    average_price = models.FloatField('进价', null=True, blank=True)
    sell_price = models.FloatField('售价', null=True, blank=True)
    is_arrears = models.BooleanField('是否欠款', default=False)  # 是否欠款
    customer = models.ForeignKey(Customer, verbose_name='客户姓名', related_name='customer', null=True, blank=True)
    remark = models.TextField('描述信息', blank=True, null=True)
    updater = models.ForeignKey(User, verbose_name='操作人员', related_name='admin')
    date = models.DateTimeField('日期', auto_now_add=True)
    arrears_price = models.FloatField('欠款额', null=True, blank=True)

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
