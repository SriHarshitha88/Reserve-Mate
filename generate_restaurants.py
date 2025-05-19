#Imports
import json
import random

def generate_restaurants(num_restaurants=50): # Increased default for more variety
    cuisines = [
        "North Indian", "South Indian","Kerala", "Hyderabadi"
    ]
    indian_cities = {
        "Bengaluru": ["Indiranagar", "Koramangala", "HSR Layout", "Whitefield", "MG Road", "Jayanagar", "Malleshwaram", "JP Nagar", "Electronic City", "Marathahalli"],
        "Mumbai": ["Bandra", "Andheri", "Colaba", "Dadar", "Juhu", "Powai", "Lower Parel", "Fort", "Chembur", "Borivali"],
        "Delhi": ["Connaught Place", "Hauz Khas Village", "Khan Market", "Saket", "Greater Kailash", "Chandni Chowk", "Karol Bagh", "Nehru Place", "Dwarka", "Rohini"],
        "Chennai": ["T. Nagar", "Anna Nagar", "Nungambakkam", "Adyar", "Mylapore", "Velachery", "Guindy", "OMR", "Besant Nagar", "Egmore"],
        "Hyderabad": ["Banjara Hills", "Jubilee Hills", "Gachibowli", "Hitech City", "Secunderabad", "Kukatpally", "Madhapur", "Ameerpet", "Dilsukhnagar", "Charminar"],
        "Kolkata": ["Park Street", "Salt Lake", "New Town", "Ballygunge", "Howrah", "Esplanade", "Gariahat", "Dum Dum", "Behala", "Shyambazar"],
        "Pune": ["Koregaon Park", "Viman Nagar", "Deccan Gymkhana", "Hinjewadi", "Kothrud", "Baner", "Wakad", "Hadapsar", "Pimpri-Chinchwad", "Shivaji Nagar"],
        "Ahmedabad": ["SG Highway", "Navrangpura", "Maninagar", "Prahlad Nagar", "Satellite", "Bodakdev", "Vastrapur", "Chandkheda", "Bopal", "Thaltej"]
    }

    names_prefixes = [
        "Spice", "Royal", "Taj", "Desi", "Masala", "Swad", "Rasoi", "Zaika", "Dawat", 
        "Bawarchi", "Dhaba", "Swaad", "Annapurna", "Tandoor", "Maharaja", "Nawab", 
        "Haveli", "Mirch", "Curry", "Shahi"
    ]
    names_suffixes = [
        "Darbar", "Mahal", "Bhavan", "Kitchen", "Dhaba", "Palace", "Garden", "House", 
        "Cafe", "Rasoi", "Hut", "Express", "Delight", "Chowk", "Corner", "Point",
        "Grill", "Pot", "Treats", "Junction"
    ]
    special_features_options = [
        ["Outdoor Seating"], ["Pure Vegetarian"], ["Jain Food Available"], ["Live Ghazals"],
        ["Family Dining"], ["Buffet Available"], ["Rooftop Dining"], ["Private Party Hall"],
        ["Lunch Thali Special"], ["Award-Winning Chef"], ["Live Tandoor/Grill"], 
        ["Authentic Regional Specialties"], ["Imported Spices"], ["Home Delivery Available"], 
        ["Traditional Indian Seating"], ["Serves Alcohol"], ["Kid-Friendly Zone"],
        ["Valet Parking"], ["Disabled Access"]
    ]
    indian_road_names = ['MG', 'Nehru', 'Gandhi', 'Patel', 'Subhash', 'Tagore', 'Bose', 'Shastri', 'Ambedkar', 'Vivekananda', 'Lajpat Rai', 'Tilak', 'Sardar Patel', 'Rajaji']


    restaurants = []
    for i in range(1, num_restaurants + 1):
        cuisine = random.choice(cuisines)
        
        # Select a city first
        city_name = random.choice(list(indian_cities.keys()))
        city_area = random.choice(indian_cities[city_name]) # Area within the selected city

        # More authentic Indian restaurant naming patterns
        if random.random() < 0.15: # City in name
            name = f"{city_name} {random.choice(names_prefixes)} {random.choice(names_suffixes)}"
        elif random.random() < 0.3:
            name = f"{random.choice(names_prefixes)} {random.choice(names_suffixes)}"
        elif random.random() < 0.6:
            name = f"{random.choice(names_prefixes)} {cuisine}"
        else:
            name = f"{cuisine} {random.choice(names_suffixes)}"
        
        # Ensure uniqueness (simple approach for demo, might need more robust for many items)
        # This simple check might lead to slightly fewer than num_restaurants if collisions are frequent
        temp_name_parts = name.split()
        if len(temp_name_parts) > 2 and temp_name_parts[0] == temp_name_parts[1]: # Avoid "Spice Spice Kitchen"
            name = " ".join(temp_name_parts[1:])
        if any(r['name'] == name and r['city_area'] == city_area for r in restaurants): # Simple check for name collision in same area
            name = f"{name} {random.choice(['Corner', 'Point', 'II'])}"


        features_count = random.randint(0, 4) # Increased max features
        special_features = random.sample(special_features_options, features_count)
        special_features = [item for sublist in special_features for item in sublist] # Flatten

        restaurant = {
            "id": i,
            "name": name,
            "address": f"{random.randint(10, 999)}, {random.choice(indian_road_names)} Road, {city_area}",
            "city": city_name, # NEW FIELD
            "city_area": city_area, # Area within the city
            "cuisine_type": cuisine,
            "seating_capacity": random.choice([20, 30, 40, 50, 60, 70, 80, 100, 120, 150, 180, 200]),
            "operating_hours": { # Slightly more varied hours
                "Mon-Thu": f"{random.choice(['11:30am', '12:00pm'])} - {random.choice(['3:00pm', '3:30pm'])} & {random.choice(['6:30pm', '7:00pm'])} - {random.choice(['11:00pm', '11:30pm'])}",
                "Fri-Sun": f"{random.choice(['11:30am', '12:00pm'])} - {random.choice(['11:30pm', '12:00am'])}"
            },
            "average_price_per_diner_inr": random.choice([200, 300, 400, 500, 650, 750, 900, 1100, 1300, 1500, 2000]), # INR
            "special_features": special_features,
            "phone_number": f"+91 {random.choice(['98', '99', '88', '77', '70', '80'])}{random.randint(10000000,99999999)}" # More realistic mobile
        }
        restaurants.append(restaurant)
    
    with open("restaurants.json", "w") as f:
        json.dump(restaurants, f, indent=4)
    print(f"Generated {len(restaurants)} Indian-specific restaurants in restaurants.json")

if __name__ == "__main__":
    generate_restaurants(50) # Generate 50 restaurants