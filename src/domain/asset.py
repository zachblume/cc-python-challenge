class Asset:

    def __init__(self, name, country, continent):
        self.name = name
        self.country = country
        self.continent = continent

    def name_matches(self, term: str) -> bool:
        return self.name == term
