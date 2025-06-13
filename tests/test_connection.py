from ynab_client import YNABClient
from datetime import datetime, timedelta

def test_connection():
    print("Testing YNAB connection...")
    
    try:
        # Initialize client
        client = YNABClient()
        print("✓ Successfully initialized YNAB client")
        
        # Test getting accounts
        accounts = client.get_accounts()
        print(f"✓ Successfully retrieved {len(accounts)} accounts")
        
        # Test getting categories
        categories = client.get_categories()
        print(f"✓ Successfully retrieved {len(categories)} category groups")
        
        # Test getting red flag transactions
        transactions = client.get_red_flag_transactions(
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now()
        )
        print(f"✓ Successfully retrieved {len(transactions)} red-flagged transactions")
        
        if transactions:
            print("\nSample transaction:")
            sample = transactions[0]
            print(f"  Date: {sample.date}")
            print(f"  Payee: {sample.payee_name}")
            print(f"  Amount: ${sample.amount/1000:,.2f}")
            print(f"  Category: {sample.category_name}")
        
        print("\nAll tests passed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check if your YNAB API token is correct in the .env file")
        print("2. Verify your internet connection")
        print("3. Make sure you have access to your YNAB account")
        print("4. Check if the token has the necessary permissions")

if __name__ == "__main__":
    test_connection() 