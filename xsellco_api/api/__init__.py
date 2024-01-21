import warnings

from xsellco_api.common.base import DEPRECATION_MESSAGE

# Issue a deprecation warning
warnings.warn(DEPRECATION_MESSAGE, DeprecationWarning, stacklevel=2)

from .channels import Channels  # noqa
from .repricers import Repricers  # noqa
from .users import Users  # noqa
