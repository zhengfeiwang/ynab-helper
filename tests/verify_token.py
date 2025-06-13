import os
from dotenv import load_dotenv
import requests

def verify_token():
    # Load environment variables
    load_dotenv()
    
    # Get API token
    api_token = os.getenv("YNAB_API_TOKEN")
    
    if not api_token:
        print("❌ Error: YNAB_API_TOKEN not found in .env file")
        print("\nPlease create a .env file in the root directory with:")
        print("YNAB_API_TOKEN=your_token_here")
        return
    
    # Test the token with a simple API call
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            "https://api.ynab.com/v1/budgets",
            headers=headers
        )
        
        if response.status_code == 200:
            print("✓ API token is valid!")
            data = response.json()
            budgets = data["data"]["budgets"]
            print(f"\nFound {len(budgets)} budget(s):")
            for budget in budgets:
                print(f"- {budget['name']} (ID: {budget['id']})")
        else:
            print(f"❌ Error: API request failed with status code {response.status_code}")
            print("\nResponse body:")
            print(response.text)
            print("\nTroubleshooting tips:")
            print("1. Make sure you copied the entire token correctly")
            print("2. Verify the token hasn't expired")
            print("3. Check if you have access to the YNAB API")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify the YNAB API is accessible")
        print("3. Make sure the token is in the correct format")

if __name__ == "__main__":
    verify_token() 