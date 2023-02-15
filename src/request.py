from typing import List


class Request:

    def __init__(self, params: List[str]):
        self.params = params

    def get(self, position: int) -> str:
        return self.params[position]
