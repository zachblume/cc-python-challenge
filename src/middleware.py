from request import Request


class MiddlewareInterface:

    def handle(self, request: Request) -> Request:
        pass
