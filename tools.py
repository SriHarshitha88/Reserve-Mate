#The Actual Tooling Functions being Used
import json
from datetime import datetime


# In-memory store for bookings for the demo\
def load_restaurants_from_file(path="restaurants.json"):
    try:
        with open(path, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: Restaurant data file not found at {path}")
        return [] # Or raise error
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {path}")
        return [] # Or raise error

ALL_RESTAURANTS = load_restaurants_from_file()

def find_restaurants(city: str = None, # NEW PARAMETER
                     cuisine: str = None, 
                     location_area: str = None, 
                     date: str = None, time: str = None, num_guests: int = None):
    """
    Searches for restaurants based on provided criteria, including city.
    """
    if not ALL_RESTAURANTS:
         return {"error": "Restaurant data not loaded. Cannot perform search."}
    
    results = list(ALL_RESTAURANTS) # Start with all restaurants

    # Filter by city first, if provided
    if city:
        results = [r for r in results if city.lower() in r.get('city', '').lower()]
        if not results: # If no restaurants in the specified city, no point in further filtering
            return {"message": f"Sorry, we don't seem to have any restaurants listed in {city} yet. Would you like to try another city?"}

    # Then filter by cuisine within the (potentially city-filtered) results
    if cuisine:
        results = [r for r in results if cuisine.lower() in r.get('cuisine_type', '').lower()]

    # Then filter by location_area within the (potentially city and cuisine filtered) results
    if location_area:
        # It's more natural if location_area is searched within the context of a city if a city was given
        # The current logic applies it sequentially, which is fine.
        results = [r for r in results if location_area.lower() in r.get('city_area', '').lower()]
    
    # Filter by number of guests
    if num_guests is not None:
        try:
            num_guests_int = int(num_guests)
            results = [r for r in results if r.get('seating_capacity', 0) >= num_guests_int]
        except ValueError:
            return {"error": "Invalid number of guests. Please provide a number."}

    if not results:
        # Provide a more specific message if filters were applied
        criteria_applied = []
        if city: criteria_applied.append(f"city: {city}")
        if cuisine: criteria_applied.append(f"cuisine: {cuisine}")
        if location_area: criteria_applied.append(f"area: {location_area}")
        if num_guests: criteria_applied.append(f"guests: {num_guests}")
        
        if criteria_applied:
            return {"message": f"No restaurants found matching your specific criteria ({', '.join(criteria_applied)}). Perhaps broaden your search?"}
        else: # Should not happen if ALL_RESTAURANTS is populated
            return {"message": "No restaurants found. This is unexpected."}
    
    limited_results = results[:5] # Limit to top 5 results for brevity
    return [
        {
            "id": r['id'], 
            "name": r['name'],
            "city": r.get('city', 'N/A'), # Include city in results
            "area": r.get('city_area', 'N/A'), # Keep area, now it's area within city
            "cuisine": r.get('cuisine_type', 'N/A'), 
            "capacity": r.get('seating_capacity', 0),
            "avg_price_inr": r.get('average_price_per_diner_inr', 'N/A'), # Use the new field name
            "special_features": r.get('special_features', [])
        } for r in limited_results
    ]

def book_restaurant(bookings_db_ref, booking_id_counter_ref, # Pass references to mutable session state parts
                    restaurant_id: int, date: str, time: str, 
                    num_guests: int, customer_name: str, customer_contact: str):
    """
    Books a table at a specific restaurant.
    (Implementation is largely the same, but takes bookings_db and counter_ref)
    """
    if not ALL_RESTAURANTS:
         return {"success": False, "message": "Restaurant data not loaded. Cannot perform booking."}
    try:
        restaurant_id = int(restaurant_id)
        num_guests = int(num_guests)
    except ValueError:
        return {"success": False, "message": "Invalid restaurant ID or number of guests. Please provide numbers."}

    restaurant = next((r for r in ALL_RESTAURANTS if r['id'] == restaurant_id), None)
    if not restaurant:
        return {"success": False, "message": f"Restaurant with ID {restaurant_id} not found."}

    if num_guests > restaurant.get('seating_capacity', 0):
        return {"success": False, "message": f"Sorry, {restaurant['name']} does not have capacity for {num_guests} guests. Max capacity: {restaurant.get('seating_capacity',0)}."}
    
    try:
        datetime.strptime(date, "%Y-%m-%d") 
    except ValueError:
        return {"success": False, "message": "Invalid date format. Please use YYYY-MM-DD."}

    new_booking_id_val = booking_id_counter_ref["value"] # Access through reference
    new_booking_id_str = f"FS{new_booking_id_val:03d}"
    
    bookings_db_ref[new_booking_id_str] = {
        "restaurant_id": restaurant_id,
        "restaurant_name": restaurant['name'],
        "date": date,
        "time": time,
        "num_guests": num_guests,
        "customer_name": customer_name,
        "customer_contact": customer_contact,
        "status": "confirmed"
    }
    booking_id_counter_ref["value"] += 1 # Increment through reference
    
    return {
        "success": True, 
        "booking_id": new_booking_id_str, 
        "details": bookings_db_ref[new_booking_id_str], # Use the updated DB ref
        "message": f"Booking confirmed for {customer_name} at {restaurant['name']} (ID: {restaurant_id}) for {num_guests} guests on {date} at {time}. Your booking ID is {new_booking_id_str}."
    }

def modify_or_delete_booking(bookings_db_ref, booking_id: str, action: str, **updates):
    """
    Modifies or deletes an existing booking.
    
    Args:
        bookings_db_ref: Reference to the bookings dictionary
        booking_id: The ID of the booking to modify/delete
        action: Either 'update' or 'delete'
        **updates: For 'update' action, fields to update (date, time, num_guests, etc.)
        
    Returns:
        dict: Result of the operation with success status and message
    """
    if booking_id not in bookings_db_ref:
        return {"success": False, "message": f"Booking ID {booking_id} not found."}
    
    booking = bookings_db_ref[booking_id]
    
    if action == "delete":
        del bookings_db_ref[booking_id]
        return {
            "success": True,
            "message": f"Booking {booking_id} has been cancelled.",
            "deleted_booking": booking
        }
    
    elif action == "update":
        # Only update fields that are provided in updates
        valid_fields = ["date", "time", "num_guests", "customer_name", "special_requests"]
        updates = {k: v for k, v in updates.items() if k in valid_fields and v is not None}
        
        # Validate date format if being updated
        if "date" in updates:
            try:
                datetime.strptime(updates["date"], "%Y-%m-%d")
            except ValueError:
                return {"success": False, "message": "Invalid date format. Please use YYYY-MM-DD."}
        
        # Validate num_guests if being updated
        if "num_guests" in updates:
            try:
                updates["num_guests"] = int(updates["num_guests"])
                # Optionally, you could add capacity validation here
            except (ValueError, TypeError):
                return {"success": False, "message": "Number of guests must be a valid number."}
        
        # Update the booking
        booking.update(updates)
        return {
            "success": True,
            "message": f"Booking {booking_id} has been updated.",
            "updated_booking": booking
        }
    
    return {"success": False, "message": "Invalid action. Must be 'update' or 'delete'."}

AVAILABLE_PYTHON_TOOLS = {
    "find_restaurants": find_restaurants,
    "book_restaurant": book_restaurant,
    "modify_or_delete_booking": modify_or_delete_booking,
}