from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

def fill_search_field(driver, search_text):
    """
    Fill text field: Inputs specified text into a search field
    """
    try:
        # Wait for search field to be present
        search_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "search"))
        )
        # Clear existing text and enter new text
        search_field.clear()
        search_field.send_keys(search_text)
        print(f"Successfully filled search field with: {search_text}")
        return True
    except Exception as e:
        print(f"Error filling search field: {str(e)}")
        return False
    
def click_element(driver, element_xpath):
    """
    Simulates a mouse click on a specified element
    """
    try:
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, element_xpath))
        )
        element.click()
        print(f"Successfully clicked element")
        return True
    except Exception as e:
        print(f"Error clicking element: {str(e)}")
        return False

def toggle_checkbox(driver, checkbox_xpath, should_check=True):
    """
    Toggles checkbox state based on the should_check parameter
    """
    try:
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, checkbox_xpath))
        )
        current_state = checkbox.is_selected()
        
        if current_state != should_check:
            checkbox.click()
            print(f"Checkbox state changed to: {should_check}")
        else:
            print(f"Checkbox already in desired state: {should_check}")
        return True
    except Exception as e:
        print(f"Error toggling checkbox: {str(e)}")
        return False

def append_to_sheets(df, sheet_id, credentials_file):
    """
    Append DataFrame to Google Sheets
    """
    try:
        # Setup credentials
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Create service
        service = build('sheets', 'v4', credentials=credentials)
        
        # Prepare the data
        values = [df.columns.values.tolist()] + df.values.tolist()
        body = {
            'values': values
        }
        
        # Make the API call
        result = service.spreadsheets().values().append(
            spreadsheetId=sheet_id,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body=body
        ).execute()
        
        print(f"Data appended successfully! {result.get('updates').get('updatedCells')} cells updated.")
        return True
        
    except Exception as e:
        print(f"An error occurred while appending to sheets: {str(e)}")
        return False

def get_world_cup_data(num_rows=10):
    """
    Fetch World Cup finals data from Wikipedia using Selenium
    """
    driver = webdriver.Chrome()
    
    try:
       # Navigate to Wikipedia page
        driver.get('https://en.wikipedia.org/wiki/List_of_FIFA_World_Cup_finals')
        
         # 1. Fill text field (search)
        search_term = input("Enter search term (or press Enter to skip): ")
        if search_term:
            fill_search_field(driver, search_term)
        
        # 2. Click interaction (example: click on a specific year)
        click_year = input("Enter year to click on (or press Enter to skip): ")
        if click_year:
            year_xpath = f"//th[contains(text(), '{click_year}')]"
            click_element(driver, year_xpath)
        
        # 3. Checkbox interaction (example: toggle view options)
        show_details = input("Show additional details? (yes/no, or press Enter to skip): ").lower()
        if show_details in ['yes', 'no']:
            checkbox_xpath = "//input[@type='checkbox']"
            toggle_checkbox(driver, checkbox_xpath, should_check=(show_details == 'yes'))
        
        time.sleep(2)  
        
        years = []
        winners = []
        scores = []
        runners_up = []
        
        # Loop through rows
        for row in range(1, num_rows + 1):
            # XPath for each element
            year_xpath = f'//*[@id="mw-content-text"]/div[1]/table[4]/tbody/tr[{row}]/th'
            winner_xpath = f'//*[@id="mw-content-text"]/div[1]/table[4]/tbody/tr[{row}]/td[1]'
            score_xpath = f'//*[@id="mw-content-text"]/div[1]/table[4]/tbody/tr[{row}]/td[2]'
            runner_xpath = f'//*[@id="mw-content-text"]/div[1]/table[4]/tbody/tr[{row}]/td[3]'
            
            # Get data
            year = driver.find_element(By.XPATH, year_xpath).text
            winner = driver.find_element(By.XPATH, winner_xpath).text
            score = driver.find_element(By.XPATH, score_xpath).text
            runner = driver.find_element(By.XPATH, runner_xpath).text
            
            years.append(year)
            winners.append(winner)
            scores.append(score)
            runners_up.append(runner)
            
        return pd.DataFrame({
            'Year': years,
            'Winner': winners,
            'Score': scores,
            'Runners-up': runners_up
        })
        
    except Exception as e:
        print(f"An error occurred while scraping: {str(e)}")
        return pd.DataFrame()
        
    finally:
        driver.quit()

def get_filtered_data(df):
    """
    Detour: Add filtering options for the data
    """
    print("\nFilter options:")
    print("1. All data")
    print("2. Winners with more than 2 goals")
    print("3. Specific year range")
    
    choice = input("Choose filter option (1-3): ")
    
    if choice == '2':
        # Filter matches where winner scored more than 2 goals
        filtered_df = df[df['Score'].str.extract('(\d+)').astype(int) > 2]
        return filtered_df
    elif choice == '3':
        # Filter by year range
        start_year = int(input("Enter start year: "))
        end_year = int(input("Enter end year: "))
        filtered_df = df[df['Year'].astype(int).between(start_year, end_year)]
        return filtered_df
    else:
        return df

def add_custom_notes(df):
    """
    Fill text field: Add custom notes to the data
    """
    notes = []
    add_notes = input("\nWould you like to add notes for each match? (yes/no): ").lower()
    
    if add_notes == 'yes':
        for index, row in df.iterrows():
            note = input(f"Enter note for {row['Year']} match ({row['Winner']} vs {row['Runners-up']}): ")
            notes.append(note)
        df['Notes'] = notes
    
    return df

def select_columns(df):
    """
    Check Box: Select columns to export
    """
    print("\nAvailable columns:")
    for i, col in enumerate(df.columns, 1):
        print(f"{i}. {col}")
    
    selected = input("Enter column numbers to export (comma-separated) or 'all': ").lower()
    
    if selected != 'all':
        try:
            selected_indices = [int(x.strip())-1 for x in selected.split(',')]
            selected_columns = df.columns[selected_indices]
            return df[selected_columns]
        except:
            print("Invalid selection, exporting all columns")
            return df
    return df

def main():
    
    # Google Sheets configuration
    SHEET_ID = 'YOUR_SHEET_ID'
    CREDENTIALS_FILE = r'credentials_file_path'
    
    # Get World Cup data
    while True:
        try:
            num_rows = int(input("Enter the number of rows to fetch (1-22): "))
            if 1 <= num_rows <= 22:
                break
            print("Please enter a number between 1 and 22")
        except ValueError:
            print("Please enter a valid number")
    
    print(f"\nFetching {num_rows} rows of World Cup data...")
    df = get_world_cup_data(num_rows)
    
    # Display initial data
    print("\nInitial data:")
    print(df)
    
    # Detour: Apply filters
    df = get_filtered_data(df)
    
    # Fill text field: Add notes
    df = add_custom_notes(df)
    
    # Check Box: Select columns
    df = select_columns(df)
    
    # Display processed data
    print("\nProcessed data:")
    print(df)
    
    # Ask to append to Google Sheets
    while True:
        response = input("\nDo you want to append this data to Google Sheets? (yes/no): ").lower()
        if response in ['yes', 'no']:
            break
        print("Please enter 'yes' or 'no'")
    
    if response == 'yes':
        print("\nAppending data to Google Sheets...")
        success = append_to_sheets(df, SHEET_ID, CREDENTIALS_FILE)
        if success:
            print("Process completed successfully!")
        else:
            print("Failed to append data to Google Sheets.")
    else:
        print("\nData fetched but not appended to Google Sheets.")

if __name__ == "__main__":
    main()