"""
WhatsApp Business Catalog Manager
Manage your consulting services catalog via WhatsApp Cloud API
"""

import requests
import json
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class CatalogItem:
    """Represents a service in your catalog"""
    name: str
    description: str
    price: float  # in GBP
    currency: str = "GBP"
    image_url: Optional[str] = None
    availability: str = "in stock"  # for services, always "in stock"
    category: Optional[str] = None


class WhatsAppCatalogManager:
    """Manage WhatsApp Business Catalog via Cloud API"""
    
    def __init__(self, access_token: str, business_account_id: str):
        self.access_token = access_token
        self.business_account_id = business_account_id
        self.base_url = "https://graph.facebook.com/v18.0"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def create_catalog(self, catalog_name: str) -> Dict:
        """Create a new catalog"""
        url = f"{self.base_url}/{self.business_account_id}/owned_product_catalogs"
        data = {
            "name": catalog_name
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
    
    def add_product(self, catalog_id: str, item: CatalogItem) -> Dict:
        """Add a service to your catalog"""
        url = f"{self.base_url}/{catalog_id}/products"
        
        # Convert price to minor units (pence)
        price_in_pence = int(item.price * 100)
        
        data = {
            "name": item.name,
            "description": item.description,
            "price": price_in_pence,
            "currency": item.currency,
            "availability": item.availability,
            "retailer_id": item.name.lower().replace(" ", "_")  # unique ID
        }
        
        if item.image_url:
            data["image_url"] = item.image_url
        
        if item.category:
            data["category"] = item.category
        
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
    
    def update_product(self, product_id: str, updates: Dict) -> Dict:
        """Update an existing product"""
        url = f"{self.base_url}/{product_id}"
        
        # Convert price to minor units if present
        if "price" in updates:
            updates["price"] = int(updates["price"] * 100)
        
        response = requests.post(url, headers=self.headers, json=updates)
        return response.json()
    
    def delete_product(self, product_id: str) -> Dict:
        """Remove a product from catalog"""
        url = f"{self.base_url}/{product_id}"
        response = requests.delete(url, headers=self.headers)
        return response.json()
    
    def list_products(self, catalog_id: str) -> List[Dict]:
        """List all products in catalog"""
        url = f"{self.base_url}/{catalog_id}/products"
        response = requests.get(url, headers=self.headers)
        return response.json().get("data", [])
    
    def send_catalog_message(self, phone_number_id: str, to: str, 
                            body_text: str, catalog_id: str) -> Dict:
        """Send a message with your catalog"""
        url = f"{self.base_url}/{phone_number_id}/messages"
        
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "catalog_message",
                "body": {
                    "text": body_text
                },
                "action": {
                    "name": "catalog_message",
                    "parameters": {
                        "thumbnail_product_retailer_id": "discovery_call"  # Featured item
                    }
                }
            }
        }
        
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()


# Example: Setup your consulting services catalog
def setup_consulting_catalog(manager: WhatsAppCatalogManager, catalog_id: str):
    """Setup your specific consulting services"""
    
    services = [
        # Discovery & Consultation
        CatalogItem(
            name="Discovery Call",
            description="Free 30-minute discovery call to discuss your needs and how I can help with ML/AI, cloud adoption, or automation.",
            price=0.00,
            category="Discovery & Consultation"
        ),
        CatalogItem(
            name="Initial Consultation",
            description="1-2 hour deep-dive consultation. Includes: detailed discussion of your challenges, preliminary recommendations, and follow-up action plan via email.",
            price=250.00,
            category="Discovery & Consultation"
        ),
        
        # Strategy Sessions
        CatalogItem(
            name="Half-Day Strategy Session",
            description="4-hour intensive strategy or business coaching session. Perfect for: Cloud adoption planning, ML/AI strategy, technology integration roadmaps, or business automation planning. Includes: session documentation and 30-day email support.",
            price=1000.00,
            category="Strategy Sessions"
        ),
        
        # Retainer Packages
        CatalogItem(
            name="Bronze Retainer",
            description="1 day per week dedicated support. Ideal for: ongoing ML/AI projects, continuous integration work, or regular business coaching. Flexible scheduling.",
            price=2000.00,
            category="Retainer Packages"
        ),
        CatalogItem(
            name="Silver Retainer",
            description="2 days per week dedicated support. Perfect for: major cloud migrations, complex ML implementations, or comprehensive platform integrations. Priority scheduling.",
            price=4000.00,
            category="Retainer Packages"
        ),
        CatalogItem(
            name="Gold Retainer",
            description="3 days per week dedicated support. For: large-scale transformations, enterprise AI implementations, or serving as interim CTO/Tech Lead. Highest priority scheduling and 24/7 emergency support.",
            price=6000.00,
            category="Retainer Packages"
        ),
    ]
    
    results = []
    for service in services:
        result = manager.add_product(catalog_id, service)
        results.append(result)
        print(f"Added: {service.name} - £{service.price}")
    
    return results


# Usage Example
if __name__ == "__main__":
    # Configure your credentials
    ACCESS_TOKEN = "EAAKIcdZASr8oBP8NJTsPhbUZCzJhbVLSAkpd7ScpVgWBeNx7tVNLipbjVUvZBszxZAgSzxA8VLygiduGkKT7zaPLG1QYqZAZCwYW3xt7yVs0sbQZA4W6ZCgZCl1kVqv9uJ7BMnddqdiW0rLSmjAMT3UfOZA2lLmp611kuBRO98YiS7NdjZA6cfobnZC7Q6o4auMRZCxAa7LBvSFkyRvEk2YGFoztT7TefyuwUzNo52vqkYLjxye4qcZAeJV0eMDbtbddArzaZCZBd8Dh6OVuI4HCeWMjK2efKKZCHVTD0mYJJyP9n3ZBYZD"
    BUSINESS_ACCOUNT_ID = "687022837460479"
    PHONE_NUMBER_ID = "856886180841184"  # Your WhatsApp Business Phone Number ID
    
    # Initialize manager
    manager = WhatsAppCatalogManager(ACCESS_TOKEN, BUSINESS_ACCOUNT_ID)
    
    # Create catalog
    catalog_response = manager.create_catalog("Consulting Services Catalog")
    catalog_id = catalog_response.get("id")
    print(f"Created catalog: {catalog_id}")
    
    # Setup your services
    setup_consulting_catalog(manager, catalog_id)
    
    
    # Send catalog to a client (example)
    manager.send_catalog_message(
        phone_number_id=PHONE_NUMBER_ID,
        to="447496727058",  # Client's number with country code
        body_text="Here are my consulting services. Let me know what interests you!",
        catalog_id=catalog_id
    )