from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.index,name='home'),
    # templates
    
    path('form/<str:username>',views.formView,name='upload'),
    path('confirm-user/<str:username>',views.getUserInfo),
    path('auth/<str:username>',views.validateEmailView,name='signin'),
    path('email/<str:username>',views.confirmEmail,name='auth'),
    path('token/<str:username>',views.confirmToken,name='token'),
    path('successfull',views.successPage,name='success-page'),

]

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
