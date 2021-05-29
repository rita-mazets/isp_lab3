from django.views.generic.detail import SingleObjectMixin, View
from .models import Category, Cart, Customer, PizzaProduct, BeerProduct
from .custom_logging import logger

class CategoryDetailMixin(SingleObjectMixin):

    CATEGORY_SLUG2PRODUCT_MODEL = {
        'pizza': PizzaProduct,
        'beer': BeerProduct
    }

    def get_context_data(self, **kwargs):
        logger.info('Использование CategoryDetailMixin')
        if isinstance(self.get_object(), Category):
            model = self.CATEGORY_SLUG2PRODUCT_MODEL[self.get_object().slug]
            context = super().get_context_data(**kwargs)
            context['categories'] = Category.objects.get_categories_for_left_sidebar()
            context['category_products'] = model.objects.all()
            return context
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.get_categories_for_left_sidebar()
        return context



class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        logger.info(f"Использование CartMixin пользователем {user}")
        if request.user.is_authenticated:
            customer = Customer.objects.filter(user=request.user).first()
            if not customer:
                customer = Customer.objects.create(
                    user=request.user    
                )
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            logger.warning('Покупатель не авторизирован')
            cart = Cart.objects.filter(for_anonymous_user=True).first()
            if not cart:
                cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)