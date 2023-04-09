# library imports
from fastapi import FastAPI
from inference import get_recommended_recipes
# initialize fastapi app
app = FastAPI()

# define search endpoint
@app.get("/search/{query}")
async def search(query: int):
    '''
    Search endpoint for recommending recipes.
    Args:
        query (str): Query string.
    Returns:
        dict: Dictionary containing search results.
    '''

    # run qna pipeline on reddit posts
    results = get_recommended_recipes([query])

    # return search results
    return results.to_dict(orient="records")
