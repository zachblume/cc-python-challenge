# Solution thoughts
Instructions: you can run the unit tests in the same below method, and you can run searches with:

python3 src/main.py model COMMODITY SCOPE ...

The scope interpretation is generic, so:
model Zinc 'North America'
model Zinc North America
...both work!

My solution approach was pretty simple:
-in tests/domain/test_model.py
You'll find two new unit tests

-in src/controllers/model_controller.py
You'll find (1) a refactored search method, (2) a scoped_search() submethod to increase readability

-in src/domain/model_repository.py
You'll find a new method, find_by_scope_and_commodity()

-in src/domain/model.py
You'll find a method is_for_given_scope_and_commodity()

In essence, this (first) approach minimizes changes to the overall application structure and codebase and potential edge cases.

(1) The updated search() method delegates a search for a scoped match to a submethod. If none is returned, a global match proceeds normally.
(2) The scoped_search() method moves through the asset repository and checks for scope string matches. 
(3) It then moves through the scope hierarchy for that match (from name to country to continent) and returns the first (most specific) matching models.
(4) If there isn't a match for each asset-scope_level combination, it percolates outwards until hitting global where it returns None and triggers the normal global search in search()

This is a quick working solution. My next steps would be:
-To write end2end tests instead of unit tests for further development changes
-To hash the scopes as an index and persist that to prevent the O(n)+ looping that it going on in this solution right now
-Add a file or db cache so each instantiation of the CLI doesn't generate the repositories and indexes at runtime


# Software Engineer: Take home coding challenge

Carbon Chain is building a simple application to search its database of emission models. Attached is our first pass on
the implementation. It contains the basic application infrastructure, a controller and domain entities with initial
business logic, and a series of unit tests that document and test the intended behaviour.

The current functionality supports a simple use case???to find the global emission intensity for a given commodity. For
example, to find the emission intensity for Copper, one can run the application with `model search Copper` and get a 
response `Global emission intensity for Copper is   13.4`.

## Terminology

- **Model** (or emission intensity model) is an entity that provides the emission intensity for producing a given
  commodity.
- **Asset** is the facility that is involved in the production of a commodity, e.g. a mine, smelter, refinery, etc.
- **Model scope** defines the area for which a model provides emission intensity, e.g. if the scope of a model is
  `India`then the emission intensity is related to India only. If a scope is `None` then that is the commodity's global
  emission intensity model.

## Your Task

Your task is to extend the existing functionality. We would like to be able to pass the asset name and find a model with
the smallest available scope for the given commodity (instead of always returning the global model).

So, for example, with the input `models search Copper Khetri`, the application should return `India emission intensity for
Copper is 18.223`. However, for `models search Zinc Tara` (an Irish copper mine) the application should return `Global emission intensity for
Zinc is 5.33` because we do not have a model with `Ireland` or `Europe` scope in the database.

A couple of things to keep in mind
- you don't have to provide a complete solution, though please submit any thoughts and assumptions that will help us
  understand how you approach the problem
- you shouldn't spend more than 2 hours on the solution ??? the main objective here is for you to get familiar with the
  codebase so that we can discuss further improvements to it in the following technical interview 
- while this is a toy application, it suggests the kind of problems we have to solve for in real life ??? your approach
  should be justifiable in a production context

## Submitting the solution

Submit your solution compressed in a zip file that includes the source code and a README with your assumptions and any
relevant instructions. Name the zip file "coding-challenge-solution.zip" and upload it as instructed in the email.

## Running the application

The simplest way to run the application is by using your local python3 installation:

```shell
python3 src/main.py model search Copper
```

Similarly, to run the included unit tests enter:

```shell
python3 -m unittest discover tests
```

### Using Docker image

If you don't have python3 installed locally (and don't want to install it), you may run the application using a
python-ready Docker image:

```shell
docker run --rm -it \
  --workdir /srv \
  --volume $(pwd):/srv \
  python:3 \
  python3 src/main.py model search Copper
```

And for the tests:

```shell
docker run --rm -it \
  --workdir /srv \
  --volume $(pwd):/srv \
  python:3 \
  python3 -m unittest discover tests
```
