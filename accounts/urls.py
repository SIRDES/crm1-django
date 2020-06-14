
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('products/', views.products, name="products"),
    path('customers/<str:pk>/', views.customers, name="customers"),
    path('user/', views.userProfile, name="userProfile"),
    path('accountSettings/', views.accountSettings, name="accountSettings"),

    path('create_order/', views.createOrder, name="create_order"),
    path('createCustomer/', views.createCustomer, name="createCustomer"),
    path('update_order/<str:pk>/', views.updateOrder, name="updateOrder"),
    path('deleteOrder/<str:pk>/', views.deleteOrder, name="deleteOrder"),

    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name="logout"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),

]
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )
