from google import genai
from google.genai import types
import requests

def analyze_file(screenshot_file):
    with open(screenshot_file, 'rb') as f:
        image_bytes = f.read()

    client = genai.Client()
    response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=[
        types.Part.from_bytes(
        data=image_bytes,
        mime_type='image/jpeg',
        ),
        'Describe this screenshot of a website.'
    ]
    )

    print(response.text)

def analyze_url(image_path):
    image_bytes = requests.get(image_path, verify=False).content
    image = types.Part.from_bytes(
    data=image_bytes, mime_type="image/png"
    )

    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=["Describe this screenshot of a website.", image],
    )

    print(response.text)

if __name__ == "__main__":
    #analyze_file("screenshots/019a4616-2094-740e-8287-08f645e1278d.png")
    analyze_url("https://urlscan.io/screenshots/019a4616-2094-740e-8287-08f645e1278d.png")
