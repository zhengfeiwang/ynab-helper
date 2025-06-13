import os
import requests
from dotenv import load_dotenv

def test_token_directly():
    # Load environment variables
    load_dotenv()
    
    # Get API token
    api_token = os.getenv("YNAB_API_TOKEN")
    
    if not api_token:
        print("❌ Error: YNAB_API_TOKEN not found in .env file")
        return
    
    print("Testing YNAB API token directly...")
    print(f"Token length: {len(api_token)} characters")
    print(f"Token starts with: {api_token[:4]}...")
    
    # Test the token with a simple API call
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    
    try:
        # First, try to get budgets
        print("\nTesting /budgets endpoint...")
        response = requests.get(
            "https://api.ynab.com/v1/budgets",
            headers=headers
        )
        
        print(f"Status code: {response.status_code}")
        print("Response headers:")
        for key, value in response.headers.items():
            print(f"  {key}: {value}")
        
        if response.status_code == 200:
            print("\n✓ API token is valid!")
            data = response.json()
            budgets = data["data"]["budgets"]
            print(f"\nFound {len(budgets)} budget(s):")
            for budget in budgets:
                print(f"- {budget['name']} (ID: {budget['id']})")
        else:
            print("\nResponse body:")
            print(response.text)
            
            if response.status_code == 401:
                print("\nPossible issues:")
                print("1. Token might be expired")
                print("2. Token might have been revoked")
                print("3. Token might be malformed")
                print("\nPlease try:")
                print("1. Generate a new token at https://app.ynab.com/settings/developer")
                print("2. Make sure to copy the entire token")
                print("3. Check for any extra spaces or newlines in the .env file")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify the YNAB API is accessible")
        print("3. Make sure the token is in the correct format")

if __name__ == "__main__":
    test_token_directly() 