# library imports
from fastapi import FastAPI
from inference import get_recommended_recipes

# initialize fastapi app
app = FastAPI()

# define recommendation endpoint
@app.get("/search/{query}")
async def search(query: int):
    '''
    API endpoint for recommending recipes.

    Args:
        query (int): recipe id.
    
    Returns:
        dict: Dictionary containing the recommendations.
    '''

    # run the inference pipeline to get recommendations
    results = get_recommended_recipes([query])

    # return the results
    return results.to_dict(orient="records")