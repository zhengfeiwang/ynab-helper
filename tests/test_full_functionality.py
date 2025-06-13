from ynab_client import YNABClient
from report_generator import ReportGenerator
from datetime import datetime, timedelta
import os

def test_full_functionality():
    print("Testing YNAB Red Flag Transaction Tracker functionality...\n")
    
    try:
        # Initialize client
        client = YNABClient()
        print("✓ Successfully initialized YNAB client")
        
        # Get accounts and categories for reference
        accounts = client.get_accounts()
        categories = client.get_categories()
        
        print(f"\nFound {len(accounts)} accounts and {len(categories)} category groups")
        
        # Test different date ranges
        print("\nTesting different date ranges:")
        date_ranges = [
            ("Last 7 days", timedelta(days=7)),
            ("Last 30 days", timedelta(days=30)),
            ("Last 90 days", timedelta(days=90))
        ]
        
        for range_name, delta in date_ranges:
            start_date = datetime.now() - delta
            transactions = client.get_red_flag_transactions(
                start_date=start_date,
                end_date=datetime.now()
            )
            print(f"- {range_name}: {len(transactions)} red-flagged transactions")
            
            if transactions:
                # Generate reports for the first date range that has transactions
                if range_name == "Last 30 days":  # or any other range you prefer
                    print("\nGenerating sample reports...")
                    report = ReportGenerator(transactions)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    # Create reports directory if it doesn't exist
                    os.makedirs("reports", exist_ok=True)
                    
                    # Generate reports in all formats
                    pdf_path = f"reports/red_flag_report_{timestamp}.pdf"
                    report.generate_pdf(pdf_path)
                    print(f"✓ Generated PDF report: {pdf_path}")
                    
                    csv_path = f"reports/red_flag_report_{timestamp}.csv"
                    report.generate_csv(csv_path)
                    print(f"✓ Generated CSV report: {csv_path}")
                    
                    excel_path = f"reports/red_flag_report_{timestamp}.xlsx"
                    report.generate_excel(excel_path)
                    print(f"✓ Generated Excel report: {excel_path}")
                    
                    # Print summary
                    print(f"\nReport Summary:")
                    print(f"- Total amount: ${report.calculate_total():,.2f}")
                    print(f"- Number of transactions: {len(transactions)}")
                    print(f"- Date range: {start_date.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}")
                    
                    # Show sample transaction details
                    if transactions:
                        print("\nSample transaction details:")
                        sample = transactions[0]
                        print(f"- Date: {sample.date}")
                        print(f"- Payee: {sample.payee_name}")
                        print(f"- Amount: ${sample.amount/1000:,.2f}")
                        print(f"- Category: {sample.category_name}")
                        if hasattr(sample, "memo") and sample.memo:
                            print(f"- Memo: {sample.memo}")
        
        print("\nAll tests completed successfully!")
        print("\nNext steps:")
        print("1. Check the generated reports in the 'reports' directory")
        print("2. Try running the main application: python src/main.py")
        print("3. Configure automated reports in config.yaml")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your YNAB API token")
        print("2. Verify your internet connection")
        print("3. Make sure you have write permissions in the current directory")

if __name__ == "__main__":
    test_full_functionality() 