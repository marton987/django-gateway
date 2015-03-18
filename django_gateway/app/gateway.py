from django.utils.importlib import import_module
from django.conf import settings

gateway_cache = {}


class TransactionProblem(Exception):
    pass


class GatewayModuleNotFound(Exception):
    pass


class InvalidData(Exception):
    pass


class Gateway(object):

    """Sub-classes to inherit from this and implement the below methods"""

    # To indicate if the gateway is in test mode or not
    test_mode = getattr(settings, "MERCHANT_TEST_MODE", True)

    # The below are optional attributes to be implemented and used by subclases.
    #
    # Set to indicate the default currency for the gateway.
    default_currency = ""
    # Sequence of countries supported by the gateway in ISO 3166 alpha-2 format.
    # http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
    supported_countries = []
    # Sequence of supported card types by the gateway. Members should be valid
    # subclasses of the Credit Card object.
    supported_cardtypes = []
    # Home page URL for the gateway. Used for information purposes only.
    homepage_url = ""
    # Name of the gateway.
    display_name = ""
    # Application name or some unique identifier for the gateway.
    application_id = ""


def get_gateway(gateway, *args, **kwargs):
    """
    Return a gateway instance specified by `gateway` name.
    This caches gateway classes in a module-level dictionnary to avoid hitting
    the filesystem every time we require a gateway.

    Should the list of available gateways change at runtime, one should then
    invalidate the cache, the simplest of ways would be to:

    >>> gateway_cache = {}
    """
    # Is the class in the cache?
    clazz = gateway_cache.get(gateway, None)
    if not clazz:
        # Let's actually load it (it's not in the cache)
        gateway_filename = "%s_gateway" % gateway
        gateway_module = None
        for app in settings.INSTALLED_APPS:
            try:
                gateway_module = import_module(
                    ".gateways.%s" % gateway_filename, package=app)
            except ImportError:
                pass
        if not gateway_module:
            raise GatewayModuleNotFound("Missing gateway: %s" % (gateway))
        gateway_class_name = "".join(gateway_filename.title().split("_"))
        try:
            clazz = getattr(gateway_module, gateway_class_name)
        except AttributeError:
            raise GatewayNotConfigured(
                "Missing %s class in the gateway module." % gateway_class_name)
        gateway_cache[gateway] = clazz
    # We either hit the cache or load our class object, let's return an instance
    # of it.
    return clazz(*args, **kwargs)
