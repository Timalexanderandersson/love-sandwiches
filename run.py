import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

def get_sales_data():
    """ 
    get sales input from the user 
    """
    while True:
        print("Please enter sales data from the last marker!")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
    
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data is valid.")
            break

    return sales_data        

def validate_data(values):
    """
    inside the try converts all the strings values into integers raised ValueErrorif string cant convert to int 
    or if there arent exactly 6 numbers
    """  
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
                print(f'Invalid data: {e}, please try again.\n')
                return False

    return True            


def update_worksheet(data, worksheet):
    """
    recive a list of integers to be inserted into a worksheet.
    update the relevant worksheet with the data provided.
    """
    print(f"surplus {worksheet} worksheet.\n") 
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f'{worksheet} updated successfully')


def calculate_surplus_data(sales_row):
    """
    calculate sales with stock and calculate the surplus for each item.
    positiv indicate waste
    negative indicate extra made when sold out
    """
    print("calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data

def get_last_5_enteries_sales():
    """
    collect colloums of data from sales worksheet. collecting the last 5 enetries of each sandwich and return the data as a list of a list.
    """
    sales = SHEET.worksheet('sales')
    columns = []
    for ind in range(1, 7):
          column = sales.col_values(ind)
          columns.append(column[-5:])
    return columns  


def calculate_stock_data(data):
    """
    calculate each average stock for each item type, adding 10%
    """
    print('Calculating stock data...\n')
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    return new_stock_data    



def main():
    """
    Run programs in the functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data,'surplus')
    sales_columns = get_last_5_enteries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to love sandwiches Data Automation")
main()    


