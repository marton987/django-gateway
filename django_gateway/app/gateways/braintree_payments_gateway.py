from django.conf import settings
from app.gateway import Gateway, TransactionProblem
from app.models import MerchantTransaction
import braintree


class BraintreePaymentsGateway(Gateway):

    def __init__(self):
        if self.test_mode:
            env = braintree.Environment.Sandbox
        else:
            env = braintree.Environment.Production
        merchant_settings = getattr(settings, "MERCHANT_SETTINGS")
        if  not merchant_settings or \
            not merchant_settings.get("braintree_payments"):

            raise GatewayNotConfigured("The '%s' gateway is not correctly "
                                       "configured." % self.display_name)
        braintree_settings = merchant_settings['braintree_payments']
        braintree.Configuration.configure(
            env,
            braintree_settings['MERCHANT_ACCOUNT_ID'],
            braintree_settings['PUBLIC_KEY'],
            braintree_settings['PRIVATE_KEY']
        )

    def create_transaction(self, user, cardholder_name, amount, number,
                           month, year, cvv):
        """
        Create a purchase with the provided Credit Card and stores the 
        Transaction result in the table Transaction
        """
        result = braintree.Transaction.sale({
            "amount": amount,
            "credit_card": {
                "cardholder_name": cardholder_name,
                "number": number,
                "expiration_month": month,
                "expiration_year": year,
                "cvv": cvv,
            }
        })
        if result.is_success:
            transaction = MerchantTransaction.objects.create(
                merchant_id=result.transaction.id,
                user=user,
                gateway='braintree',
                status='success',
                response=result.transaction
            )
        elif result.transaction:
            transaction = MerchantTransaction.objects.create(
                merchant_id=result.transaction.id,
                user=user,
                gateway='braintree',
                status='failure',
                message=result.message,
                response=result.transaction
            )
        else:
            print("message: " + result.message)
            for error in result.errors.deep_errors:
                print("attribute: " + error.attribute)
                print("  code: " + error.code)
                print("  message: " + error.message)
            raise TransactionProblem("We had a problem with your transaction")
        return transaction
