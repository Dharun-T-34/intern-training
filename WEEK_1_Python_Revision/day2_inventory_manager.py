# ─────────────────────────────────────────────────────────
#  DAY 2 — Inventory & Contact Manager
#  Uses: List, Tuple, Dictionary, Set, Comprehensions
# ─────────────────────────────────────────────────────────

# ── DATA STORE ───────────────────────────────────────────
# List of dictionaries — each item is one inventory record
inventory = []

# Set — tracks all unique categories automatically
categories = set()

# Tuple — column headers (fixed, never changes)
FIELDS = ("id", "name", "category", "price", "quantity")

# Dictionary — summary report cache
report_cache = {}

# ── ID GENERATOR ─────────────────────────────────────────
def generate_id():
    """Generate a simple auto-incrementing ID."""
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1


# ── ADD ITEM ─────────────────────────────────────────────
def add_item():
    print("\n── Add New Item ──")

    name = input("  Item name     : ").strip()
    if not name:
        print("  Name cannot be empty.")
        return

    category = input("  Category      : ").strip().lower()
    if not category:
        print("  Category cannot be empty.")
        return

    try:
        price    = float(input("  Price (₹)     : "))
        quantity = int(input("  Quantity      : "))
    except ValueError:
        print("  Invalid price or quantity.")
        return

    # Create a dictionary for this item
    item = {
        "id"      : generate_id(),
        "name"    : name,
        "category": category,
        "price"   : price,
        "quantity": quantity
    }

    inventory.append(item)       # add to list
    categories.add(category)     # set auto-removes duplicates

    print(f"\n  ✅ Item added with ID {item['id']}")


# ── VIEW ALL ITEMS ────────────────────────────────────────
def view_all():
    print("\n── All Inventory Items ──")

    if not inventory:
        print("  No items found.")
        return

    # Print using tuple FIELDS as headers
    print(f"\n  {'ID':<5} {'Name':<20} {'Category':<15} {'Price':>10} {'Qty':>6}")
    print("  " + "-" * 60)

    for item in inventory:
        print(f"  {item['id']:<5} {item['name']:<20} "
              f"{item['category']:<15} "
              f"₹{item['price']:>9.2f} {item['quantity']:>6}")

    print(f"\n  Total items: {len(inventory)}")
    print(f"  Categories : {', '.join(sorted(categories))}")


# ── SEARCH ITEM ───────────────────────────────────────────
def search_item():
    print("\n── Search Items ──")
    print("  1. Search by name")
    print("  2. Search by category")
    print("  3. Search by price range")
    choice = input("  Choose: ").strip()

    if choice == "1":
        keyword = input("  Enter name keyword: ").strip().lower()
        # List comprehension — filter by name
        results = [item for item in inventory
                   if keyword in item["name"].lower()]

    elif choice == "2":
        print(f"  Available categories: {', '.join(sorted(categories))}")
        cat = input("  Enter category: ").strip().lower()
        # List comprehension — filter by category
        results = [item for item in inventory
                   if item["category"] == cat]

    elif choice == "3":
        try:
            low  = float(input("  Min price (₹): "))
            high = float(input("  Max price (₹): "))
            # List comprehension — filter by price range
            results = [item for item in inventory
                       if low <= item["price"] <= high]
        except ValueError:
            print("  Invalid price.")
            return
    else:
        print("  Invalid choice.")
        return

    # Show results
    if not results:
        print("  No items found.")
        return

    print(f"\n  Found {len(results)} item(s):")
    print(f"  {'ID':<5} {'Name':<20} {'Category':<15} {'Price':>10} {'Qty':>6}")
    print("  " + "-" * 60)
    for item in results:
        print(f"  {item['id']:<5} {item['name']:<20} "
              f"{item['category']:<15} "
              f"₹{item['price']:>9.2f} {item['quantity']:>6}")


# ── UPDATE ITEM ───────────────────────────────────────────
def update_item():
    print("\n── Update Item ──")

    try:
        item_id = int(input("  Enter item ID to update: "))
    except ValueError:
        print("  Invalid ID.")
        return

    # Find the item in the list
    item = None
    for i in inventory:
        if i["id"] == item_id:
            item = i
            break

    if not item:
        print(f"  No item found with ID {item_id}.")
        return

    print(f"\n  Current details: {item}")
    print("\n  What to update?")
    print("  1. Name")
    print("  2. Category")
    print("  3. Price")
    print("  4. Quantity")

    choice = input("  Choose: ").strip()

    if choice == "1":
        item["name"] = input("  New name: ").strip()
    elif choice == "2":
        new_cat = input("  New category: ").strip().lower()
        categories.add(new_cat)   # add new category to set
        item["category"] = new_cat
    elif choice == "3":
        try:
            item["price"] = float(input("  New price (₹): "))
        except ValueError:
            print("  Invalid price.")
            return
    elif choice == "4":
        try:
            item["quantity"] = int(input("  New quantity: "))
        except ValueError:
            print("  Invalid quantity.")
            return
    else:
        print("  Invalid choice.")
        return

    print("  ✅ Item updated successfully.")


