import json
import ollama

# --- 1. Supermarket Tools (Internal Data) ---

ITEMS_DATABASE = {
    "organic apples": {"price": 2.99, "stock": 45, "unit": "lb", "aisle": 3},
    "whole milk": {"price": 3.49, "stock": 12, "unit": "gallon", "aisle": 1},
    "sourdough bread": {"price": 4.99, "stock": 0, "unit": "loaf", "aisle": 5},
    "cereal": {"price": 5.29, "stock": 20, "unit": "box", "aisle": 2},
}

STORE_INFO = {
    "hours": "Monday - Sunday: 7:00 AM - 10:00 PM",
    "holidays": "Closed on Thanksgiving Day and Christmas Day. Open 8:00 AM - 4:00 PM on New Year's Day.",
    "return_policy": "Receipt required within 14 days for a full refund. Perishables non-refundable after 48 hours."
}

def check_product_info(item_name: str) -> dict:
    """Gets price, stock quantity, and aisle location for a store item."""
    item = item_name.lower().strip()
    if item in ITEMS_DATABASE:
        return {"item": item, **ITEMS_DATABASE[item]}
    return {"error": f"Item '{item_name}' not found in inventory."}

def check_store_policy(query_type: str) -> str:
    """Returns store policies, operating hours, or holiday schedules.
    Allowed query_type values: 'hours', 'holidays', 'return_policy'
    """
    return STORE_INFO.get(query_type.lower().strip(), "Policy information not available.")

def calculate_item_total(price: float, quantity: int) -> float:
    """Calculates the total cost for a specific item quantity."""
    return round(price * quantity, 2)


# Map tool names to actual python functions
AVAILABLE_TOOLS = {
    "check_product_info": check_product_info,
    "check_store_policy": check_store_policy,
    "calculate_item_total": calculate_item_total,
}

TOOL_SCHEMAS = [check_product_info, check_store_policy, calculate_item_total]


# --- 2. Multi-Step Execution Loop ---

def run_supermarket_agent(system_prompt: str, user_prompt: str, max_iterations: int = 5):
    """Agent runner that loops dynamically until the model finishes multi-step reasoning."""
    print(f"\n==================== NEW REQUEST ====================")
    print(f"User: {user_prompt}\n")

    # Maintain local conversation history for context during tool calling loop
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    iteration = 0

    while iteration < max_iterations:
        iteration += 1

        # Query the model with available tools
        response = ollama.chat(
            model="gemma4",
            messages=messages,
            tools=TOOL_SCHEMAS
        )

        message = response["message"]
        messages.append(message)  # Save assistant response to history

        # Exit condition: If the model has no tool calls, it has reached its final answer
        if not message.get("tool_calls"):
            print(f"[Final Agent Answer]:\n{message['content']}\n")
            return

        # Handle tool calls dynamically
        for tool in message["tool_calls"]:
            func_name = tool["function"]["name"]
            func_args = tool["function"]["arguments"]

            print(f"[Step {iteration} Tool Call]: {func_name}({func_args})")

            if func_name in AVAILABLE_TOOLS:
                tool_output = AVAILABLE_TOOLS[func_name](**func_args)
                print(f"[Tool Output]: {tool_output}\n")

                # Send tool execution output back into context history
                messages.append({
                    "role": "tool",
                    "name": func_name,
                    "content": json.dumps(tool_output)
                })
            else:
                print(f"[Execution Error]: Function '{func_name}' not available.\n")

    print("[Warning]: Maximum reasoning iterations reached standard execution cutoff.")


# --- 3. Example Demonstrations ---

SYSTEM_PROMPT = """You are FreshCart Supermarket's AI Assistant. 
You answer customer questions accurately by checking store stock, calculating price totals, and providing operating details.
Use tool calls sequentially to resolve complex queries requiring multi-step reasoning. Always state prices, availability, and totals clearly."""

# Example 1: Multi-step check and calculation across stock/prices
USER_PROMPT_1 = "I want to buy 3 boxes of cereal and 2 gallons of whole milk. Are both in stock, and what will the total price be?"

# Example 2: Inquiry spanning policy + out-of-stock item handling
USER_PROMPT_2 = "Can I buy sourdough bread on Thanksgiving Day? Also, do you have any in stock right now?"

# Example 3: General customer support and store info check
USER_PROMPT_3 = "What are your return policy rules, and what aisle can I find organic apples in?"


# Run demonstrations
if __name__ == "__main__":
    #run_supermarket_agent(SYSTEM_PROMPT, USER_PROMPT_1)
    #run_supermarket_agent(SYSTEM_PROMPT, USER_PROMPT_2)
    run_supermarket_agent(SYSTEM_PROMPT, USER_PROMPT_3)
