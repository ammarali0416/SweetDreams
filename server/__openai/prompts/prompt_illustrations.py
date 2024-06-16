guidelines: str = """You are tasked with generating consistent stylistic guidelines for illustrations that will be used throughout a PDF book. Below is the information provided about the overall illustrative style and the main characters:

- Illustrative Style: <Illustrative Style>
- Main Characters: <JSON list of main characters?

Create standardized descriptions and visual styles for each main character in a way that matches the overall illustrative style. Ensure that the descriptions are detailed enough for DALL·E to generate images that are consistent and cohesive throughout the book. Provide the standardized styles in a JSON format.

Example output:

{
  "overall_style": "Watercolor",
  "characters": [
    {
      "name": "Alice",
      "style": "A young girl with blonde hair, depicted in a soft watercolor style, wearing a blue dress with a white apron."
    },
    {
      "name": "The White Rabbit",
      "style": "A rabbit in a watercolor style, with a waistcoat and a pocket watch, emphasizing a whimsical and vintage appearance."
    }
  ]
}"""

chapters_images: str = """Your task is to generate a DALL·E prompt for creating an illustration for a specific chapter of a book. The illustration must align with the overall illustrative style, character styles, and the chapter plot provided. Use the chapter plot in conjunction with the other context details to create a cohesive and relevant illustration. Only describe characters if they are part of the chapter illustration idea, and provide detailed descriptions of these characters' appearances and the overall illustrative style to ensure consistency throughout the book.

- Overall Illustrative Style: {Overall Illustrative Style}
- Character Styles: {Character Styles}
- Chapter Illustration Guidelines: {Chapter Illustration Guidelines}
- Chapter Plot: {Chapter Plot}

Create a detailed DALL·E prompt that describes the illustration to be generated. Ensure the prompt clearly conveys the scene, incorporates the chapter plot and chapter illustration guideline, includes only the relevant characters, and describes their appearances in detail according to the specified style. The description should help maintain visual coherence across all images in the book.

Example output:

"Create a watercolor illustration of Alice in an enchanted forest. The scene should feature Alice, wearing a blue dress with a white apron, depicted in a watercolor style. She should be meeting the Cheshire Cat, who has a wide grin and is perched on a tree branch. The illustration should reflect the whimsical and vibrant elements of the enchanted forest as described in the chapter plot, where Alice first encounters the magical creatures. No other characters should be included in this scene."
"""

cover: str = """You need to generate a DALL·E prompt for creating a book cover illustration for a PDF book. The cover should reflect the overall illustrative style and feature the main characters, capturing the essence of the book's plot.

- Overall Illustrative Style: {Overall Illustrative Style}
- Character Styles: {Character Styles}
- Book Plot: {Book Plot}

Craft a detailed DALL·E prompt for the book cover, ensuring it incorporates key visual elements that represent the book's theme and main characters. Only include characters who are significant to the book's plot and provide detailed descriptions of their appearances to ensure consistency with the overall illustrative style. The cover should be eye-catching and convey the magical and whimsical nature of the story.

Example output:

"DALL·E, create a watercolor book cover for 'Alice's Adventures'. The cover should feature Alice, wearing a blue dress with a white apron, standing at the edge of a magical forest. She should be depicted in a whimsical and vibrant watercolor style. Include the White Rabbit, wearing a waistcoat and holding a pocket watch, standing near Alice. In the background, add a subtle hint of the Cheshire Cat's smile among the tree branches. The illustration should capture the enchanting and adventurous spirit of the story."
"""