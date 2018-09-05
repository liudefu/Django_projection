# coding = utf-8
from django.conf.urls import url

from payment.views import PaymentView

urlpatterns = [
    url(r'^orders/(?P<order_id>\d+)/$',PaymentView.as_view(),name='pay_by_alipay'),
]
