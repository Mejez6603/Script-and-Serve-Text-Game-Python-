import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# GLOBAL variable to hold a reference to the text box for customer order display
# This allows the 'serve_customer_ui_action' function to update it.
customer_order_display_textbox = None
python_command_textbox = None  # Also need a ref to clear python command box
current_selected_customer_data = None  # To store the data of the customer currently being served


# --- FUNCTIONS TO BE CALLED BY UI ACTIONS ---

def serve_customer_ui_action(customer_data):
    """
    This function is called when a 'Serve' button on a customer card is clicked.
    It updates the 'Customer Order' display in the 'Handle Order' frame.
    """
    global customer_order_display_textbox, python_command_textbox, current_selected_customer_data

    if customer_order_display_textbox:
        current_selected_customer_data = customer_data  # Store the customer data

        # Format the customer order details
        order_details = f"Customer: {customer_data['name']}\n"
        order_details += "Order:\n"
        for item, qty in customer_data['order'].items():
            order_details += f"  - {qty} {item.title()}\n"

        # Update the read-only textbox
        customer_order_display_textbox.config(state='normal')  # Enable writing
        customer_order_display_textbox.delete('1.0', tk.END)  # Clear previous content
        customer_order_display_textbox.insert(tk.END, order_details)  # Insert new content
        customer_order_display_textbox.config(state='disabled')  # Disable writing again (read-only)

        # Clear the python command box for new input
        if python_command_textbox:
            python_command_textbox.delete('1.0', tk.END)

        print(f"Customer {customer_data['name']}'s order loaded for handling.")
    else:
        print("Error: Customer order display textbox not initialized.")


# --- End of UI Action Functions ---

