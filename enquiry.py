"""
WhatsApp Business Inquiry Handler
Automate responses to common inquiries and manage bookings
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, Optional
import re

class WhatsAppMessenger:
    """Handle incoming and outgoing WhatsApp messages"""
    
    def __init__(self, access_token: str, phone_number_id: str):
        self.access_token = access_token
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v24.0"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
    def send_text_message(self, to: str, message: str) -> Dict:
        """Send a simple text message"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
    
    def send_template_message(self, to: str, template_name: str, 
                            language_code: str = "en") -> Dict:
        """Send a pre-approved template message"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": language_code}
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
    
    def send_interactive_buttons(self, to: str, body_text: str, 
                                buttons: list) -> Dict:
        """Send message with interactive buttons"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        button_objects = []
        for i, button in enumerate(buttons):
            button_objects.append({
                "type": "reply",
                "reply": {
                    "id": f"btn_{i}",
                    "title": button
                }
            })
        
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text},
                "action": {"buttons": button_objects}
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
    
    def send_list_message(self, to: str, body_text: str, button_text: str,
                         sections: list) -> Dict:
        """Send interactive list message"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "interactive",
            "interactive": {
                "type": "list",
                "body": {"text": body_text},
                "action": {
                    "button": button_text,
                    "sections": sections
                }
            }
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()
    
    def mark_as_read(self, message_id: str) -> Dict:
        """Mark a message as read"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()


class InquiryHandler:
    """Intelligent inquiry handler with auto-responses"""
    
    def __init__(self, messenger: WhatsAppMessenger):
        self.messenger = messenger
        
        # Keywords for service matching
        self.service_keywords = {
            "discovery": ["discovery", "free call", "intro", "introduction"],
            "consultation": ["consultation", "initial", "first meeting"],
            "strategy": ["strategy", "planning", "half day", "workshop"],
            "retainer": ["retainer", "ongoing", "regular", "monthly"],
            "ml_ai": ["machine learning", "ml", "ai", "artificial intelligence", "model"],
            "cloud": ["cloud", "aws", "azure", "gcp", "migration"],
            "automation": ["automation", "integration", "workflow", "api"]
        }
    
    def analyze_inquiry(self, message: str) -> Dict:
        """Analyze incoming message and determine intent"""
        message_lower = message.lower()
        
        analysis = {
            "services_mentioned": [],
            "is_pricing_query": any(word in message_lower for word in 
                                   ["price", "cost", "rate", "fee", "how much"]),
            "is_booking_request": any(word in message_lower for word in 
                                     ["book", "schedule", "appointment", "meeting", "call"]),
            "is_general_inquiry": True
        }
        
        # Check which services are mentioned
        for service, keywords in self.service_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                analysis["services_mentioned"].append(service)
        
        return analysis
    
    def handle_inquiry(self, from_number: str, message: str, 
                      message_id: str) -> None:
        """Process inquiry and send appropriate response"""
        
        # Mark as read
        self.messenger.mark_as_read(message_id)
        
        # Analyze the message
        analysis = self.analyze_inquiry(message)
        
        # Handle discovery call requests immediately
        if "discovery" in analysis["services_mentioned"]:
            self.send_discovery_response(from_number)
            return
        
        # Handle pricing queries
        if analysis["is_pricing_query"]:
            self.send_pricing_response(from_number, analysis["services_mentioned"])
            return
        
        # Handle booking requests
        if analysis["is_booking_request"]:
            self.send_booking_response(from_number)
            return
        
        # Handle specific service inquiries
        if analysis["services_mentioned"]:
            self.send_service_info(from_number, analysis["services_mentioned"])
            return
        
        # Default: Send service options
        self.send_general_inquiry_response(from_number)
    
    def send_discovery_response(self, to: str) -> None:
        """Send discovery call booking info"""
        message = """Great! I'd love to have a discovery call with you. 🎯

This is a free 30-minute call where we can:
• Discuss your current challenges
• Explore how ML/AI or automation could help
• Determine if we're a good fit

You can book directly here: [YOUR_BOOKING_LINK]

Or reply with a few time slots that work for you (UK time), and I'll send a calendar invite."""
        
        self.messenger.send_text_message(to, message)
    
    def send_pricing_response(self, to: str, services: list) -> None:
        """Send pricing information"""
        message = """Here's my pricing structure (all prices exclude VAT):

📞 Discovery Call (30 min) - FREE
💼 Initial Consultation (1-2 hours) - £250
🎯 Strategy/Coaching Session (half-day) - £1,000

Monthly Retainers:
🥉 Bronze (1 day/week) - £2,000/month
🥈 Silver (2 days/week) - £4,000/month
🥇 Gold (3 days/week) - £6,000/month

For bespoke ML/AI implementations or large-scale cloud migrations, I provide custom quotes based on scope.

Would you like to start with a free discovery call?"""
        
        self.messenger.send_text_message(to, message)
    
    def send_booking_response(self, to: str) -> None:
        """Send booking options"""
        sections = [
            {
                "title": "Quick Start",
                "rows": [
                    {
                        "id": "discovery",
                        "title": "Discovery Call",
                        "description": "Free 30-min call"
                    },
                    {
                        "id": "consultation",
                        "title": "Initial Consultation",
                        "description": "1-2 hours - £250"
                    }
                ]
            },
            {
                "title": "Deep Dive",
                "rows": [
                    {
                        "id": "strategy",
                        "title": "Strategy Session",
                        "description": "Half-day - £1,000"
                    },
                    {
                        "id": "retainer",
                        "title": "Monthly Retainer",
                        "description": "Ongoing support"
                    }
                ]
            }
        ]
        
        self.messenger.send_list_message(
            to=to,
            body_text="What would you like to book?",
            button_text="View Services",
            sections=sections
        )
    
    def send_service_info(self, to: str, services: list) -> None:
        """Send detailed info about mentioned services"""
        service_info = {
            "ml_ai": "I specialize in practical ML/AI implementations - from proof-of-concept to production. This includes model development, MLOps, and helping teams understand what's realistic vs. hype.",
            "cloud": "Cloud adoption strategy and migration support across AWS, Azure, and GCP. I focus on right-sizing, cost optimization, and smooth transitions.",
            "automation": "Platform integrations and workflow automation using Python, APIs, and modern tools. I help eliminate repetitive tasks and connect your systems."
        }
        
        response_parts = []
        for service in services:
            if service in service_info:
                response_parts.append(service_info[service])
        
        if response_parts:
            message = "\n\n".join(response_parts)
            message += "\n\nWould you like to schedule a free discovery call to discuss your specific needs?"
            self.messenger.send_text_message(to, message)
    
    def send_general_inquiry_response(self, to: str) -> None:
        """Send general information"""
        buttons = ["View Services", "Book Discovery Call", "Pricing"]
        
        self.messenger.send_interactive_buttons(
            to=to,
            body_text="Hi! Thanks for reaching out. I help businesses with ML/AI, cloud adoption, and automation. How can I help you?",
            buttons=buttons
        )


