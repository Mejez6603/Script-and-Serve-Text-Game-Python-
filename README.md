# Script & Serve: Python Shop

![Script & Serve Logo](image_b3854a.png)

## 📜 Overview

Welcome to "Script & Serve: Python Shop"! This is a unique, interactive, and educational shop management game where you run a business in an adventure-themed world. Unlike traditional games, you fulfill customer orders by writing actual Python code! Every transaction becomes a fun coding challenge, designed to reinforce fundamental Python programming concepts. Master essential syntax, manage your inventory and balance, and build a thriving shop by serving adventurers in need of potions, armor, and more.

## ✨ Features

* **Interactive GUI:** A custom-built, fixed-layout graphical user interface (GUI) using Tkinter, providing a clear overview of your shop, customers, and the transaction area.
* **Python Code Execution:** Directly input and run Python code within the game's "Handle Order" panel to process customer requests.
* **Dynamic Order Fulfillment:** The game verifies your Python code to ensure it correctly deducts items from inventory and accurately updates your shop's balance.
* **Real-time Feedback:** Receive immediate pop-up messages for Python syntax errors, logical errors (e.g., trying to sell what you don't have, incorrect calculations), or successful transactions.
* **Customer Management:** See your queue of waiting customers, select one to "serve," and observe their status change (Serve, Serving, Waiting, Served).
* **Adventure Theme:** Immerse yourself in a fantasy setting, selling magical potions, powerful armor, ancient scrolls, and other fantastical goods.
* **Progressive Learning (Planned):** Designed for future expansion, with planned levels to introduce new items, more complex order scenarios, and introduce advanced Python concepts (e.g., loops, conditionals, functions).

## 💻 Technologies Used

* **Python 3.x:** The core programming language for the game logic and backend.
* **Tkinter:** Python's standard GUI toolkit, used for building the entire user interface.
* **Pillow (PIL Fork):** A powerful image processing library used for loading, resizing, and displaying game assets within the Tkinter GUI.
* **PyInstaller:** (Used for packaging) A tool that bundles a Python application and all its dependencies into a single standalone executable.

## 🚀 Getting Started

### System Requirements

* **Operating System:** Windows, macOS, Linux (Tkinter and Python are cross-platform).
* **Python Version:** Python 3.7 or higher is recommended.
    * *(Note: If using Python 3.13 beta, be aware of potential nuances with `global` keyword behavior.)*

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [ https://github.com/Mejez6603/Script-and-Serve-Text-Game-Python-.git]
    cd ScriptAndServe-Game
    ```
    

2.  **Install Dependencies:**
    ```bash
    pip install Pillow
    ```

3.  **Place Image Assets:** Ensure the following image files are located in the **same directory** as your `main.py` file:
    * `image_b3854a.png` (Logo for sidebar)
    * `image_b37a03.png` (Main shop background image)

## 🎮 Usage

### Running the Game

Simply execute the `main.py` file:

```bash
python main.py
````

### Gameplay Basics

1.  **Initial Setup:** Upon starting, your shop will open with an initial inventory and a few customers in the queue.
2.  **Serve a Customer:**
      * Click the **"Serve"** button on any customer card in the "Customers" section.
      * The selected customer's order details will appear in the "Customer Order" box on the right. The "Serve" button for that customer will change to "Serving," and others to "Waiting."
3.  **Write Your Python Code:**
      * In the "Enter python command" textbox, write Python code to process the order.
      * **Goal:** Deduct the ordered items from your `inventory` and add the correct earnings to your `balance`.
      * **Available Variables:** Your code has direct access to:
          * `inventory` (a dictionary holding your shop's stock and item details)
          * `balance` (a list containing your current money, accessed as `balance[0]`)
          * `current_selected_customer_data` (a dictionary with details about the customer you are currently serving, including their `order`)
      * **Example Code Pattern:**
        ```python
        total_earned = 0
        for item_name, quantity_ordered in current_selected_customer_data['order'].items():
            inventory[item_name]['stock'] -= quantity_ordered
            total_earned += quantity_ordered * inventory[item_name]['price']
        balance[0] += total_earned
        ```
4.  **Run Your Code:**
      * Click the **"Run Code"** button.
      * The game's internal system will execute and verify your code.
      * **Feedback:** You'll receive pop-up messages indicating:
          * `SyntaxError`: If your Python code has typos, incorrect indentation, etc.
          * `KeyError`: If you try to access an item or property that doesn't exist (e.g., an item not in your `inventory`, or a misspelled item name). This can also occur if you try to sell an item you haven't unlocked yet\!
          * `TypeError` / `RuntimeError`: For other logical or execution errors.
          * "Code Correct\!": If your code successfully and correctly processed the order according to game rules.
5.  **Complete the Sale:**
      * After your code is verified as "Code Correct\!", the **"Complete Sale"** button will become enabled.
      * Click it to finalize the transaction, remove the customer from the queue, and prepare for the next sale.

### Python Concepts You'll Practice

  * **Variables & Data Types:** Integers, strings, floats.
  * **Data Structures:** Dictionaries (accessing nested values), Lists (accessing `balance[0]`).
  * **Operators:** Arithmetic (`+`, `-`, `*`), Assignment (`=`, `+=`, `-=`).
  * **Control Flow (Future):** `for` loops, `if` statements.
  * **Error Handling:** Understanding and debugging common Python errors.

## 📁 Project Structure

```
ScriptAndServe-Game/
├── main.py                   # Main game logic and GUI
├── image_b3854a.png          # Logo image
├── image_b37a03.png          # Main shop background image
├── .gitignore                # Specifies files/folders Git should ignore
└── README.md                 # This documentation file
```

## 📦 Packaging for Distribution (Standalone Executable)

You can package this Python application into a standalone executable (`.exe` for Windows, executable for macOS/Linux) using `PyInstaller`. This allows users to run the game without needing to install Python or dependencies separately.

1.  **Install PyInstaller:**

    ```bash
    pip install pyinstaller
    ```

2.  **Navigate to Project Root:** Open your command prompt/terminal in the `ScriptAndServe-Game` directory.

3.  **Run PyInstaller:**

    ```bash
    pyinstaller --noconsole --onefile --add-data "image_b3854a.png:." --add-data "image_b37a03.png:." main.py
    ```

      * `--noconsole`: Prevents a console window from opening alongside the GUI (optional).
      * `--onefile`: Creates a single executable file (optional, otherwise creates a folder).
      * `--add-data "source:destination"`: Crucial for including your image files. It copies them into the executable's temporary directory at runtime.
      * `main.py`: Your main script.

4.  **Find the Executable:** The executable will be created in a `dist/` folder within your project directory.

## 📚 Changelog

**v1.0.0 (2025-06-27)**

  * Initial release with core GUI structure.
  * Implemented "Serve" button functionality to display customer orders.
  * "Run Code" button with `exec()` based Python code execution and comprehensive verification (syntax, key, type, logic errors).
  * "Complete Sale" button functionality to finalize transactions, remove customers, and refresh UI.
  * Dynamic customer generation and display.
  * Adventure-themed items and mock customer data.
  * Fixed-size layout for predictable UI experience.

## ⚠️ Troubleshooting

  * **`FileNotFoundError: 'image_name.png' not found`**:
      * Ensure the image file is in the **same directory** as your `main.py` script.
      * Double-check the spelling and capitalization of the filename in your code (e.g., `image_b3854a.png` vs `Image_B3854A.PNG`).
  * **`_tkinter.TclError: cannot use geometry manager pack inside ... which already has slaves managed by grid`**:
      * This means you've mixed `pack()` and `grid()` as direct children of the same parent widget. Review the `pack()` and `grid()` calls for the children of the frame mentioned in the error message. Ensure all children of a specific frame use *only one* geometry manager.
  * **`UnboundLocalError: cannot access local variable 'variable_name' where it is not associated with a value`**:
      * This happens when Python thinks a variable is local to a function (because it's assigned there later), but you try to read its value before it's assigned, and it's not declared `global`.
      * **Fix:** Ensure `global variable_name` is at the very top of the function where `variable_name` is used globally.
  * **`KeyError: 'item_name'`**:
      * This means you're trying to access a dictionary key (like an item name) that doesn't exist in the dictionary (e.g., `inventory["leather armor"]` when "leather armor" isn't in your `inventory` yet).
      * **Fix:** Check your spelling. Or, if it's a new item, ensure you've leveled up or unlocked it in the game's progression (`LEVEL_ITEM_UNLOCKS`).

## 🙏 Acknowledgments

A heartfelt thank you to:

  * The **open-source community** for developing Python, Tkinter, Pillow, and PyInstaller, which made this project possible.
  * **Nooby**
  * **Doc**
  * **Firelink**
  * **SBBC PC**
  * And, of course, to my beloved **dog and cat** for their constant companionship.

## 📄 License

This project is licensed under the [MIT License](https://www.google.com/search?q=LICENSE). You can create a `LICENSE` file in your repository and paste the MIT License text there.

