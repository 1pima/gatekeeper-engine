from concurrent import futures

import grpc
from flask import Flask

# $ make generate
import contracts.vault.v1.token_service_pb2_grpc as token_grpc
import contracts.processing.v1.transaction_service_pb2_grpc as tx_grpc
from config.settings import settings


def _setup():
    # DB
    from internal.models import base
    base.configure(settings.DB_DSN, settings.DB_POOL_SIZE, settings.DB_MAX_OVERFLOW)

    # HASHICORP
    from internal.util import vault
    vault.configure(settings.HVAC_URL, settings.HVAC_TOKEN, settings.HVAC_MASTER_KEY, settings.HMAC_KEY)


def new_grpc() -> grpc.Server:
    _setup()

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=settings.GRPC_MAX_WORKERS),
        options=[('grpc.max_concurrent_streams', settings.GRPC_MAX_CONCURRENT_STREAMS)]
    )

    # Сервис обработки токенов
    from internal.transport.grpc.token_servicer import TokenServicer
    token_grpc.add_TokenServiceServicer_to_server(
        TokenServicer(), server
    )

    # Сервис обработки транзакций
    from internal.transport.grpc.transaction_servicer import TransactionServicer
    tx_grpc.add_TransactionServiceServicer_to_server(
        TransactionServicer(), server
    )

    return server


def new_wsgi() -> Flask:
    _setup()

    app = Flask('gatekeeper')
    from config import flask_default
    app.config.from_object(flask_default)

    return app
