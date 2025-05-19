#Imports
import json
from llm_interface import get_llm_response_with_tools # Using the non-streaming version
from tools import AVAILABLE_PYTHON_TOOLS, ALL_RESTAURANTS
from tools_schema import TOOLS_AVAILABLE 

#Defining the System Prompt here - Goal is to focus on Tool calls and be conversational as possible
SYSTEM_PROMPT = """You are ReserveMate, a helpful and conversational assistant for FoodieSpot restaurants. Your personality is friendly and personable - you chat naturally rather than overwhelming users with questions all at once.
IMPORTANT: You must make MANDATORILY make appropriate tool calls whenever you have sufficient information for a search or booking or updating a booking. STRICTLY Never pretend to search or book or update a booking without using the proper tool functions.

Your primary functions:
- Help users find restaurants matching their preferences
- Assist with table reservations

When a user expresses interest in finding a restaurant or making a reservation, guide them through the process conversationally, asking for information one step at a time rather than all at once.

Guidelines TO STRICTLY ADHERE TO:
- STRICTLY DO NOT DO Any searches/BOOKINGS/UPDATES without using the appropriate tool functions.
- PLEASE Ensure you have all the contact information and name before making a BOOKING TOOL CALL. 
- STRICTLY do not mention about Tool call use or send any internal use variables like tool call id, Restaurant ID etc. Avoid messages like "It looks like the tool call call_9jvz returned an error or successful"
- Keep your responses friendly, concise, and occasionally use relevant emojis to add personality (but don't overdo it)."""

#Defining a Pseudo-Streaming Function - To Mimic Streaming. In Normal Condtions, this will be a Stream=True param.
def process_user_message_pseudo_stream(user_input_content, conversation_history, bookings_db_ref, booking_id_counter_ref):
    """
    Processes a user message, interacts with LLM using OpenAI-style tool calling.
    The final text output will be "pseudo-streamed" by the calling UI.
    Returns the final text string from the assistant.
    """
    conversation_history.append({"role": "user", "content": user_input_content})
    
    messages_for_llm = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    llm_message_response = get_llm_response_with_tools(messages_for_llm, TOOLS_AVAILABLE)

    if isinstance(llm_message_response, str) and llm_message_response.startswith("LLM_ERROR:"):
        error_content = llm_message_response
        final_response_text = f"Sorry, I faced an issue: {error_content}"
        conversation_history.append({"role": "assistant", "content": final_response_text})
        return final_response_text

    # llm_message_response is a ChatCompletionMessage object
    response_message_content_text = llm_message_response.content # Text part, could be None
    tool_calls = llm_message_response.tool_calls # List of tool calls or None

    if tool_calls:
        print(f"[AGENT LOG] LLM requested tool call(s):")
        for tc_log in tool_calls:
            print(f"[AGENT LOG]   - Tool: {tc_log.function.name}, Args: {tc_log.function.arguments}, ID: {tc_log.id}")

        # Add the LLM's response (which includes the tool_calls request) to history
        conversation_history.append(
            {
                "role": "assistant",
                "content": response_message_content_text if response_message_content_text else None,
                "tool_calls": [ # Store simplified version for history
                    {
                        "id": tc.id, "type": tc.type,
                        "function": {"name": tc.function.name, "arguments": tc.function.arguments}
                    } for tc in tool_calls
                ]
            }
        )

        for tool_call in tool_calls: # tool_call is now a ToolCall object
            function_name = tool_call.function.name
            function_args_json = tool_call.function.arguments
            tool_call_id = tool_call.id
            
            print(f"[AGENT LOG] Executing tool: {function_name} with ID: {tool_call_id}")
            try:
                function_args = json.loads(function_args_json)
            except json.JSONDecodeError as e:
                print(f"[AGENT ERROR] Failed to parse tool arguments: {function_args_json}, Error: {e}")
                tool_result_content = json.dumps({"error": f"Invalid args format from LLM: {function_args_json}"})
                conversation_history.append({
                    "role": "tool", "tool_call_id": tool_call_id,
                    "name": function_name, "content": tool_result_content
                })
                continue

            if function_name in AVAILABLE_PYTHON_TOOLS:
                python_function_to_call = AVAILABLE_PYTHON_TOOLS[function_name]
                try:
                    if function_name == "find_restaurants":
                        tool_result = python_function_to_call(**function_args)
                    elif function_name == "book_restaurant":
                        tool_result = python_function_to_call(bookings_db_ref, booking_id_counter_ref, **function_args)
                    else:
                        tool_result = python_function_to_call(bookings_db_ref, **function_args)
                    tool_result_content = json.dumps(tool_result)
                    print(f"[AGENT LOG] Tool {function_name} (ID: {tool_call_id}) executed. Result snippet: {tool_result_content[:100]}...")
                except Exception as e:
                    print(f"[AGENT ERROR] Tool {function_name} (ID: {tool_call_id}) execution failed: {e}")
                    tool_result_content = json.dumps({"error": f"Error during {function_name} execution: {str(e)}"})
                
                conversation_history.append({
                    "role": "tool", "tool_call_id": tool_call_id, 
                    "name": function_name, "content": tool_result_content
                })
            else:
                print(f"[AGENT WARNING] Unknown tool '{function_name}' requested.")
                conversation_history.append({
                    "role": "tool", "tool_call_id": tool_call_id,
                    "name": function_name, "content": json.dumps({"error": f"Unknown tool: {function_name}"})
                })
        
        # Second LLM call to get summary based on tool results
        messages_for_llm_after_tool = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history
        final_llm_message_response = get_llm_response_with_tools(messages_for_llm_after_tool, TOOLS_AVAILABLE) # Can still use tools

        if isinstance(final_llm_message_response, str) and final_llm_message_response.startswith("LLM_ERROR:"):
            final_response_text = f"Sorry, I faced an issue after using a tool: {final_llm_message_response}"
        elif final_llm_message_response.tool_calls:
            # LLM wants to call ANOTHER tool. For simplicity, just take text content.
            print("[AGENT WARNING] LLM requested a nested tool call. Taking text content only for this turn.")
            final_response_text = final_llm_message_response.content if final_llm_message_response.content else "I've processed that. What next?"
            # Store the nested tool call request in history for completeness
            conversation_history.append({
                "role": "assistant", "content": final_response_text,
                "tool_calls": [
                    {"id": tc.id, "type": tc.type, "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                    for tc in final_llm_message_response.tool_calls
                ]
            })
        else:
            final_response_text = final_llm_message_response.content if final_llm_message_response.content else "Okay, done."
            conversation_history.append({"role": "assistant", "content": final_response_text})
        
        return final_response_text

    else:
        # No tool call, LLM responded directly with text
        final_response_text = response_message_content_text if response_message_content_text else "I'm not sure how to help with that. Can you rephrase?"
        conversation_history.append({"role": "assistant", "content": final_response_text})
        return final_response_text