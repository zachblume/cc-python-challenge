from typing import Optional


class Model:

    def __init__(self, commodity: str, scope: Optional[str], emission_intensity: float):
        self.commodity = commodity
        self.scope = scope
        self.emission_intensity = emission_intensity

    def is_global_for_commodity(self, commodity: str) -> bool:
        return self.commodity == commodity and self.scope is None

    def get_emission_intensity(self) -> float:
        return self.emission_intensity
