import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.messagebox  # Import for pop-up messages
import random  # For customer generation and shuffling lists

# --- GLOBAL UI Element References (for state management) ---
# These variables need to be accessible and modifiable by different functions
customer_order_display_textbox = None
python_command_textbox = None
current_selected_customer_data = None  # Stores data of customer currently being handled (the one whose 'Serve' button was last clicked)
all_serve_buttons = []  # List to hold references to all 'Serve' buttons on customer cards
btn_complete_sale_ref = None  # Reference to the 'Complete Sale' button
customer_cards_container = None  # Reference to the frame holding customer cards, needed for repopulation

# --- GLOBAL GAME STATE VARIABLES (Consolidated) ---
player_level = 1
balance = 1000  # Starting balance
game_time = 900  # 9:00 AM (HHMM format)
inventory = {}  # Will be populated at startup by unlock_level_items
MAX_CUSTOMERS = 4  # Max simultaneous customers displayable on UI
active_customers = []  # List to hold currently active customer dictionaries (actual game state)

# Master list of all possible items in the game
ALL_GAME_ITEMS = {
    "health potion": {"price": 50, "restock_cost": 30},
    "mana elixir": {"price": 75, "restock_cost": 45},
    "iron sword": {"price": 200, "restock_cost": 120},
    "leather armor": {"price": 150, "restock_cost": 90},
    "healing salve": {"price": 20, "restock_cost": 12},
    "scroll of fireball": {"price": 120, "restock_cost": 80},
    "gold coin pouch": {"price": 10, "restock_cost": 5},  # Small item for common orders
    "enchanted amulet": {"price": 500, "restock_cost": 350},
}

# Items unlocked at each level (and their initial stock level for fresh unlock)
LEVEL_ITEM_UNLOCKS = {
    1: {"health potion": {"stock": 10}, "mana elixir": {"stock": 5}},  # Initial items
    2: {"iron sword": {"stock": 0}, "leather armor": {"stock": 0}, "healing salve": {"stock": 15}},
    3: {"scroll of fireball": {"stock": 0}, "gold coin pouch": {"stock": 20}, "enchanted amulet": {"stock": 0}},
}

# Level-up costs/thresholds (for future use)
LEVEL_UP_COSTS = {
    2: 500,
    3: 1500,
}

# List of names for customer generation
FIRST_NAMES = ["Sir Reginald", "Lady Elara", "Master Theron", "Apprentice Lyra", "Goblin Gnarl", "Orc Grunt",
               "Dark Sorcerer", "Mystic Anya"]
LAST_NAMES = ["of Eldoria", "Stonefist", "Whisperwind", "Brightspark", "Grimtooth", "Bloodaxe", "Shadowfell",
              "Moonpetal"]

# --- DYNAMIC CUSTOMER DATA FOR FILLING DISPLAY SLOTS (Mock Data for UI Testing) ---
# This list is only used to fill display slots if active_customers has fewer than MAX_CUSTOMERS
mock_customers = [
    {"id": 101, "name": "Sir Reginald", "type": "Knight", "order": {"health potion": 3, "leather armor": 1}},
    {"id": 102, "name": "Apprentice Lyra", "type": "Mage", "order": {"mana elixir": 2, "scroll of fireball": 1}},
    {"id": 103, "name": "Goblin Gnarl", "type": "Raider", "order": {"gold coin pouch": 5}},
    {"id": 104, "name": "Lady Elara", "type": "Noble", "order": {"healing salve": 2, "enchanted amulet": 1}},
    {"id": 105, "name": "Orc Grunt", "type": "Warrior", "order": {"iron sword": 1, "health potion": 1}},
    {"id": 106, "name": "Dark Sorcerer", "type": "Evil", "order": {"mana elixir": 3, "enchanted amulet": 1}},
]


