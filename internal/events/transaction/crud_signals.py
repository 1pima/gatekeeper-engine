from internal.models.processing import Transaction


@Transaction.after_created.connect
def after_transaction_created(transaction: Transaction, desc=None):
    pass


@Transaction.after_authorized.connect
def after_transaction_authorized(transaction: Transaction, desc=None):
    pass
