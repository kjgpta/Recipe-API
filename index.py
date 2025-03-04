import os, json
from openai import OpenAI
from typing import Optional, List
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Header, Body
from pydantic import BaseModel
from typing import List, ClassVar
from fastapi.middleware.cors import CORSMiddleware  # ✅ Required for CORS


load_dotenv()
# Initialize FastAPI app
app = FastAPI()

# ✅ Enable CORS to allow requests from any frontend (adjust if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Define authentication key (set this in your .env or deployment environment)
API_AUTH_KEY = os.getenv("API_AUTH_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Pydantic Model for Recipe Request
class RecipeRequest(BaseModel):
    vegetables: Optional[List[str]] = []
    cuisines: Optional[List[str]] = []
    dietaryRestrictions: Optional[List[str]] = []
    nutritionalPreferences: Optional[List[str]] = []

# Pydantic Model for Recipe Response
class SmartChefRecipe(BaseModel):
    Id: int
    title: str
    description: str
    cookTime: str
    servings: int
    ingredients: List[str]
    instructions: List[str]

    @classmethod
    def parse_list(cls, recipes_json: List[dict]) -> List["SmartChefRecipe"]:
        """
        Parses a list of dictionaries (JSON) into a list of SmartChefRecipe objects.
        """
        return [cls(**recipe) for recipe in recipes_json]

# Function to validate API key
def verify_api_key(api_key: str = Header(...)):
    if api_key != API_AUTH_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

# Function to parse the response
def parse_recipe_response(response):
    """
    Parses and validates the recipe returned by an OpenAI Chat Completion.
    Ensures the JSON structure matches the required format.
    Raises exceptions if the JSON is invalid or missing fields.
    """
    message = response.choices[0].message
    # Check if message.content is a string; if so, parse it as JSON.
    if isinstance(message.content, str):
        content = message.content.strip()
        # If the response is wrapped in a markdown code block (e.g., "```json ... ```"), remove those markers.
        if content.startswith("```"):
            lines = content.splitlines()
            # Remove the first line if it starts with ```
            if lines and lines[0].startswith("```"):
                lines = lines[1:]
            # Remove the last line if it is the closing ```
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            content = "\n".join(lines).strip()

        try:
            recipe_data = json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError("The response did not contain valid JSON.") from e
    else:
        # Assume the response is already a Python object, e.g. a list (JSON array)
        recipe_data = message.content

    # Ensure we always have a list (array of JSON objects)
    if isinstance(recipe_data, dict):  
        recipe_data = [recipe_data]  # Convert single object into a list

    if not isinstance(recipe_data, list):
        raise ValueError("Expected a JSON array of recipes, but got something else.")

    # Ensure all recipes have the required keys and valid types
    required_keys = ["Id", "title", "description", "cookTime", "servings", "ingredients", "instructions"]
    validated_recipes = []

    for recipe in recipe_data:
        # Check for missing keys
        missing_keys = [key for key in required_keys if key not in recipe]
        if missing_keys:
            raise ValueError(f"A recipe is missing required keys: {', '.join(missing_keys)}")

        # Validate types
        if not isinstance(recipe["Id"], int):
            raise ValueError("'Id' must be an integer.")
        if not isinstance(recipe["title"], str):
            raise ValueError("'title' must be a string.")
        if not isinstance(recipe["description"], str):
            raise ValueError("'description' must be a string.")
        if not isinstance(recipe["cookTime"], str):
            raise ValueError("'cookTime' must be a string (e.g., '30 minutes').")
        if not isinstance(recipe["servings"], (int, float)):
            raise ValueError("'servings' must be a numeric type (int or float).")
        if not isinstance(recipe["ingredients"], list) or not all(isinstance(i, str) for i in recipe["ingredients"]):
            raise ValueError("'ingredients' must be a list of strings.")
        if not isinstance(recipe["instructions"], list) or not all(isinstance(i, str) for i in recipe["instructions"]):
            raise ValueError("'instructions' must be a list of strings.")

        validated_recipes.append(recipe)

    # Optionally parse validated recipes into Pydantic model objects
    return SmartChefRecipe.parse_list(validated_recipes)

# Function to generate a recipe
def generate_recipe(preferences: RecipeRequest):
    if isinstance(preferences, dict):
        preferences = RecipeRequest(**preferences)
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        prompt = f"""
            You are an expert chef. Please create **five(5) distinct recipes** in strict compliance with the following user preferences:

            - **Available Vegetables**: {', '.join(preferences.vegetables)}
            - **Cuisine Preferences**: {', '.join(preferences.cuisines)}
            - **Dietary Restrictions**: {', '.join(preferences.dietaryRestrictions)}
            - **Nutritional Requirements**: {', '.join(preferences.nutritionalPreferences)}

            Return your answer as a **array of JSON objects** of exactly five(5) recipe objects, each with the exact structure below (no extra text outside the JSON). 
            Do not include extra commentary or formatting outside the JSON:
            [
                {{
                    "Id": 1,
                    "title": "Example Recipe Title",
                    "description": "A brief description of the dish.",
                    "cookTime": "30 minutes",
                    "servings": 4,
                    "ingredients": ["Ingredient 1", "Ingredient 2"],
                    "instructions": ["Step 1", "Step 2"],
                }},
                {{
                    "Id": 2,
                    "title": "Second Recipe",
                    "description": "Another delicious dish.",
                    "cookTime": "45 minutes",
                    "servings": 2,
                    "ingredients": ["Ingredient A", "Ingredient B"],
                    "instructions": ["Step 1", "Step 2"],
                }},
                {{
                    "Id": 3,
                    "title": "Third Recipe",
                    "description": "Yet another tasty dish.",
                    "cookTime": "25 minutes",
                    "servings": 3,
                    "ingredients": ["Ingredient X", "Ingredient Y"],
                    "instructions": ["Step 1", "Step 2"],
                }},
                {{
                    "Id": 4,
                    "title": "Fourth Recipe",
                    "description": "A different variation of flavors.",
                    "cookTime": "50 minutes",
                    "servings": 5,
                    "ingredients": ["Ingredient P", "Ingredient Q"],
                    "instructions": ["Step 1", "Step 2"],
                }},
                {{
                    "Id": 5,
                    "title": "Fifth Recipe",
                    "description": "A final delightful recipe.",
                    "cookTime": "60 minutes",
                    "servings": 6,
                    "ingredients": ["Ingredient M", "Ingredient N"],
                    "instructions": ["Step 1", "Step 2"],
                }}
            ]
            **Requirements**:
                1. Provide exactly five(5) recipes in total, no more no less.
                2. Strictly follow all dietary restrictions and nutritional preferences.
                3. Incorporate the specified vegetables whenever possible.
                4. Adhere to the indicated cuisine style, if provided.
                5. The recipe should be detailed, with clear instructions and accurate ingredient lists.
                6. Include a variety of cooking techniques and flavors to keep the recipes distinct.
                7. cookTime should be in the format "X minutes".
                8. Ensure that each recipe should have a unique Id (1-5).
                9. If some preferences are not specified, assume no restrictions or preferences in those categories.
                10. The recipes should be health-conscious and nutritionally balanced.
                11. Instructions should be clear and easy to follow, with precise cooking times and steps.
                12. Include suggested substitutions for any ingredients that may be hard to find.
                13. Include all the ingredients thoroughly and in the correct order of use.
                14. Aim to create delicious, gourmet-level meals that are visually appealing and satisfying.
                15. Ensure that all the infredients are present in the list
                16. Steps should be very detailed, ensuring no point of error.

            Generate only the **array of JSON objects** as described above, with **no additional commentary**.
            """
        
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {

                    "role": "system",
                    "content": "You are an expert chef who designs detailed, gourmet-level recipes that strictly adhere to any specified dietary restrictions and nutritional preferences. Each recipe you provide is meticulously crafted with clear ingredient lists, precise cooking instructions, timing, and suggested substitutions. Your goal is to create delicious, health-conscious meals without compromising on taste or presentation."
                }
                ,
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.6,
            frequency_penalty=0.1,
            presence_penalty=0.1,
            # response_format = SmartChefRecipe
        )
        output = response.choices[0].message

        if (output.refusal):
            print(output.refusal)
        else:
            recipe = parse_recipe_response(response)
            return recipe

    except ValueError as ve:
        # Handle JSON or validation errors
        print(f"Validation Error: {ve}")
        return None

    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return None

# API Endpoint for Generating Recipes
@app.post("/generate-recipe", response_model=List[SmartChefRecipe])
def generate_recipe_api(preferences: RecipeRequest, api_key: str = Depends(verify_api_key)):
    return generate_recipe(preferences)

@app.get("/")
def read_root():
    return {"message": "API is working!"}

# ✅ Run Uvicorn ASGI Server (Required for Vercel)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
