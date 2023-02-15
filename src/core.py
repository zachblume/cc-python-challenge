from typing import Dict, List

from controller import ControllerInterface
from exceptions import ApplicationException
from middleware import MiddlewareInterface
from request import Request


class Core:

    def __init__(self, middlewares: Dict[str, List[MiddlewareInterface]], controllers: Dict[str, ControllerInterface]):
        self.middlewares = middlewares
        self.controllers = controllers

    def run(self, path: str, endpoint: str, params: List[str]):
        try:
            request = self._apply_middleware(path, endpoint, Request(params))
            return self._dispatch_controller(path, endpoint, request)
        except ApplicationException as e:
            return f'Problem when processing request: {e.message}'

    def _apply_middleware(self, path: str, endpoint: str, request: Request):
        key = f'{path.lower()}:{endpoint.lower()}'
        endpoint_middlewares: List[MiddlewareInterface] = self.middlewares.get(key)
        if endpoint_middlewares is None:
            return request

        for middleware in endpoint_middlewares:
            request = middleware.handle(request)
        return request

    def _dispatch_controller(self, path: str, endpoint: str, request: Request):
        controller = self.controllers.get(path)

        if controller is None:
            raise Exception(f'Path {path} has no matching controller')

        return self._invoke_endpoint(endpoint, controller, request)

    def _invoke_endpoint(self, endpoint: str, controller: ControllerInterface, request: Request) -> str:
        endpoint_method = controller.__getattribute__(endpoint)
        if endpoint_method is None or not callable(endpoint_method):
            raise ApplicationException(f'Endpoint {endpoint} does not exist on controller {controller.__class__}')

        return endpoint_method(request)
