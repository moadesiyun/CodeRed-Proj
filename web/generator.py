import json
import google.generativeai as genai
import os

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]
def generate_details(data):
    model = genai.GenerativeModel(model_name="gemini-pro",
                                generation_config=generation_config,
                                safety_settings=safety_settings)

    prompt_parts = [
    "Create Json of flight data based on a sentence. Fields should include \"Origin\", \"Destination\", \"Departuredate\",\"Returndate\". Date should be formatted as YYYY/MM/DD.\n",
    ]

    line = data
    prompt_parts += line 
    try:
        response = model.generate_content(prompt_parts)
    except Exception as e:
            print(e)
            return 'Failed to generate flight details'

    flights_details = response.text
    firstValue = flights_details.index("{")
    lastValue = len(flights_details) - flights_details[::-1].index("}")
    jsonString = flights_details[firstValue:lastValue]
<<<<<<< HEAD
    res = json.loads(jsonString)
        
    return res
=======
        
    return jsonString
print(generate_details(data))
>>>>>>> a87188df7fa5f540b5e346379547434dcd0b2a00