# --- HELPER FUNCTIONS ---
def format_time(time_int):
    """Converts HHMM integer to a readable time string (e.g., 900 -> 09:00 AM)."""
    hours = time_int // 100
    minutes = time_int % 100
    period = "AM"
    if hours >= 12:
        period = "PM"
        if hours > 12:
            hours -= 12
    if hours == 0:  # Handle 00:xx as 12:xx AM
        hours = 12
    return f"{hours:02d}:{minutes:02d} {period}"


def unlock_level_items(level, current_inventory):
    """Adds new items to the inventory based on the player's level."""
    if level in LEVEL_ITEM_UNLOCKS:
        print(f"\n--- NEW ITEMS UNLOCKED FOR LEVEL {level}! ---")
        for item_name, initial_details in LEVEL_ITEM_UNLOCKS[level].items():
            if item_name not in current_inventory:  # Only add if not already present
                current_inventory[item_name] = {
                    "stock": initial_details["stock"],
                    "price": ALL_GAME_ITEMS[item_name]["price"],
                    "restock_cost": ALL_GAME_ITEMS[item_name]["restock_cost"]
                }
                print(
                    f"- {item_name.title()} (Price: ₱{current_inventory[item_name]['price']}, Restock: ₱{current_inventory[item_name]['restock_cost']})")
        print("-------------------------------------------\n")


def generate_customer():
    """Generates a new random customer with an order based on current inventory."""
    name = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

    available_items_for_order = list(inventory.keys())  # Use the global 'inventory'

    if not available_items_for_order:
        print("Warning: No items in inventory to generate customer orders from (is inventory empty?).")
        return None

    num_items_in_order = random.randint(1, min(len(available_items_for_order), 3))  # 1 to 3 distinct items
    order = {}

    random.shuffle(available_items_for_order)

    for i in range(num_items_in_order):
        item = available_items_for_order[i]
        quantity = random.randint(1, 5)  # Order 1 to 5 units of an item
        order[item] = quantity

    customer = {
        "id": random.randint(1000, 9999),  # Unique ID for identification
        "name": name,
        "type": random.choice(["Knight", "Mage", "Raider", "Noble", "Merchant"]),  # Expanded types
        "order": order,
        "patience": random.randint(3, 6)  # How many "ticks" before they leave (for future time system)
    }
    return customer


# --- FUNCTIONS TO BE CALLED BY UI ACTIONS ---

def serve_customer_ui_action(customer_data):
    """
    This function is called when a 'Serve' button on a customer card is clicked.
    It updates the 'Customer Order' display in the 'Handle Order' frame
    and prepares the transaction area.
    """
    global customer_order_display_textbox, python_command_textbox, current_selected_customer_data

    if customer_order_display_textbox:
        current_selected_customer_data = customer_data  # Store the customer data for later use by Run Code/Complete Sale

        # Format the customer order details for display
        order_details = f"Customer: {customer_data['name']} ({customer_data['type']})\n"
        order_details += "Order:\n"
        for item, qty in customer_data['order'].items():
            order_details += f"  - {qty} {item.title()}\n"

        # Update the read-only customer order textbox
        customer_order_display_textbox.config(state='normal')  # Enable writing temporarily
        customer_order_display_textbox.delete('1.0', tk.END)  # Clear previous content
        customer_order_display_textbox.insert(tk.END, order_details)  # Insert new content
        customer_order_display_textbox.config(state='disabled')  # Disable writing again (make it read-only)

        # Clear the python command box for new input, if a customer is selected
        if python_command_textbox:
            python_command_textbox.delete('1.0', tk.END)

        print(f"Customer {customer_data['name']}'s order loaded for handling.")
    else:
        print("Error: Customer order display textbox not initialized.")