# Webhook handler for receiving messages
def handle_webhook(request_body: Dict, messenger: WhatsAppMessenger, 
                   handler: InquiryHandler) -> None:
    """Process incoming webhook from WhatsApp"""
    
    try:
        # Extract message data
        entry = request_body.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        
        if not messages:
            return
        
        message = messages[0]
        from_number = message.get("from")
        message_id = message.get("id")
        
        # Handle text messages
        if message.get("type") == "text":
            text = message.get("text", {}).get("body", "")
            handler.handle_inquiry(from_number, text, message_id)
        
        # Handle interactive responses (button/list clicks)
        elif message.get("type") == "interactive":
            interactive = message.get("interactive", {})
            button_reply = interactive.get("button_reply", {})
            list_reply = interactive.get("list_reply", {})
            
            if button_reply:
                # Handle button click
                button_id = button_reply.get("id")
                # Process based on button_id
                pass
            
            if list_reply:
                # Handle list selection
                selected_id = list_reply.get("id")
                # Process based on selected_id
                pass
    
    except Exception as e:
        print(f"Error processing webhook: {e}")


# Example usage in a Flask webhook endpoint
"""
from flask import Flask, request

app = Flask(__name__)

ACCESS_TOKEN = "your_access_token"
PHONE_NUMBER_ID = "your_phone_number_id"

messenger = WhatsAppMessenger(ACCESS_TOKEN, PHONE_NUMBER_ID)
handler = InquiryHandler(messenger)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    handle_webhook(body, messenger, handler)
    return "OK", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    # WhatsApp webhook verification
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if mode == "subscribe" and token == "YOUR_VERIFY_TOKEN":
        return challenge, 200
    return "Forbidden", 403

if __name__ == "__main__":
    app.run(port=5000)
"""