#Adding in the OpenAI based schema for the two tools in question.

FIND_RESTAURANTS_SCHEMA = {
    "type": "function",
    "function": {
        "name": "find_restaurants",
        "description": "Searches for restaurants based on user criteria like city, specific area within a city, cuisine, date, time, or number of guests. Use this to help users discover suitable restaurants.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {  # NEW PARAMETER
                    "type": "string",
                    "description": "The city where the user wants to find a restaurant (e.g., 'Bengaluru', 'Mumbai', 'Delhi')."
                },
                "cuisine": {
                    "type": "string",
                    "description": "The type of Indian cuisine (e.g., 'North Indian', 'Hyderabadi', 'Punjabi')."
                },
                "location_area": { # This now refers to an area *within* a city
                    "type": "string",
                    "description": "The specific area or neighborhood within the specified city (e.g., 'Indiranagar' if city is 'Bengaluru', 'Bandra' if city is 'Mumbai')."
                },
                "date": {
                    "type": "string",
                    "description": "The desired date for the reservation in YYYY-MM-DD format."
                },
                "time": {
                    "type": "string",
                    "description": "The desired time for the reservation (e.g., '7 PM', '19:00')."
                },
                "num_guests": {
                    "type": "integer",
                    "description": "The number of guests for the reservation."
                }
            },
            "required": [] # Still no strictly required parameters to start a search.
        }
    }
}

BOOK_RESTAURANT_SCHEMA = {
    "type": "function",
    "function": {
        "name": "book_restaurant",
        "description": "Makes a reservation at a specific restaurant once all details are gathered. Ensure you have restaurant_id, date, time, num_guests, customer_name, and customer_contact before calling this.",
        "parameters": {
            "type": "object",
            "properties": {
                "restaurant_id": {
                    "type": "integer",
                    "description": "The unique ID of the restaurant to book, obtained from 'find_restaurants'."
                },
                "date": {
                    "type": "string",
                    "description": "The date for the booking in YYYY-MM-DD format."
                },
                "time": {
                    "type": "string",
                    "description": "The time for the booking (e.g., '7 PM', '19:00')."
                },
                "num_guests": {
                    "type": "integer",
                    "description": "The number of guests for the booking."
                },
                "customer_name": {
                    "type": "string",
                    "description": "The name of the customer making the booking."
                },
                "customer_contact": {
                    "type": "string",
                    "description": "The contact information for the customer (e.g., email or phone number)."
                }
            },
            "required": ["restaurant_id", "date", "time", "num_guests", "customer_name", "customer_contact"]
        }
    }
}

MODIFY_OR_DELETE_BOOKING_SCHEMA = {
    "type": "function",
    "function": {
        "name": "modify_or_delete_booking",
        "description": "Modifies or deletes an existing booking. For updates, only include fields that need to be changed.",
        "parameters": {
            "type": "object",
            "properties": {
                "booking_id": {
                    "type": "string",
                    "description": "The unique ID of the booking to modify/delete (e.g., 'FS001')."
                },
                "action": {
                    "type": "string",
                    "enum": ["update", "delete"],
                    "description": "Whether to update or delete the booking."
                },
                "date": {
                    "type": "string",
                    "description": "New date for the booking in YYYY-MM-DD format (for updates only)."
                },
                "time": {
                    "type": "string",
                    "description": "New time for the booking (e.g., '7 PM', '19:00') (for updates only)."
                },
                "num_guests": {
                    "type": "integer",
                    "description": "New number of guests (for updates only)."
                },
                "customer_name": {
                    "type": "string",
                    "description": "Updated name for the booking (for updates only)."
                },
                "special_requests": {
                    "type": "string",
                    "description": "Any special requests or notes (for updates only)."
                }
            },
            "required": ["booking_id", "action"]
        }
    }
}

TOOLS_AVAILABLE = [FIND_RESTAURANTS_SCHEMA, BOOK_RESTAURANT_SCHEMA, MODIFY_OR_DELETE_BOOKING_SCHEMA]