import sys

from controllers.model_controller import ModelController
from core import Core
from domain.asset import Asset
from domain.asset_repository import AssetRepository
from domain.model import Model
from domain.model_repository import ModelRepository


def prepare_asset_repository() -> AssetRepository:
    return AssetRepository([
        Asset('Khetri', 'India', 'Asia'),
        Asset('Cerro Verde', 'Peru', 'South America'),
        Asset('El Abra', 'Chile', 'South America'),
        Asset('Red Dog', 'USA', 'North America'),
        Asset('Stamina', 'Peru', 'South America'),
        Asset('Tara', 'Ireland', 'Europe'),
    ])


def prepare_model_repository() -> ModelRepository:
    return ModelRepository([
        Model('Copper', None, 13.4),
        Model('Copper', 'India', 18.223),
        Model('Copper', 'Chile', 9.23),
        Model('Copper', 'South America', 11.12),
        Model('Zinc', None, 5.33),
        Model('Zinc', 'USA', 3.45),
        Model('Zinc', 'North America', 3.98),
        Model('Zinc', 'South America', 6.13),
    ])


if __name__ == '__main__':
    assert len(sys.argv) >= 4

    asset_repository = prepare_asset_repository()
    model_repository = prepare_model_repository()
    middlewares = {
        # 'model:search': [ModelSearchMiddleware(...)]
    }

    controllers = {
        'model': ModelController(asset_repository, model_repository)
    }

    core = Core(middlewares, controllers)
    out = core.run(sys.argv[1], sys.argv[2], sys.argv[3:])
    print(out)
