# Recipe API

Welcome to the Recipe API repository. This API harnesses the power of GPT-based artificial intelligence to generate five unique and highly customized recipes based on specified ingredients, cuisines, dietary restrictions, and nutritional preferences. Whether you're in search of a high-protein vegetarian dish or a specific cuisine-inspired meal, this API provides innovative and tailored recipe suggestions using cutting-edge AI technology.

## Features

- **AI-Driven Recipe Generation:** Powered by GPT, the API analyzes user input and intelligently crafts unique, flavorful, and well-balanced recipes.
- **Personalized Recommendations:** Users can input specific ingredients, dietary restrictions, cuisines, and nutritional preferences to receive tailored recipes.
- **Supports Various Cuisines:** Whether you enjoy Italian, Mexican, Asian, or other global cuisines, the API provides diverse and authentic recipe options.
- **Dietary Adaptability:** The AI ensures that recipes align with dietary needs, including vegetarian, vegan, gluten-free, and more.
- **Nutritional Customization:** Users can request high-protein, low-carb, or other nutritionally optimized recipes tailored to their health goals.
- **Comprehensive Recipe Details:** Each response includes a recipe title, description, estimated cooking time, servings, ingredient list, and step-by-step cooking instructions.
- **Seamless Integration:** With a simple JSON-based request and response structure, the API can be easily incorporated into applications, meal planners, and research projects.

## Usage

### Input Payload

To request recipes, send a JSON payload with the following structure:

```json
{
  "vegetables": ["carrot", "spinach"],
  "cuisines": ["Italian"],
  "dietaryRestrictions": ["vegetarian"],
  "nutritionalPreferences": ["High Protein"]
}
```

**Parameters:**

- `vegetables` (array of strings): List of vegetables to include in the recipes.
- `cuisines` (array of strings): Desired cuisines for the recipes.
- `dietaryRestrictions` (array of strings): Any dietary restrictions to consider.
- `nutritionalPreferences` (array of strings): Nutritional preferences for the recipes.

### Output Response

The API responds with an array of AI-generated recipe objects. Each object contains:

- `Id` (integer): Unique identifier for the recipe.
- `title` (string): Name of the recipe.
- `description` (string): AI-generated brief description of the recipe.
- `cookTime` (string): Estimated cooking time.
- `servings` (integer): Number of servings.
- `ingredients` (array of strings): List of ingredients required.
- `instructions` (array of strings): Step-by-step cooking instructions.

**Example Response:**

```json
[
  {
    "Id": 1,
    "title": "Spinach and Ricotta Stuffed Shells",
    "description": "Classic Italian stuffed pasta shells with creamy ricotta and spinach, elevated with a high-protein twist.",
    "cookTime": "45 minutes",
    "servings": 4,
    "ingredients": [
      "20 jumbo pasta shells",
      "2 cups fresh spinach, chopped",
      "1 cup ricotta cheese",
      "1/2 cup grated Parmesan cheese",
      "1/2 cup cooked lentils",
      "1/2 teaspoon nutmeg",
      "Salt and pepper to taste",
      "2 cups marinara sauce",
      "1 cup shredded mozzarella cheese"
    ],
    "instructions": [
      "Preheat oven to 375°F (190°C).",
      "Cook the pasta shells according to package instructions; drain and set aside.",
      "In a large bowl, combine spinach, ricotta, Parmesan, lentils, nutmeg, salt, and pepper. Mix well.",
      "Stuff each pasta shell with the ricotta mixture.",
      "Spread 1 cup of marinara sauce in the bottom of a baking dish.",
      "Arrange stuffed shells over the sauce and cover with remaining marinara sauce.",
      "Sprinkle mozzarella cheese on top.",
      "Cover with foil and bake for 20 minutes. Remove foil and bake for an additional 10 minutes until bubbly.",
      "Serve hot."
    ]
  }
... 
]
```

## Access

For access to the Postman collection and API, please send an email request to [mailguptakshitij@gmail.com](mailto:mailguptakshitij@gmail.com).

## License

This project is licensed under the Apache-2.0 license. See the [LICENSE](LICENSE) file for details.

