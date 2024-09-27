import json
import os
import requests
import random
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


PINATA_API_KEY = os.getenv('PINATA_API_KEY')
PINATA_SECRET_API_KEY = os.getenv('PINATA_SECRET_API_KEY')


PINATA_BASE_URL = 'https://api.pinata.cloud/pinning/pinFileToIPFS'


CLOTHES_OPTIONS = ["Jacket", "Suit", "Military", "Empty"]
CLOTHES_WEIGHTS = [45, 25, 10, 20]

HAIR_OPTIONS = ["Fade", "Mohawk", "Box", "Empty"]
HAIR_WEIGHTS = [30, 25, 35, 10]

BOOTS_OPTIONS = ["Nike", "Adidas", "New Balance", "Empty"]
BOOTS_WEIGHTS = [40, 20, 10, 30]


def generate_attributes(token_id):
    clothes = random.choices(CLOTHES_OPTIONS, CLOTHES_WEIGHTS, k=1)[0]
    hair = random.choices(HAIR_OPTIONS, HAIR_WEIGHTS, k=1)[0]
    boots = random.choices(BOOTS_OPTIONS, BOOTS_WEIGHTS, k=1)[0]
    

    attributes = {
        "name": f"NFT #{token_id}",
        "description": f"This is NFT #{token_id} from MyNFTCollection.",
        "image": f"https://ipfs.io/ipfs/Qmb8Guy7sL3i3GWKxaP62m98r8FgMQYoxnpapTmotCDzu1/bear-{token_id:04d}.png",
        "attributes": [
            {
                "trait_type": "Clothes",
                "value": clothes
            },
            {
                "trait_type": "Hair",
                "value": hair
            },
            {
                "trait_type": "Boots",
                "value": boots
            }
        ]
    }
    return attributes


def upload_to_pinata(json_data, token_id):
    if not os.path.exists('metadata'):
        os.makedirs('metadata')
    
    json_filename = f'metadata/{token_id}.json'
    
    with open(json_filename, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    with open(json_filename, 'rb') as file:
        response = requests.post(
            PINATA_BASE_URL,
            files={'file': (json_filename, file)},
            headers={
                'pinata_api_key': PINATA_API_KEY,
                'pinata_secret_api_key': PINATA_SECRET_API_KEY
            }
        )

    if response.status_code == 200:
        print(f"Successfully uploaded {json_filename} to IPFS!")
        ipfs_hash = response.json()['IpfsHash']
        return f"ipfs://{ipfs_hash}"
    else:
        print(f"Failed to upload {json_filename}: {response.text}")
        return None


def create_and_upload_metadata(token_id):
    attributes = generate_attributes(token_id)
    
    ipfs_url = upload_to_pinata(attributes, token_id)
    if ipfs_url:
        print(f"Metadata for token #{token_id} uploaded: {ipfs_url}")
    return ipfs_url


for token_id in range(100):
    create_and_upload_metadata(token_id)
