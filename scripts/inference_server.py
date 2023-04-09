# library imports
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from inference import get_recommended_recipes
import json

# initialize fastapi app
app = FastAPI()

# load the api key from config.json
config = json.load(open("../config.json"))
api_key = config["api-key"]

# define middleware for authentication
@app.middleware("http")
async def authentication(request: Request, call_next):
    '''
    Middleware for authentication.
    Args:
        request (Request): Request object.
        call_next (function): Function to call next.
    Returns:
        JSONResponse: JSON response object.
    '''
    if request.headers.get('api-key') == api_key:
        response = await call_next(request)

    else:
        response = JSONResponse(
            content={"message": "unauthorized access"}, status_code=401
        )
    return response

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