import logging

import grpc

from contracts.vault.v1 import token_service_pb2 as pb
from contracts.vault.v1 import token_service_pb2_grpc as pb_grpc
from internal.models.base import db_session
from internal.models.vault import TokenData

log = logging.getLogger(__name__)


class TokenServicer(pb_grpc.TokenServiceServicer):

    def GetTokenByHash(self, request: pb.GetTokenByHashRequest, context):  # noqa
        try:
            token = TokenData.query.filter(TokenData.hash==request.card_hash).one_or_none()
            if not token:
                context.abort(grpc.StatusCode.NOT_FOUND, f"card token {request.card_hash} not found")

            return pb.GetTokenByHashResponse(token_id=str(token.id))  # noqa
        except Exception as e:
            log.exception(e)
            context.abort(grpc.StatusCode.INTERNAL, f"internal error: {str(e)}")
        finally:
            db_session.remove()
