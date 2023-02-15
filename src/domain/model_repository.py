from typing import List, Optional

from domain.model import Model


class ModelRepository:

    def __init__(self, models: List[Model]):
        self.models = models

    def find_global_by_commodity(self, commodity: str) -> Optional[Model]:
        for model in self.models:
            if model.is_global_for_commodity(commodity):
                return model
        return None

    def find_by_scope_and_commodity(self, scope: str, scope_level: int, commodity: str) -> Optional[Model]:
        for model in self.models:
            if model.is_for_given_scope_and_commodity(scope, scope_level, commodity):
                return model
        return None
