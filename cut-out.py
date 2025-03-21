import re
import json
import os
from urllib.parse import urlparse
# from functions import get_html  # Uncomment if needed

def create_filename(url):
    path = urlparse(url).path
    segments = [s for s in path.split('/') if s]
    filename = segments[-1] if segments else 'default'
    filename = re.sub(r'[^\w\-]', '_', filename)
    return f"{filename}.json"

def extract_product_info(html_content):
    image_pattern = re.compile(r'<div class="card-product__item">.*?<img.*?src="(.*?)".*?>.*?</div>', re.DOTALL)
    description_pattern = re.compile(r'<div class="full--content">.*?<p>.*?</p>.*?<p>(.*?)</p>.*?</div>', re.DOTALL)
    characteristics_pattern = re.compile(r'<div class="mini-tbl__cols">.*?<p>(.*?)</p>.*?<p>(.*?)</p>.*?</div>', re.DOTALL)

    image_match = image_pattern.search(html_content)
    description_match = description_pattern.search(html_content)
    characteristics_matches = characteristics_pattern.findall(html_content)

    image_url = "https://piano.by" + image_match.group(1).strip() if image_match else None

    if description_match:
        description = description_match.group(1).strip()
        description = re.sub(r'<.*?>', '', description)
        description = re.sub(r'\s+', ' ', description)
    else:
        description = "No description found."

    characteristics_dict = {}
    for match in characteristics_matches:
        key = re.sub(r'<.*?>', '', match[0].strip())
        value = re.sub(r'<.*?>', '', match[1].strip())
        characteristics_dict[key] = value

    return image_url, description, characteristics_dict

def run_script(url):
    #url = str(input("Enter url to get description from (Piano.by only) ~> "))
    os.makedirs("./Data", exist_ok=True)

    with open("./HTML/parsed.html", 'r') as file:
        html_content = file.read()

    image_url, description, characteristics_dict = extract_product_info(html_content)

    product_info = {
        "url": url,
        "description": description,
        "characteristics": characteristics_dict,
        "image": image_url
    }

    # Save to JSON
    filename = create_filename(url)
    filepath = os.path.join("./Data", filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(product_info, file, ensure_ascii=False, indent=4)

    print(f"\nData has been saved to: {filepath}")
    print("\nSaved content:")
    print(json.dumps(product_info, ensure_ascii=False, indent=4))

    # Save to text file
    with open("./Data/parsed.txt", 'w', encoding='utf-8') as file:
        file.write(product_info["description"])
        file.write("\nCharacteristics:\n")
        for key, value in product_info["characteristics"].items():
            file.write(f"{key}: {value}\n")
        file.write("Image link: ")
        file.write(product_info["image"] if product_info["image"] else "No image found.")


