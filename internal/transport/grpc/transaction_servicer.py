import logging

import grpc

from contracts.processing.v1 import transaction_service_pb2 as pb
from contracts.processing.v1 import transaction_service_pb2_grpc as pb_grpc
from internal.models.base import db_session
from internal.models.processing import Transaction


log = logging.getLogger(__name__)


class TransactionServicer(pb_grpc.TransactionServiceServicer):

    def CreateTransaction(self, request: pb.CreateTransactionRequest, context): # noqa
        try:
            transaction = Transaction.create(
                reference=request.reference,
                ext_id=request.ext_id,
                tr_type=request.tr_type,
                transaction_amount=request.transaction_amount.amount,
                transaction_currency=request.transaction_amount.currency_code,
                settlement_amount=request.settlement_amount.amount,
                settlement_currency=request.settlement_currency.currency_code,
                token_id=request.token_id,
                mcc_id=request.mcc_id,
                bank_data=request.bank_data
            )
            return pb.CreateTransactionResponse(transaction_id=str(transaction.id)) # noqa
        except Exception as e:
            log.exception(e)
            context.abort(grpc.StatusCode.INTERNAL, f"internal error: {str(e)}")
        finally:
            db_session.remove()

    def AuthorizeTransaction(self, request: pb.AuthorizeTransactionRequest, context): # noqa
        try:
            transaction = Transaction.query.filter(Transaction.id==request.transaction_id).one_or_none()
            if not transaction:
                log.warning(f'transaction {request.transaction_id} not found')
                context.abort(grpc.StatusCode.NOT_FOUND, f"transaction {request.transaction_id} not found")

            # todo тут логика лимитов и другая валидация транзакции

            transaction.authorize('00', 'Approved')
            return pb.AuthorizeTransactionResponse(mps_code='00', mps_message='Approved') # noqa
        except Exception as e:
            log.exception(e)
            context.abort(grpc.StatusCode.INTERNAL, f"internal error: {str(e)}")
        finally:
            db_session.remove()