def serve_customer_and_update_buttons(customer_data, clicked_button):
    """
    Called when a 'Serve' button is clicked.
    Updates all serve button states ('Serving', 'Waiting', 'Serve')
    and then calls the main UI action to display the order.
    """
    global all_serve_buttons, btn_complete_sale_ref

    # First, disable the 'Complete Sale' button, as a new customer/transaction means previous code is invalid
    if btn_complete_sale_ref:
        btn_complete_sale_ref.config(state='disabled')

    # Update the states and text of all 'Serve' buttons
    for btn in all_serve_buttons:
        if btn == clicked_button:
            # The button that was just clicked
            btn.config(text="Serving", state='disabled')
        else:
            # All other 'Serve' buttons
            btn.config(text="Waiting", state='disabled')

            # Now, call the main UI action to display the order in the Handle Order frame
    serve_customer_ui_action(customer_data)


def run_code_command():
    """
    Called when the 'Run Code' button is pressed.
    Retrieves the Python code from the textbox, attempts to validate it (simulated for now),
    and provides feedback.
    """
    global inventory, balance  # <<< RE-ADD THIS LINE HERE
    global python_command_textbox, btn_complete_sale_ref, current_selected_customer_data

    if not current_selected_customer_data:
        tkinter.messagebox.showwarning("No Customer Selected", "Please select a customer by clicking 'Serve' first.")
        return

    player_code = python_command_textbox.get('1.0', tk.END).strip()

    if not player_code:
        tkinter.messagebox.showwarning("Empty Code", "Please enter some Python code to run.")
        if btn_complete_sale_ref:
            btn_complete_sale_ref.config(state='disabled')
        return

    # --- Prepare the execution environment (sandbox) ---
    # Create copies of inventory and balance for the player's code to modify.
    # This allows us to verify changes without directly affecting the real game state yet.
    exec_inventory = {item: data.copy() for item, data in inventory.items()}
    exec_balance = balance

    # A mutable list to hold balance so inner code can modify it and it's reflected outside
    # (because integers are immutable, `balance += X` creates a new int, not modifies the original if global)
    balance_wrapper = [exec_balance]

    # Define the scope for the player's code execution
    execution_globals = {
        'inventory': exec_inventory,  # Player can access/modify this
        'balance': balance_wrapper,  # Player can access/modify this (via [0])
        'current_selected_customer_data': current_selected_customer_data,  # Player can access customer data
        'print': print,  # Allow player to use print() for debugging
        # You can add other helper functions here for higher levels
    }
    execution_locals = {}  # No specific local variables needed

    transaction_verified_correctly = False
    print(
        f"\n--- Executing player code for {current_selected_customer_data['name']} (Order ID: {current_selected_customer_data['id']}) ---")
    print(f"Player Code:\n{player_code}\n---")

    try:
        # Execute the player's code
        exec(player_code, execution_globals, execution_locals)

        # After execution, retrieve updated values from the execution environment
        updated_inventory = execution_globals['inventory']
        updated_balance = execution_globals['balance'][0]  # Get the value from the list wrapper

        # --- VERIFICATION LOGIC ---
        verification_passed = True
        total_expected_gain = 0
        customer_order_items = current_selected_customer_data['order']

        # 1. Check if all ordered items were attempted to be deducted
        for item, qty_ordered in customer_order_items.items():
            # Check if item exists in game's master list (for price lookup)
            if item not in ALL_GAME_ITEMS:
                verification_passed = False
                tkinter.messagebox.showerror("Code Error",
                                             f"Logic Error: Customer ordered '{item}' which is not a recognized item in your shop's master list.")
                break

                # Check if player's code somehow removed the item from inventory dict, or bad key
            if item not in updated_inventory or 'stock' not in updated_inventory[item]:
                verification_passed = False
                tkinter.messagebox.showerror("Code Error",
                                             f"Logic Error: Your code removed '{item}' from inventory or corrupted its structure.")
                break

            # Check if original stock was sufficient for this order
            original_stock_for_item = inventory.get(item, {}).get('stock', 0)
            if original_stock_for_item < qty_ordered:
                verification_passed = False
                tkinter.messagebox.showerror("Code Error",
                                             f"Logical Error: You tried to fulfill '{item}' ({qty_ordered}) but only had {original_stock_for_item} in stock originally. Cannot sell what you don't have!")
                break

                # Check if stock was correctly deducted
            expected_stock_after_deduction = original_stock_for_item - qty_ordered
            if updated_inventory[item]['stock'] != expected_stock_after_deduction:
                verification_passed = False
                tkinter.messagebox.showerror("Code Error",
                                             f"Logic Error: Stock for '{item}' is incorrect.\nExpected: {expected_stock_after_deduction}, Actual: {updated_inventory[item]['stock']}\n(Did you use `-=` and the correct quantity?)")
                break  # Stop if stock deduction is wrong

            # Calculate expected gain
            total_expected_gain += ALL_GAME_ITEMS[item]['price'] * qty_ordered

        # 2. Check if final balance is correct (only if item deductions passed)
        if verification_passed:
            expected_balance_after_sale = balance + total_expected_gain
            if updated_balance != expected_balance_after_sale:
                verification_passed = False
                tkinter.messagebox.showerror("Code Error",
                                             f"Logic Error: Balance is incorrect.\nExpected: ₱{expected_balance_after_sale}, Actual: ₱{updated_balance}\n(Did you correctly calculate total earnings and use `balance[0] += amount`?)")

        # 3. Check for unexpected deductions (player deducted items not in order, or extra items)
        if verification_passed:
            for item_name_in_inv, original_details in inventory.items():
                original_stock = original_details['stock']
                current_stock_after_player_code = updated_inventory.get(item_name_in_inv, {}).get('stock',
                                                                                                  original_stock)

                # If item was not in order but stock changed OR stock changed more than ordered
                if (
                        item_name_in_inv not in customer_order_items and current_stock_after_player_code != original_stock) or \
                        (item_name_in_inv in customer_order_items and current_stock_after_player_code < (
                                original_stock - customer_order_items[item_name_in_inv])):
                    verification_passed = False
                    tkinter.messagebox.showerror("Code Error",
                                                 f"Logic Error: You deducted '{item_name_in_inv}' which was NOT in the customer's order, or you deducted too many items.")
                    break  # Stop if unexpected deduction

        # --- Final Outcome based on Verification ---
        if verification_passed:
            tkinter.messagebox.showinfo("Code Correct!",
                                        "Your Python code executed successfully and the transaction logic is correct!\n\nNow, click 'Complete Sale' to finalize.")
            # Apply changes to actual global game state immediately upon successful verification
            inventory.update(updated_inventory)
            balance = updated_balance

            if btn_complete_sale_ref:
                btn_complete_sale_ref.config(state='normal')  # Enable Complete Sale button
        else:
            # If verification failed, the error message would have already been shown by messagebox.showerror
            if btn_complete_sale_ref:
                btn_complete_sale_ref.config(state='disabled')

    except SyntaxError as e:
        tkinter.messagebox.showerror("Syntax Error",
                                     f"Your Python code has a SYNTAX ERROR:\n\n{e}\n\nPlease fix your code (check typos, missing colons, indentation).")
        if btn_complete_sale_ref:
            btn_complete_sale_ref.config(state='disabled')
    except KeyError as e:
        tkinter.messagebox.showerror("Key Error",
                                     f"Your Python code has a KEY ERROR:\n\nYou tried to access an item or dictionary key that doesn't exist or is misspelled: {e}\n\nRemember to use exact item names like 'health potion' and correct dictionary keys like 'stock' or 'price'.")
        if btn_complete_sale_ref:
            btn_complete_sale_ref.config(state='disabled')
    except TypeError as e:
        tkinter.messagebox.showerror("Type Error",
                                     f"Your Python code has a TYPE ERROR:\n\n{e}\n\nCheck if you're performing operations on the wrong type of data (e.g., adding a string to a number, or using `balance` without `[0]` if it's a list).")
        if btn_complete_sale_ref:
            btn_complete_sale_ref.config(state='disabled')
    except Exception as e:
        # Catch any other unexpected errors
        tkinter.messagebox.showerror("Runtime Error",
                                     f"An unexpected PYTHON RUNTIME ERROR occurred:\n\n{e}\n\nReview your code carefully.")
        if btn_complete_sale_ref:
            btn_complete_sale_ref.config(state='disabled')


