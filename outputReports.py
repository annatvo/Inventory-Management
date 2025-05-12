import csv
from datetime import datetime
import os

# Item class to represent each item in the inventory
class Item:
    def __init__(self, item_id, manufacturer, item_type, price, service_date, condition):
        self.item_id = item_id
        self.manufacturer = manufacturer
        self.item_type = item_type
        self.price = price
        self.service_date = service_date
        self.condition = condition

# Create a folder for output reports
output_dir = r'..\manufactor\outputReports'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read data from a CSV file (ManufacturerList.csv) and create a dictionary of items
def read_csv_file(file_name):
    items_dict = {}
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            item_id = row[0]
            manufacturer = row[1]
            item_type = row[2]
            condition = 'damaged' if len(row) > 3 and row[3].lower() == 'damaged' else False
            items_dict[item_id] = Item(item_id, manufacturer, item_type, None, None, condition)
    return items_dict

# Read data from a CSV file (PriceList.csv)
def read_price_list(items_dict, file_name):
    with open(file_name, 'r') as csvfile: 
        reader = csv.reader(csvfile)
        for row in reader:
            item_id = row[0]
            price = float(row[1])
            if item_id in items_dict:
                items_dict[item_id].price = price

# Read data from a CSV file (ServiceDatesList.csv)
def read_service_dates(items_dict, file_name):
    with open(file_name, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Skip the header row
        for row in reader:
            # Read the item ID and service date
            item_id = row[0]
            service_date = row[1]
            # Update the service date in the items dictionary
            # Check if the item ID exists in the items dictionary
            if item_id in items_dict:
                items_dict[item_id].service_date = service_date

# Full inventory report sorted alphabetically by manufacturer
def full_inventory_report(items_dict):
    sorted_items = sorted(items_dict.values(), key=sorted_by_manufacturer)
    with open(os.path.join(output_dir, 'FullInventory.csv'), 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)
        # Write the header row
        writer.writerow(['Item ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date', 'Condition'])
        # Write the data rows
        for item in sorted_items:
            writer.writerow([item.item_id, item.manufacturer, item.item_type,
                             item.price, item.service_date, 'damaged' if item.condition else ''])

# Key function for sorting items
def sorted_by_manufacturer(item):
    return item.manufacturer

# Item type Inventory report sorted by item ID
def item_type_inventory_report(items_dict):
    item_types = {}
    for item in items_dict.values():
        if item.item_type not in item_types:
            item_types[item.item_type] = []
        item_types[item.item_type].append(item)

    for item_type, items_list in item_types.items():
        sorted_items = sorted(items_list, key=sorted_by_item_id)
        file_name = f'{item_type}Inventory.csv'
        with open(os.path.join(output_dir, file_name), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Item ID', 'Manufacturer', 'Price', 'Service Date', 'Condition'])

            for item in sorted_items:
                writer.writerow([item.item_id, item.manufacturer, item.price,
                                 item.service_date, 'damaged' if item.condition else ''])

# Key function for sorting items
def sorted_by_item_id(item):
    return item.item_id

# Past service date report sorted by service date from oldest to most recent
def past_service_date_inventory_report(items_dict):
    today = datetime.today()
    past_service = [item for item in items_dict.values()
                    if datetime.strptime(item.service_date, '%m/%d/%Y') < today]
    sorted_items = sorted(past_service, key=sorted_by_service_date)
    with open(os.path.join(output_dir, 'PastServiceDateInventory.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Item ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date', 'Condition'])
        for item in sorted_items:
            writer.writerow([item.item_id, item.manufacturer, item.item_type,
                             item.price, item.service_date, 'damaged' if item.condition else ''])

# Key function for sorting items
def sorted_by_service_date(item):
    return datetime.strptime(item.service_date, '%m/%d/%Y')

# Damage inventory report sorted by price from the most expensive to the least expensive
def damaged_inventory_report(items_dict):
    damaged_items = [item for item in items_dict.values() if item.condition]
    sorted_items = sorted(damaged_items, key=sorted_by_price, reverse=True)
    with open(os.path.join(output_dir, 'DamagedInventory.csv'), 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Item ID', 'Manufacturer', 'Item Type', 'Price', 'Service Date'])

        for item in sorted_items:
            writer.writerow([item.item_id, item.manufacturer, item.item_type,
                             item.price, item.service_date])

# Key function for sorting items
def sorted_by_price(item):
    return item.price

def main():
    # Read manufacturer list
    items = read_csv_file('F:/GitHub Projects/python/manufactor/ManufacturerList.csv')

    # Read price list
    read_price_list(items, 'F:/GitHub Projects/python/manufactor/PriceList.csv')

    # Read service dates list
    read_service_dates(items, 'F:/GitHub Projects/python/manufactor/ServiceDatesList.csv')

    # Create inventory reports
    full_inventory_report(items)
    item_type_inventory_report(items)
    past_service_date_inventory_report(items)
    damaged_inventory_report(items)

if __name__ == '__main__':
    main()
