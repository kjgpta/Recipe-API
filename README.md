# Recipe API

Welcome to the Recipe API repository. This API allows users to generate five unique recipes based on a combination of specified ingredients, cuisines, dietary restrictions, and nutritional preferences. Whether you are looking for a high-protein vegetarian meal or a specific cuisine-based dish, this API can help you discover new and exciting recipes tailored to your needs.

## Features

- Personalized Recipe Generation: Users can input specific ingredients, dietary restrictions, cuisines, and nutritional preferences to receive customized recipes.
- Supports Various Cuisines: Whether you enjoy Italian, Mexican, Asian, or other global cuisines, the API provides diverse recipe options.
- Dietary Restrictions Considered: The API accommodates various dietary needs, including vegetarian, vegan, gluten-free, and more.
- Nutritional Preferences: Users can request high-protein, low-carb, or other nutritionally tailored recipes.
- Detailed Recipe Information: Each response includes a recipe title, description, estimated cooking time, servings, ingredients list, and step-by-step cooking instructions.
- Ease of Use: Simple JSON-based request and response structure for easy integration into other applications.

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

The API responds with an array of recipe objects. Each object contains:

- `Id` (integer): Unique identifier for the recipe.
- `title` (string): Name of the recipe.
- `description` (string): Brief description of the recipe.
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

## Postman Collection Access

For access to the Postman collection, please send an email request to [mailguptakshitij@gmail.com](mailto:mailguptakshitij@gmail.com).

## License

This project is licensed under the Apache-2.0 license. See the [LICENSE](LICENSE) file for details.
