from sqlalchemy_utils import force_auto_coercion

# todo проверить
force_auto_coercion()

from . import catalog, identity, processing, risk, vault
