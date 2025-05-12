import csv
from datetime import datetime


# Function to load CSV data into a list
def load_csv(filename):
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)
    return data


# Inventory class to manage and query items
class Inventory:
    def __init__(self, manufacturer_filename, price_filename, service_date_filename):
        self.inventory = {}
        self.load_inventory(manufacturer_filename, price_filename, service_date_filename)

    # Load data from CSV files
    def load_inventory(self, manufacturer_filename, price_filename, service_date_filename):
        manufacturer_data = load_csv(manufacturer_filename)
        price_data = load_csv(price_filename)
        service_date_data = load_csv(service_date_filename)        
        
        # Create a dictionary of items using item_id as keys
        for item in manufacturer_data:
            item_id, manufacturer, item_type, damaged = item
            self.inventory[item_id] = {
                'manufacturer': manufacturer,
                'item_type': item_type,
                'damaged': damaged
            }

        # Add price information to the items
        for item in price_data:
            item_id, price = item
            self.inventory[item_id]['price'] = float(price)

        # Convert service date strings to datetime objects and add to the items
        for item in service_date_data:
            item_id, service_date_str = item
            self.inventory[item_id]['service_date'] = datetime.strptime(service_date_str, '%m/%d/%Y')

    # Query items based on manufacturer and item type
    def query_item(self, manufacturer, item_type):
        
        matching_items = [(item_id, item) for item_id, item in self.inventory.items()
                          if manufacturer.lower() in item['manufacturer'].lower()
                          and item_type.lower() in item['item_type'].lower()
                          and item['service_date'] >= datetime.now()
                          and item['damaged'] != 'damaged']        
        return matching_items


# Main function to interact with the user
def main():
    # Initialize the inventory dictionary using CSV data
    inventory_dict = Inventory("ManufacturerList.csv", "PriceList.csv", "ServiceDatesList.csv")

    while True:
        query = input("Enter the manufacturer and item type or q to quit: ")
        if query.lower() == 'q':
            break

        query_parts = query.split()

        if len(query_parts) != 2:
            print("Invalid input format. Please enter both the manufacturer and item type.")
            continue

        manufacturer, item_type = query_parts

        # Query the inventory for matching items
        items = inventory_dict.query_item(manufacturer, item_type)

        if not items:
            print("No such item in inventory\n")
            continue

        # Sort items by price and choose the highest-priced item
        items.sort(key=sort_by_price, reverse=True)
        chosen_item_id, chosen_item = items[0]

        # Print the chosen item details
        print('---------------------------------------------------------------')
        print(f"Your item is: {chosen_item_id}, {chosen_item['manufacturer']}, "
              f"{chosen_item['item_type']}, ${chosen_item['price']}")

        close_price_items = [(item_id, item) for item_id, item in inventory_dict.inventory.items()
                             if item['manufacturer'].lower() != manufacturer.lower()
                             and item['item_type'].lower() == item_type.lower()
                             and item['service_date'] >= datetime.now()
                             and item['damaged'] != 'damaged']

        # Find and print a similar item with close price
        close_price_items.sort(key=sort_by_price, reverse=True)

        if close_price_items:
            similar_item_id, similar_item = close_price_items[0]
            print(f"You may also consider similar item: {similar_item_id}, {similar_item['manufacturer']}, "
                  f"{similar_item['item_type']}, ${similar_item['price']}")

        print('---------------------------------------------------------------\n')


# Function to sort items by price
def sort_by_price(item):
    return item[1]["price"]

if __name__ == "__main__":
    main()