# --- FUNCTIONS TO MANAGE UI STATE AND GAME PROGRESSION ---

def reset_transaction_ui_and_customers():
    """
    Clears the Handle Order section, resets buttons, and refreshes customer display.
    This is called after a successful 'Complete Sale'.
    """
    global customer_order_display_textbox, python_command_textbox, btn_complete_sale_ref, all_serve_buttons
    global current_selected_customer_data, active_customers

    # 1. Clear Handle Order section UI
    if customer_order_display_textbox:
        customer_order_display_textbox.config(state='normal')
        customer_order_display_textbox.delete('1.0', tk.END)
        customer_order_display_textbox.config(state='disabled')
    if python_command_textbox:
        python_command_textbox.delete('1.0', tk.END)
    if btn_complete_sale_ref:
        btn_complete_sale_ref.config(state='disabled')  # Disable 'Complete Sale' again

    # 2. Reset the currently selected customer data
    current_selected_customer_data = None

    # 3. Reset all serve buttons to 'Serve' and ensure they are enabled (will be handled by populate_customer_cards)
    all_serve_buttons.clear()  # Clear references, as populate_customer_cards will recreate them

    # 4. Bring in a new customer (if space allows, for actual gameplay)
    if len(active_customers) < MAX_CUSTOMERS:  # Check if there's space for a new customer
        new_customer = generate_customer()
        if new_customer:
            active_customers.append(new_customer)
            print(f"New customer '{new_customer['name']}' arrived!")

    # 5. Refresh the customer display (regenerate all customer cards based on active_customers)
    populate_customer_cards()


