from typing import List, Optional

from domain.asset import Asset


class AssetRepository:

    def __init__(self, assets: List[Asset]):
        self.assets = assets

    def find_by_name(self, name: str) -> Optional[Asset]:
        for asset in self.assets:
            if asset.name_matches(name):
                return asset
        return None
