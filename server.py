from config.settings import settings
from internal.factory import new_grpc


def serve():
    server = new_grpc()
    server.add_insecure_port(f'[::]:{settings.GRPC_PORT}')
    server.start()

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(grace=5)


if __name__ == '__main__':
    serve()
