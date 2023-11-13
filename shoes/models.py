from django.db import models
from django.urls import reverse, reverse_lazy


class Shoes(models.Model):
    brand = models.CharField(max_length=120, default='brand', verbose_name='Бренд')
    name = models.CharField(max_length=120, default='shoes', verbose_name='Модель')  # varchar
    description = models.TextField(blank=True, null=True, verbose_name='Описание')  # text  с большим пространством
    price = models.FloatField(default=10, verbose_name='Цена')  # число с плавающей запятой
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    date_update = models.DateTimeField(auto_now=True, null=True, verbose_name='Дата изменения')
    photo = models.ImageField(upload_to='Image', null=True, verbose_name='Фото')
    exist = models.BooleanField(default=True, verbose_name='В каталоге?')

    def __str__(self):
        return self.name

    supplier = models.ForeignKey('Supplier', on_delete=models.PROTECT, null=True, verbose_name='Поставщик')

    class Meta:
        verbose_name = 'Обувь'
        verbose_name_plural = 'Обувь'


class Supplier(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название поставщика')
    agent_name = models.CharField(max_length=100, verbose_name='Имя агента поставщика')
    agent_firstname = models.CharField(max_length=100, verbose_name='Фамилия агента поставщика')
    agent_patronymic = models.CharField(max_length=100, verbose_name='Отчество агента поставщика')
    exist = models.BooleanField(default=True, verbose_name='Сотрудники')

    def get_absolute_url(self):
        return reverse('info_supp_view', kwargs={'supplier_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Поставщики'
        verbose_name_plural = 'Поставщики'
        ordering = ['title']


class Order(models.Model):
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    date_finish = models.DateTimeField(null=True, verbose_name='Дата завершения заказа', blank=True)
    price = models.FloatField(null=True, verbose_name='Стоимость заказа')
    address_delivery = models.CharField(max_length=150, verbose_name='Адрес доставки')
    status = models.CharField(max_length=150, verbose_name='Статус',
                              choices=[('1', 'Создан'), ('2', 'Отменен'), ('3', 'Согласован'),
                                       ('4', 'В пути'), ('5', 'Завершен')])

    shoes = models.ManyToManyField(Shoes, through='Pos_order')

    def __str__(self):
        return f"{self.date_create} {self.status} {self.price}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['date_create']

class Pos_order(models.Model):
    shoes = models.ForeignKey(Shoes, on_delete=models.PROTECT, verbose_name='Обувь')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ')
    count_shoes = models.IntegerField(verbose_name='Количество Обуви')
    price = models.FloatField(verbose_name='Общая цена обуви')

    def __str__(self):
        return self.shoes.name + " " + self.order.address + " " + self.order.status

    class Meta:
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции'
        ordering = ['shoes', 'order', 'price']
class Chegue(models.Model):
    date_print = models.DateTimeField(auto_now_add=True, verbose_name='Дата распечатки')
    address_print = models.CharField(max_length=150, verbose_name='Место создания чека')
    terminal = models.CharField(max_length=10, verbose_name='Код терминала')
    order = models.OneToOneField(Order, on_delete=models.PROTECT, primary_key=True, verbose_name='Заказ')

    def __str__(self):
        return str(self.date_print) + " " + self.terminal

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'
        ordering = ['terminal', 'date_print']