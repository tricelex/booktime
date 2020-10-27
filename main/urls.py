from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView, DetailView
from rest_framework import routers
from main import views, models, forms, endpoints, admin

router = routers.DefaultRouter()
router.register(r"orderlines", endpoints.PaidOrderLineViewSet)
router.register(r"orders", endpoints.PaidOrderViewSet)

urlpatterns = [
    path("address/", views.AddressListView.as_view(), name="address_list"),
    path("address/create/", views.AddressCreateView.as_view(), name="address_create"),
    path("address/<int:pk>/", views.AddressUpdateView.as_view(), name="address_update"),
    path(
        "address/<int:pk>/delete/",
        views.AddressDeleteView.as_view(),
        name="address_delete",
    ),
    path(
        "order/done/",
        TemplateView.as_view(template_name="order_done.html"),
        name="checkout_done",
    ),
    path(
        "order/address_select/",
        views.AddressSelectionView.as_view(),
        name="address_select",
    ),
    path("order-dashboard/", views.OrderView.as_view(), name="order-dashboard"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="login.html",
            form_class=forms.AuthenticationForm,
        ),
        name="login",
    ),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("products/<slug:tag>/", views.ProductListView.as_view(), name="products"),
    path(
        "product/<slug:slug>/",
        DetailView.as_view(model=models.Product),
        name="product",
    ),
    path("add_to_basket/", views.add_to_basket, name="add_to_basket"),
    path("basket/", views.manage_basket, name="basket"),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "about-us/",
        TemplateView.as_view(template_name="about_us.html"),
        name="about_us",
    ),
    path("contact-us/", views.ContactUsView.as_view(), name="contact_us"),
    path("api/", include(router.urls)),
    path("admin/", admin.main_admin.urls),
    path("office-admin/", admin.central_office_admin.urls),
    path("dispatch-admin/", admin.dispatchers_admin.urls),
]
