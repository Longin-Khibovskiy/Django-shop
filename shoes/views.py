from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Shoes
from .forms import ShoesForm
from .models import Shoes, Supplier, Order, Pos_order, Chegue
from .forms import ShoesForm, SupplierForm, RegistrationForm, LoginForm, ContactForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .utils import Default_value
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.http import JsonResponse
from .serializers import ShoesSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from basket.forms import BasketAddProductForm


# Create your views here.
def index(request):
    print(request)
    return HttpResponse('Hello django')


def shoes(request):
    shoes = Shoes.objects.all()  # Возврат всех записей из БД
    responce = '<h1>Список нашей обуви</h1>'
    for item in shoes:
        responce += f'<div>\n<p>{item.name}</p>\n<p>{item.price}</p></div>'
    # responce += '<h3>Banana</h3>'
    # responce += '<h4>Avocado</h4>'
    return HttpResponse(responce)


def index_template(request):
    return render(request, 'shoes/index.html')


def shoes_template(request):
    context = {'title': 'Обувь'}
    shoeses = Shoes.objects.all()
    paginator = Paginator(shoeses, 8)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    context['page_obj'] = page_objects

    if request.method == "GET":
        shoes_id = request.GET.get('name', 'NIKE')
        try:
            shoes_one = Shoes.objects.get(pk=shoes_id)
        except:
            pass
        else:
            context['shoes_one'] = shoes_one
        context['name'] = request.GET.get('name', 'NIKE')
    elif request.method == "POST":
        shoes_id = request.POST.get('name', 'NIKE')
        try:
            shoes_one = Shoes.objects.get(pk=shoes_id)
        except:
            pass
        else:
            context['shoes_one'] = shoes_one
        context['name'] = request.POST.get('name', 'NIKE')

    return render(request=request,
                  template_name='shoes/shoes-all.html',
                  context=context)


@permission_required('shoes.add_shoes')
def shoes_add(request):
    if request.method == "POST":
        context = dict()
        context['brand'] = request.POST.get('brand')
        context['name'] = request.POST.get('name')
        context['description'] = request.POST.get('description')
        context['price'] = request.POST.get('price')
        context['photo'] = request.POST.get('photo')

        Shoes.objects.create(
            brand=context['brand'],
            name=context['name'],
            description=context['description'],
            price=context['price'],
            photo=context['photo']
        )
        return HttpResponseRedirect('/shoes/list/')
    else:
        shoesform = ShoesForm()
        context = {'form': shoesform}
        return render(request, 'shoes/shoes-add.html', context=context)


@login_required
def shoes_detail(request, shoes_id):
    shoeses = get_object_or_404(Shoes, pk=shoes_id)
    basket_form = BasketAddProductForm()
    return render(request, 'shoes/shoes-info.html', {'shoes_item': shoeses, 'basket_form': basket_form})


# Supplier --------------------------------------------

def supplier_list(request):
    suppliers = Supplier.objects.filter(exist=True).order_by('title')
    return render(request, 'shoes/supplier/supplier-list.html',
                  {'supplier': suppliers, 'title': 'Список поставщиков из функции'})


class SupplierListView(ListView, Default_value):
    model = Supplier
    template_name = 'shoes/supplier/supplier-list.html'  # Путь шаблона
    context_object_name = 'supplier'  # Отправка данных по заданному ключу
    extra_context = {'title': 'Список поставщиков из класса'}  # Доп. значения (статичные значения)

    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем атрибуты из класса
        print(context)
        context = self.add_title_context(context=context, title_name='Страница брендов')

        context['info'] = 'Страница брендов, которые с нами работают'
        return context

    def get_queryset(self):
        return Supplier.objects.filter(exist=True).order_by('title')


class SupplierDetailView(DetailView):

    model = Supplier
    template_name = 'shoes/supplier/supplier-info.html'

    context_object_name = 'one_supplier'
    pk_url_kwarg = 'supplier_id'


def supplier_form(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)

            Supplier.objects.create(
                title=form.cleaned_data['title'],
                agent_name=form.cleaned_data['agent_name'],
                agent_firstname=form.cleaned_data['agent_firstname'],
                agent_patronymic=form.cleaned_data['agent_patronymic'],
                exist=form.cleaned_data['exist'],
            )
            return redirect('list_supp')
        else:
            context = {'form': form}
            return render(request, 'shoes/supplier/supplier-add.html', context)
    else:
        form = SupplierForm()
        context = {'form': form}
        return render(request, 'shoes/supplier/supplier-add.html', context)


class SupplierCreateView(CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'shoes/supplier/supplier-add.html'
    context_object_name = 'form'
    success_url = reverse_lazy('list_supp_view')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SupplierUpdateView(UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'shoes/supplier/supplier-edit.html'
    context_object_name = 'from'

    @method_decorator(permission_required('shoes.change_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = reverse_lazy('list_supp_view')

    @method_decorator(permission_required('shoes.delete_supplier'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


def user_registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            return redirect('index_shoes')
    else:
        form = RegistrationForm()
    return render(request, 'shoes/auth/registration.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print('is_anon', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            login(request, user)
            print('is_anon', request.user.is_anonymous)
            print('is_auth', request.user.is_authenticated)
            print(user)
            return redirect('index_shoes')
    else:
        form = LoginForm()
    return render(request, 'shoes/auth/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('log in')


def contact_email(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(
                form.cleaned_data['subject'],
                form.cleaned_data['content'],
                settings.EMAIL_HOST_USER,
                ['django.project@mail.ru'],
                fail_silently=True,
            )
            if mail:
                return redirect('index_shoes')
    else:
        form = ContactForm()
    return render(request, 'shoes/email.html', {'form': form})


@api_view(['GET', 'POST'])
def shoes_api_list(request):
    if request.method == 'GET':
        shoes_list = Shoes.objects.all()
        serializer = ShoesSerializer(shoes_list, many=True)
        return Response({'shoes_list': serializer.data})
    elif request.method == 'POST':
        serializer = ShoesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def shoes_api_detail(request, pk, format=None):
    shoes_obj = get_object_or_404(Shoes, pk=pk)
    if shoes_obj.exist:
        if request.method == 'GET':
            serializer = ShoesSerializer(shoes_obj)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ShoesSerializer(shoes_obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Данные успешно изменены', 'shoes': serializer.data})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELEET':
            shoes_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
