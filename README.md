# ReserveMate – A FoodieSpot Initiative 🍽️

ReserveMate is an AI-powered restaurant reservation system designed to streamline the booking process for customers of FoodieSpot restaurants. Using advanced LLM-based conversational interfaces, it simplifies restaurant discovery, reservation management, and provides a personalized customer experience.

## Table of Contents

- [Setup Instructions](#setup-instructions)
- [Prompt Engineering Approach](#prompt-engineering-approach)
- [Example Conversations](#example-conversations)
- [Business Strategy](#business-strategy)
- [Feature Roadmap](#feature-roadmap)
  

## Setup Instructions

### Prerequisites

- Python 3.8+
- Internet connection for LLM API calls

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SriHarshitha88/Reserve-Mate.git
   cd ReserveMate
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your API credentials:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

To Obtain your Groq API Key - Proceed to Groq Console and Generate a new API Key.

## Prompt Engineering Approach

ReserveMate uses a carefully crafted system prompt that balances conversational abilities with function-calling capabilities:

### Core Principles

1. **Conversational First**: The AI maintains a friendly, personable conversation flow that feels natural to users.

2. **Tool Integration**: The system is designed to leverage tools for restaurant searches and reservation management rather than hallucinating responses.

3. **Progressive Information Gathering**: Rather than overwhelming users with multiple questions at once, the AI gathers information conversationally and progressively.

4. **Domain-Specific Knowledge**: The AI understands restaurant terminology and reservation processes.

### Prompt Engineering Techniques

- **Persona Definition**: Clear definition of the AI's role as ReserveMate
- **Instruction Clarity**: Explicit instructions on when to use tools and how to interact
- **Error Prevention**: Specific guidelines to prevent common LLM issues like hallucination
- **Conversational Guardrails**: Rules that ensure the conversation stays helpful and on-topic

### Tool Integration

Tools are defined with clear schemas and integrated with session state to enable:
- Restaurant searches with flexible parameters
- Reservation creation with validation
- Reservation modification and cancellation

## Example Conversations

### Restaurant Discovery Journey

**User**: "I'm looking for North Indian restaurants in Indiranagar for dinner this weekend."

**ReserveMate**: "I'd be happy to help you find a great North Indian spot in Indiranagar for the weekend! What day were you thinking of dining, and how many people will be in your party?"

**User**: "Saturday night, table for 4."

**ReserveMate**: "Perfect! I'll search for North Indian restaurants in Indiranagar for this Saturday. What time would you prefer for your dinner?"

**User**: "Around 8 PM."

**ReserveMate**: "I've found 3 excellent North Indian restaurants in Indiranagar available this Saturday at 8 PM for 4 guests:

1. **Punjabi By Nature** - Known for authentic flavors and tandoor specialties
2. **Spice Terrace** - Elegant dining with a lakeside view
3. **The Maharaja Club** - Royal dining experience with live music

Do any of these catch your interest?"

### Booking Confirmation Journey

**User**: "The Maharaja Club sounds good."

**ReserveMate**: "Great choice! The Maharaja Club offers a royal dining experience with live music on Saturdays. To confirm your reservation for 4 people this Saturday at 8 PM, I'll need your name and a contact number or email."

**User**: "My name is xyz, phone number is 9876543210."

**ReserveMate**: "Thanks, xyz! I've confirmed your reservation at The Maharaja Club for 4 guests this Saturday at 8 PM. Your booking ID is FS042. You'll receive a confirmation SMS shortly. Is there anything else you'd like to know about the restaurant before your visit?"

### Booking Modification Journey

**User**: "I need to change my reservation to 7 PM instead of 8 PM."

**ReserveMate**: "I'd be happy to help you modify your reservation. Could you please provide your booking ID?"

**User**: "FS042"

**ReserveMate**: "Thanks for providing your booking ID. I can see your reservation at The Maharaja Club for 4 guests this Saturday. Would you like me to change the time from 8 PM to 7 PM?"

**User**: "Yes, please."

**ReserveMate**: "Great! I've updated your reservation at The Maharaja Club. Your booking is now confirmed for 4 guests this Saturday at 7 PM. Your booking ID remains FS042. Is there anything else you'd like me to help with?"

## Business Strategy

ReserveMate is designed to transform the restaurant reservation experience for FoodieSpot while delivering significant business value:

### Long-Term Vision

ReserveMate aims to create an omnichannel restaurant booking system that's available everywhere and anytime—on mobile, web, or via voice calls. It will handle FAQs, suggest dishes based on preferences, and manage reservations end-to-end.

### Challenges Addressed

#### Operational Inefficiency
- Reduce staff dedicated solely to managing reservations
- Capture previously missed booking opportunities
- Streamline reservation processes

#### Revenue Optimization
- Balance occupancy between peak and off-peak hours
- Handle special occasions without system overloads
- Enable flexible pricing strategies

#### Customer Experience
- Create complete feedback loops
- Recognize and reward loyalty
- Enable personalization and upselling opportunities

#### Communication
- Overcome language limitations
- Unify communication across channels
- Enable proactive engagement

### Success Metrics

#### Primary Indicators
- **Adoption Rate**: ≥60% of reservations via ReserveMate within 3 months
- **No-Show Reduction**: ≥20% decrease through smart confirmations
- **Revenue Distribution**: ≥25% increase in off-peak covers
- **Customer Satisfaction**: ≥4.5/5 CSAT across all channels
- **Handling Time**: ≥30% faster booking process vs. manual systems

### Implementation Strategy

Phased deployment with ROI tracking:

1. **Phase 1**: Controlled Alpha (2 weeks)
   - Single flagship location
   - 100 VIP customers
   - Core booking functionality

2. **Phase 2**: Limited Beta (4 weeks)
   - 5 strategic locations
   - Full reservation flow with loyalty program
   - Staff training

3. **Phase 3**: City Cluster Launch (8 weeks)
   - All restaurants in key cities
   - Complete feature set
   - Multi-language support

4. **Phase 4**: Full-Scale National Rollout (12 weeks)
   - All 50+ locations nationwide
   - Complete POS and CRM integration
   - Advanced prediction features

## Feature Roadmap

### Current Implementation
- ✅ Basic restaurant search
- ✅ Restaurant booking
- ✅ Booking management (update/delete)
- ✅ Conversational interface

### Upcoming Features
- 🔄 Multi-language support
- 🔄 Loyalty program integration
- 🔄 Calendar integration
- 🔄 Proactive recommendations
- 🔄 Feedback collection and analysis

### Future Enhancements
- 📅 Advanced table management
- 📅 Pre-ordering capabilities
- 📅 Deposit handling for high-demand slots
- 📅 Voice channel support

---

© 2025 FoodieSpot. All rights reserved.