def complete_sale_command():
    """
    Called when the 'Complete Sale' button is pressed.
    Finalizes the transaction by removing the customer and resetting the UI.
    Assumes 'run_code_command' has already verified and applied changes to global state.
    """
    global active_customers, current_selected_customer_data

    if current_selected_customer_data:
        # Find and remove the served customer from the active list
        customer_id_to_remove = current_selected_customer_data['id']
        active_customers = [cust for cust in active_customers if cust['id'] != customer_id_to_remove]

        tkinter.messagebox.showinfo("Sale Complete!", f"Successfully served {current_selected_customer_data['name']}!")
        print(f"Customer {current_selected_customer_data['name']} served and removed.")

        # Reset the UI and potentially bring in new customers
        reset_transaction_ui_and_customers()
    else:
        tkinter.messagebox.showwarning("No Active Transaction", "No customer selected or transaction in progress.")


def populate_customer_cards():
    """
    Clears existing customer cards and repopulates them from active_customers.
    Fills remaining slots with mock customers for display if active_customers is less than MAX_CUSTOMERS.
    """
    global all_serve_buttons, customer_cards_container, mock_customers  # Need access to these globals

    # Clear all existing cards from the UI
    for widget in customer_cards_container.winfo_children():
        widget.destroy()
    all_serve_buttons.clear()  # Clear list of button references for new ones

    # Prepare list of customers to display (actual active + mock fillers)
    display_customers_list = list(active_customers)  # Start with actual active customers

    # If active_customers is less than MAX_CUSTOMERS, fill remaining slots with mock data
    if len(display_customers_list) < MAX_CUSTOMERS:
        num_mock_needed = MAX_CUSTOMERS - len(display_customers_list)
        # Create a pool of mock customers not currently active to avoid ID conflicts for display
        # (This is just for UI display, not adding to actual game state yet)
        available_mock = [c for c in mock_customers if c['id'] not in [ac['id'] for ac in active_customers]]
        random.shuffle(available_mock)
        display_customers_list.extend(available_mock[:num_mock_needed])

    # Ensure we only display up to MAX_CUSTOMERS slots
    display_customers_list = display_customers_list[:MAX_CUSTOMERS]

    # Loop through the display list to create and pack each customer card
    for i, customer_data in enumerate(display_customers_list):
        # Configure grid column for this card within customer_cards_container
        customer_cards_container.grid_columnconfigure(i, weight=1)
        customer_cards_container.grid_rowconfigure(0, weight=1)  # Ensure row can expand

        card = ttk.Frame(customer_cards_container, relief="ridge", borderwidth=1)
        card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")  # Cards fill their grid cells

        # Display customer details on the card
        details_text = f"{customer_data['name']} ({customer_data['type']})\n"
        details_text += "Order:\n"
        display_items = list(customer_data['order'].items())[:3]  # Show first few items on the card
        for item, qty in display_items:
            details_text += f"  {qty} {item.title()}\n"
        if len(customer_data['order']) > 3:
            details_text += "  ..."

        tk.Label(card, text=details_text, wraplength=120, justify="left").pack(expand=True, fill="both", padx=5, pady=2)

        # Create and configure the Serve Button
        serve_button = ttk.Button(card, text="Serve")
        serve_button.pack(side="bottom", pady=5)

        # Assign the command using lambda to capture current customer_data and the button reference
        serve_button.config(
            command=lambda data=customer_data, btn=serve_button: serve_customer_and_update_buttons(data, btn))

        # Store the button reference in the global list for later state management
        all_serve_buttons.append(serve_button)


