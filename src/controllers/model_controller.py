from controller import ControllerInterface
from domain.asset_repository import AssetRepository
from domain.model_repository import ModelRepository
from request import Request


class ModelController(ControllerInterface):

    def __init__(self, asset_repository: AssetRepository, model_repository: ModelRepository):
        self.asset_repository = asset_repository
        self.model_repository = model_repository

    def search(self, request: Request) -> str:
        commodity = request.get(0)

        model = self.model_repository.find_global_by_commodity(commodity)
        return f'Global emissions intensity for {commodity} is {model.emission_intensity}'