# ── DELETE ITEM ───────────────────────────────────────────
def delete_item():
    print("\n── Delete Item ──")

    try:
        item_id = int(input("  Enter item ID to delete: "))
    except ValueError:
        print("  Invalid ID.")
        return

    # List comprehension — keep all items EXCEPT the one to delete
    original_count = len(inventory)
    remaining = [item for item in inventory if item["id"] != item_id]

    if len(remaining) == original_count:
        print(f"  No item found with ID {item_id}.")
        return

    # Confirm before deleting
    confirm = input(f"  Delete item ID {item_id}? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Deletion cancelled.")
        return

    # Replace inventory contents
    inventory.clear()
    inventory.extend(remaining)

    # Rebuild categories set from remaining items
    categories.clear()
    categories.update(item["category"] for item in inventory)

    print("  ✅ Item deleted.")


# ── REPORTS ──────────────────────────────────────────────
def show_report():
    print("\n── Inventory Report ──")

    if not inventory:
        print("  No data to report.")
        return

    # Dictionary comprehension — total quantity per category
    qty_by_cat = {
        cat: sum(item["quantity"] for item in inventory
                 if item["category"] == cat)
        for cat in categories
    }

    # Dictionary comprehension — total value per category
    value_by_cat = {
        cat: sum(item["price"] * item["quantity"] for item in inventory
                 if item["category"] == cat)
        for cat in categories
    }

    # List comprehension — low stock items (quantity < 5)
    low_stock = [item["name"] for item in inventory
                 if item["quantity"] < 5]

    # List comprehension — expensive items (price > 1000)
    expensive = [item["name"] for item in inventory
                 if item["price"] > 1000]

    # Set comprehension — unique categories in use
    active_cats = {item["category"] for item in inventory}

    # Total inventory value
    total_value = sum(item["price"] * item["quantity"]
                      for item in inventory)

    print(f"\n  Total items     : {len(inventory)}")
    print(f"  Total value     : ₹{total_value:,.2f}")
    print(f"  Categories used : {', '.join(sorted(active_cats))}")

    print("\n  📊 Stock by category:")
    for cat, qty in sorted(qty_by_cat.items()):
        value = value_by_cat[cat]
        bar = "█" * min(qty, 20)
        print(f"    {cat:<15} {bar:<20} qty:{qty}  value:₹{value:,.2f}")

    if low_stock:
        print(f"\n  ⚠️  Low stock (< 5 units): {', '.join(low_stock)}")

    if expensive:
        print(f"  💰 Expensive items (> ₹1000): {', '.join(expensive)}")


# ── MAIN MENU ─────────────────────────────────────────────
def show_menu():
    print("\n" + "=" * 45)
    print("        INVENTORY MANAGER — Day 2")
    print("=" * 45)
    print("  1. Add item")
    print("  2. View all items")
    print("  3. Search items")
    print("  4. Update item")
    print("  5. Delete item")
    print("  6. View report")
    print("  0. Exit")
    print("=" * 45)


def main():
    # Pre-load some sample data so you can test immediately
    sample = [
        {"id": 1, "name": "Laptop",    "category": "electronics", "price": 55000, "quantity": 10},
        {"id": 2, "name": "Mouse",     "category": "electronics", "price": 500,   "quantity": 3},
        {"id": 3, "name": "Notebook",  "category": "stationery",  "price": 50,    "quantity": 50},
        {"id": 4, "name": "Pen",       "category": "stationery",  "price": 10,    "quantity": 100},
        {"id": 5, "name": "Desk",      "category": "furniture",   "price": 8000,  "quantity": 2},
    ]
    inventory.extend(sample)
    categories.update(item["category"] for item in sample)

    print("\nWelcome to Inventory Manager!")
    print("Sample data preloaded — start exploring.\n")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if   choice == "1": add_item()
        elif choice == "2": view_all()
        elif choice == "3": search_item()
        elif choice == "4": update_item()
        elif choice == "5": delete_item()
        elif choice == "6": show_report()
        elif choice == "0":
            print("\nGoodbye! Commit your work. 🚀")
            break
        else:
            print("Invalid choice — enter 0 to 6.")


if __name__ == "__main__":
    main()
