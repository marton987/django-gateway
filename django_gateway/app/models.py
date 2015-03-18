from django.db import models
from django.contrib.auth.models import User

GATEWAY_CHOICE = (
    ('braintree', 'Braintree Payments'),
    ('paypal', 'PayPal'),
)


class MerchantTransaction(models.Model):
    
    """
    merchant_id: Identifier of the Merchant used for this transaction
    user: User who made this transaction
    gateway: gateway used
    status: Status of the transaction
    message: Message returned by the Merchant
    response: Complete response of the Merchant
    """
    TRANSACTION_STATUS_CHOICE = (
        ('success', 'Success'),
        ('failure', 'Failure'),
    )
    merchant_id = models.CharField(max_length = 20, verbose_name="Merchant id")
    user = models.ForeignKey(User, verbose_name="User")
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    gateway = models.CharField(max_length = 10, choices=GATEWAY_CHOICE, verbose_name="Gateway")
    status = models.CharField(max_length = 10, choices=TRANSACTION_STATUS_CHOICE, verbose_name="Status")
    message = models.TextField(blank=True, null=True, verbose_name="Message")
    response = models.TextField(blank=True, null=True, verbose_name="Response")
    timestamp = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Timestamp")

    def __unicode__(self):
        return self.merchant_id

    class Meta:
        verbose_name = "Merchant transaction"
        verbose_name_plural = "Merchant transactions"