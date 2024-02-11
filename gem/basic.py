"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

import google.generativeai as genai

genai.configure(api_key="AIzaSyCdU5Lt7WN-SrF3Rpx0OX4FDCF5PKhJxD4")

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
    "Create Json of flight data based on a sentence. Fields should include \"departure_airport\", \"arrival_airport\", \"departure_date\",\"arrival_date\". Date should be formatted as MM/DD/YYYY.\n",
    ]

    line = data
    prompt_parts += line 
    try:
        response = model.generate_content(prompt_parts)
    except Exception as e:
            print(e)
            return 'Failed to generate flight details'

    flights_details = response.text
    
    return flights_details