def create_main_ui():
    # Declare global variables that will be assigned widget references within this function
    global customer_order_display_textbox, python_command_textbox, btn_complete_sale_ref, all_serve_buttons, customer_cards_container

    root = tk.Tk()
    root.title("Script & Serve: Python Shop")
    # --- GLOBAL WINDOW SIZE ---
    root_width = 1200
    root_height = 700
    root.geometry(f"{root_width}x{root_height}")
    root.resizable(False, False)  # Keep it fixed so user can't stretch it

    # --- INITIAL GAME SETUP (Populate inventory and initial customers) ---
    unlock_level_items(player_level, inventory)  # Populate initial inventory based on current level

    # Initialize active_customers list with some random customers at startup
    for _ in range(2):  # Start with 2 random customers in queue
        new_customer = generate_customer()
        if new_customer:
            active_customers.append(new_customer)
    # --- END INITIAL GAME SETUP ---

    # --- CONFIGURATION VARIABLES (ADJUST THESE NUMBERS!) ---
    # These are the main dimensions you'll change to customize the layout.

    # 1. Left Sidebar
    sidebar_width_config = 160  # Width of the left sidebar

    # 2. Customers Section (at the bottom of the right side)
    customers_height_config = 200  # Height of the entire customers panel

    # 3. Handle Order Section (top right)
    handle_order_width_config = 350  # Width of the "Handle Order" panel

    # 4. Shop Image (the remaining space, but scaled to this size)
    shop_img_display_width = 650  # Actual width the shop image will be drawn at
    shop_img_display_height = 480  # Actual height the shop image will be drawn at

    # --- END CONFIGURATION VARIABLES ---

    # --- 1. Left Sidebar Frame ---
    sidebar_frame = ttk.Frame(root, relief="solid", borderwidth=1, width=sidebar_width_config)
    sidebar_frame.pack(side="left", fill="y", padx=5, pady=5)  # Packs to the left, fills vertical space
    sidebar_frame.pack_propagate(False)  # Crucial: Prevents sidebar from resizing based on its contents

    # --- Image Logo ---
    logo_frame_size = 100
    logo_frame = ttk.Frame(sidebar_frame, relief="flat", borderwidth=0,
                           width=logo_frame_size, height=logo_frame_size)
    logo_frame.pack(pady=15, padx=10, fill="x")
    logo_frame.pack_propagate(False)

    try:
        logo_img_path = 'logo.png'  # Ensure this path is correct
        logo_img = Image.open(logo_img_path)
        logo_display_size_in_frame = 80
        logo_img_resized = logo_img.resize((logo_display_size_in_frame, logo_display_size_in_frame),
                                           Image.Resampling.NEAREST)
        logo_img_tk = ImageTk.PhotoImage(logo_img_resized)
        logo_label = tk.Label(logo_frame, image=logo_img_tk)
        logo_label.image = logo_img_tk
        logo_label.pack(expand=True, anchor="center")
    except FileNotFoundError:
        print(f"ERROR: Logo image '{logo_img_path}' was NOT FOUND! Check path and filename.")
        placeholder_label = tk.Label(logo_frame, text="[Logo Not Found]\n(Check filename/path!)", fg="red")
        placeholder_label.pack(expand=True, fill="both")
    except Exception as e:
        print(f"AN UNEXPECTED ERROR occurred while loading or displaying the logo: {e}")
        placeholder_label = tk.Label(logo_frame, text=f"[Logo Error]\n{e}", fg="red")
        placeholder_label.pack(expand=True, fill="both")

    # --- Sidebar Buttons ---
    btn_inventory = ttk.Button(sidebar_frame, text="Inventory", width=15)
    btn_inventory.pack(pady=5, padx=10)
    btn_sales = ttk.Button(sidebar_frame, text="Sales", width=15)
    btn_sales.pack(pady=5, padx=10)
    btn_commands = ttk.Button(sidebar_frame, text="Commands", width=15)
    btn_commands.pack(pady=5, padx=10)
    ttk.Frame(sidebar_frame).pack(expand=True, fill="y")

    # --- 2. Right Main Content Area ---
    right_main_content_area_frame = ttk.Frame(root, relief="solid", borderwidth=1)
    right_main_content_area_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

    # --- 2a. Customers Frame (Bottom of Right Main Content Area - Fixed Height) ---
    customers_frame = ttk.Frame(right_main_content_area_frame, relief="solid", borderwidth=1,
                                height=customers_height_config)
    customers_frame.pack(side="bottom", fill="x", padx=5, pady=5)
    customers_frame.pack_propagate(False)

    lbl_customers_title = ttk.Label(customers_frame, text="Customers", font=("Arial", 12, "bold"))
    lbl_customers_title.pack(side="top", anchor="w", padx=5, pady=2)

    # This frame will hold the customer cards dynamically generated by populate_customer_cards()
    customer_cards_container = ttk.Frame(customers_frame)  # <<< Assign to GLOBAL here
    customer_cards_container.pack(fill="both", expand=True, padx=5, pady=5)

    # --- Initial Customer Card Population ---
    populate_customer_cards()  # Call to display the initial set of customers at startup

    # --- 2b. Top Section (Shop Image & Handle Order) ---
    top_section_frame = ttk.Frame(right_main_content_area_frame, relief="solid", borderwidth=1)
    top_section_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

    # Grid config for top_section_frame (contains shop image and handle order side-by-side)
    top_section_frame.grid_columnconfigure(0, weight=1)  # Shop Image column (flexible)
    top_section_frame.grid_columnconfigure(1, weight=0)  # Handle Order column (fixed by width_config)
    top_section_frame.grid_rowconfigure(0, weight=1)  # Only one row, flexible vertically

    # --- 2b.i. Handle Order Frame (Top Right - Fixed Width) ---
    handle_order_frame = ttk.Frame(top_section_frame, relief="ridge", borderwidth=2, width=handle_order_width_config)
    handle_order_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    handle_order_frame.grid_propagate(False)

    # Internal grid for Handle Order frame content
    handle_order_frame.grid_rowconfigure(0, weight=0)  # "Handle Order" label
    handle_order_frame.grid_rowconfigure(1, weight=0)  # "Customer Order" label
    handle_order_frame.grid_rowconfigure(2, weight=1)  # Customer Order Textbox (make it expand vertically)
    handle_order_frame.grid_rowconfigure(3, weight=0)  # Python Instructions Label
    handle_order_frame.grid_rowconfigure(4, weight=0)  # "Enter python command" label
    handle_order_frame.grid_rowconfigure(5, weight=1)  # Python command Textbox (make it expand vertically)
    handle_order_frame.grid_rowconfigure(6, weight=0)  # Run Code button
    handle_order_frame.grid_rowconfigure(7, weight=0)  # Complete Sale button
    handle_order_frame.grid_rowconfigure(8, weight=1)  # Spacer row at the bottom
    handle_order_frame.grid_columnconfigure(0, weight=1)

    lbl_handle_order = ttk.Label(handle_order_frame, text="Handle Order", font=("Arial", 14, "bold"))
    lbl_handle_order.grid(row=0, column=0, pady=5)

    # --- Customer Order Display Widgets ---
    lbl_customer_order = ttk.Label(handle_order_frame, text="Customer Order")
    lbl_customer_order.grid(row=1, column=0, sticky="nw", padx=10, pady=(0, 2))

    customer_order_display_textbox = tk.Text(handle_order_frame, wrap="word", height=6)
    customer_order_display_textbox.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
    customer_order_display_textbox.config(state='disabled')

    # --- Python Instructions Label ---
    lbl_python_instructions = ttk.Label(handle_order_frame,
                                        text="Instructions: Use 'inventory', 'balance', 'current_selected_customer_data' variables.\nExample: inventory['health potion']['stock'] -= 1",
                                        wraplength=handle_order_width_config - 20,
                                        justify="left",
                                        font=("Arial", 8, "italic"))
    lbl_python_instructions.grid(row=3, column=0, sticky="nw", padx=10, pady=(5, 2))

    # --- Python Command Input ---
    lbl_enter_command = ttk.Label(handle_order_frame, text="Enter python command")
    lbl_enter_command.grid(row=4, column=0, sticky="nw", padx=10, pady=(0, 2))

    python_command_textbox = tk.Text(handle_order_frame, wrap="word", height=10)
    python_command_textbox.grid(row=5, column=0, sticky="nsew", padx=10, pady=5)

    btn_run_code = ttk.Button(handle_order_frame, text="Run Code", command=run_code_command)
    btn_run_code.grid(row=6, column=0, pady=5, sticky="ew", padx=10)

    btn_complete_sale_ref = ttk.Button(handle_order_frame, text="Complete Sale",
                                       command=complete_sale_command)  # Connected to function
    btn_complete_sale_ref.grid(row=7, column=0, pady=5, sticky="ew", padx=10)
    btn_complete_sale_ref.config(state='disabled')

    # --- 2b.ii. Shop Image Frame (Top Left - Fills Remaining Space) ---
    shop_image_frame = ttk.Frame(top_section_frame, relief="ridge", borderwidth=2)
    shop_image_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

    # --- Fixed Image Loading ---
    img_path = 'storeimage.jpg'  # Ensure this path is correct
    try:
        original_img = Image.open(img_path)
        resized_img = original_img.resize((shop_img_display_width, shop_img_display_height), Image.Resampling.NEAREST)
        shop_image_tk = ImageTk.PhotoImage(resized_img)

        shop_image_label = tk.Label(shop_image_frame, image=shop_image_tk)
        shop_image_label.image = shop_image_tk
        shop_image_label.pack(expand=True, anchor="center")

    except FileNotFoundError:
        print(f"Error: Image file '{img_path}' not found. Please ensure it's in the correct directory.")
        placeholder_label = tk.Label(shop_image_frame, text="[Shop Image Placeholder]\n(Image not found)",
                                     bg="lightgray", fg="red")
        placeholder_label.pack(expand=True, fill="both")
    except Exception as e:
        print(f"Error loading image: {e}")
        placeholder_label = tk.Label(shop_image_frame, text=f"[Shop Image Placeholder]\nError: {e}", bg="lightgray",
                                     fg="red")
        placeholder_label.pack(expand=True, fill="both")

    root.mainloop()


if __name__ == "__main__":
    create_main_ui()