def create_main_ui():
    global customer_order_display_textbox, python_command_textbox  # Declare globals

    root = tk.Tk()
    root.title("Script & Serve: Python Shop")
    root_width = 1200
    root_height = 700
    root.geometry(f"{root_width}x{root_height}")
    root.resizable(False, False)

    # --- CONFIGURATION VARIABLES ---
    sidebar_width_config = 160
    customers_height_config = 280  # Adjusted as per your preference
    handle_order_width_config = 200  # Adjusted as per your preference
    shop_img_display_width = 800  # Adjusted as per your preference
    shop_img_display_height = 400
    # --- END CONFIGURATION VARIABLES ---

    # --- 1. Left Sidebar Frame ---
    sidebar_frame = ttk.Frame(root, relief="solid", borderwidth=1, width=sidebar_width_config)
    sidebar_frame.pack(side="left", fill="y", padx=5, pady=5)
    sidebar_frame.pack_propagate(False)

    # Image Logo
    logo_frame_size = 100
    logo_frame = ttk.Frame(sidebar_frame, relief="flat", borderwidth=0,
                           width=logo_frame_size, height=logo_frame_size)
    logo_frame.pack(pady=15, padx=10, fill="x")
    logo_frame.pack_propagate(False)

    try:
        logo_img_path = 'logo.png'
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

    # Sidebar Buttons
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

    # Container for dynamically generated customer cards
    customer_cards_container = ttk.Frame(customers_frame)
    customer_cards_container.pack(fill="both", expand=True, padx=5, pady=5)

    # --- DYNAMIC CUSTOMER CARD GENERATION (Mock Data for UI Testing) ---
    # In your actual game, you'd loop through gs.active_customers here.
    mock_customers = [
        {"id": 101, "name": "Sir Reginald", "type": "Knight", "order": {"health potion": 3, "leather armor": 1}},
        {"id": 102, "name": "Apprentice Lyra", "type": "Mage", "order": {"mana elixir": 2, "scroll of fireball": 1}},
        {"id": 103, "name": "Goblin Gnarl", "type": "Raider", "order": {"gold coin pouch": 5}},
        {"id": 104, "name": "Lady Elara", "type": "Noble", "order": {"healing salve": 2, "enchanted amulet": 1}}
    ]

    for i, customer_data in enumerate(mock_customers):
        customer_cards_container.grid_columnconfigure(i, weight=1)
        customer_cards_container.grid_rowconfigure(0, weight=1)

        card = ttk.Frame(customer_cards_container, relief="ridge", borderwidth=1)
        card.grid(row=0, column=i, padx=5, pady=5, sticky="nsew")

        # Customer details label
        details_text = f"{customer_data['name']}\n"
        details_text += "Order:\n"
        for item, qty in customer_data['order'].items():
            details_text += f"  {qty} {item.title()}\n"  # Shorter order display

        tk.Label(card, text=details_text, wraplength=120, justify="left").pack(expand=True, fill="both", padx=5, pady=2)

        # Serve Button
        # The command uses a lambda to "capture" the current customer_data for the button
        serve_button = ttk.Button(card, text="Serve", command=lambda data=customer_data: serve_customer_ui_action(data))
        serve_button.pack(side="bottom", pady=5)

    # --- 2b. Top Section (Shop Image & Handle Order) ---
    top_section_frame = ttk.Frame(right_main_content_area_frame, relief="solid", borderwidth=1)
    top_section_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

    # Grid config for top_section_frame (contains shop image and handle order side-by-side)
    top_section_frame.grid_columnconfigure(0, weight=1)  # Shop Image column (flexible)
    top_section_frame.grid_columnconfigure(1, weight=0)  # Handle Order column (fixed by width_config)
    top_section_frame.grid_rowconfigure(0, weight=1)  # Only one row, flexible vertically

    # --- 2b.i. Handle Order Frame (Top Right - Fixed Width) ---
    handle_order_frame = ttk.Frame(top_section_frame, relief="ridge", borderwidth=2, width=handle_order_width_config)
    handle_order_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)  # Placed in fixed column 1
    handle_order_frame.grid_propagate(False)

    # Internal grid for Handle Order frame content
    # New rows added for Customer Order display
    handle_order_frame.grid_rowconfigure(0, weight=0)  # "Handle Order" label
    handle_order_frame.grid_rowconfigure(1, weight=0)  # "Customer Order" label (NEW)
    handle_order_frame.grid_rowconfigure(2, weight=1)  # Customer Order Textbox (NEW - make it expand)
    handle_order_frame.grid_rowconfigure(3, weight=0)  # "Enter python command" label (shifted)
    handle_order_frame.grid_rowconfigure(4, weight=1)  # Python command Textbox (shifted - make it expand)
    handle_order_frame.grid_rowconfigure(5, weight=0)  # Run Code button (shifted)
    handle_order_frame.grid_rowconfigure(6, weight=0)  # Complete Sale button (shifted)
    handle_order_frame.grid_rowconfigure(7, weight=1)  # Spacer row at the bottom
    handle_order_frame.grid_columnconfigure(0, weight=1)

    lbl_handle_order = ttk.Label(handle_order_frame, text="Handle Order", font=("Arial", 14, "bold"))
    lbl_handle_order.grid(row=0, column=0, pady=5)

    # --- NEW: Customer Order Display Widgets ---
    lbl_customer_order = ttk.Label(handle_order_frame, text="Customer Order")
    lbl_customer_order.grid(row=1, column=0, sticky="nw", padx=10, pady=(0, 2))

    customer_order_display_textbox = tk.Text(handle_order_frame, wrap="word", height=6)  # Set initial height
    customer_order_display_textbox.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
    customer_order_display_textbox.config(state='disabled')  # Make it read-only by default

    # --- Existing: Python Command Input ---
    lbl_enter_command = ttk.Label(handle_order_frame, text="Enter python command")
    lbl_enter_command.grid(row=3, column=0, sticky="nw", padx=10, pady=(0, 2))

    python_command_textbox = tk.Text(handle_order_frame, wrap="word", height=10)  # Using global var name
    python_command_textbox.grid(row=4, column=0, sticky="nsew", padx=10, pady=5)  # Make it expand with nsew

    btn_run_code = ttk.Button(handle_order_frame, text="Run Code")
    btn_run_code.grid(row=5, column=0, pady=5, sticky="ew", padx=10)

    btn_complete_sale = ttk.Button(handle_order_frame, text="Complete Order")
    btn_complete_sale.grid(row=6, column=0, pady=5, sticky="ew", padx=10)

    # --- 2b.ii. Shop Image Frame (Top Left - Fills Remaining Space) ---
    shop_image_frame = ttk.Frame(top_section_frame, relief="ridge", borderwidth=2)
    shop_image_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)  # Placed in flexible column 0

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