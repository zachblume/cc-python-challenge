from controller import ControllerInterface
from domain.asset_repository import AssetRepository
from domain.model_repository import ModelRepository
from request import Request


class ModelController(ControllerInterface):

    def __init__(self, asset_repository: AssetRepository, model_repository: ModelRepository):
        self.asset_repository = asset_repository
        self.model_repository = model_repository

    def search(self, request: Request) -> str:
        """
        This method executes the scoped_search method if it was passed as a scope argument,
        and otherwise returns a global search (it also returns a global match if there is no scope match)
        """
        commodity = request.get(0)
        search_scope = "Global"
        model = False

        # If there is scope, and it's discoverable, return a scoped answer
        if (len(request.params) > 1):
            # Get the specified search scope
            search_scope = ""
            # This rebuilds the space-concatenated string
            # from the request in case of searches like "model search South America"
            # where South America is really a single param
            for i in range(1, len(request.params)):
                if i > 1:
                    search_scope += " "
                search_scope += request.get(i)

            # Find any possible scoped match
            scoped_answer = self.scoped_search(
                search_scope, commodity)

            # If there is one...
            if scoped_answer:
                # Destructure the answer
                temp_model, scope_match = answer

                # Replace the model for answer
                model = temp_model

                # Defined the scope for the answer
                answer_scope = scope_match

        # If there is no scope, or the scope is undiscoverable and model was never updated,
        # return the global answer
        if not model:
            answer_scope = "Global"
            model = self.model_repository.find_global_by_commodity(commodity)

        return f'{answer_scope} emissions intensity for {commodity} is {model.emission_intensity}'

    def scoped_search(self, search_scope, commodity):
        """
        This method moves through the asset repository and checks for scope matches. 
        It then moves through the scope hierarchy for that match and returns the first (most specific) matching models.
        If there isn't a match for that asset-scope_level combination, it percolates outwards until hitting global where it returns None
        """

        # Initialize a list with falsy values of same length as possible scopes
        matches = [None] * 3

        # Iterate through assets to find matching assets
        for asset in self.asset_repository.assets:
            # Define the scopes in a hierarchy by
            # indexing their scope category names in an array
            scopes = [asset.name, asset.country, asset.continent]
            # Iterate through the three scopes to find a match
            for match_level, scope in enumerate(scopes):
                # If the named scope matches our search scope
                if scope == search_scope:
                    # Hash the match
                    matches[match_level] = scopes
                    # We're hashing it because perhaps there's an edge case
                    # where multiple asset strings match the search string
                    # and we're looking for the most specific one (i.e., min(match_min))
                    # or where a certain asset hierarchy match doesn't produce a model match

        # Iterate through matches by hierarchy level
        # (starting at specific and moving to global)
        for match_level, scopes in enumerate(matches):
            # And for every valid match...
            if scopes != None:
                # Do a model search
                # starting at match_level and moving to end
                for scope_level in range(match_level, len(scopes)):
                    scope = scopes[scope_level]
                    temp_model = self.model_repository.find_by_scope_and_commodity(
                        scope, scope_level, commodity)
                    if (temp_model):
                        return temp_model, scope

        return None
