from ynab_client import YNABClient
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta

def test_red_flags():
    console = Console()
    client = YNABClient()
    
    # Test different date ranges
    end_date = datetime.now()
    date_ranges = [
        ("Last 7 days", end_date - timedelta(days=7)),
        ("Last 30 days", end_date - timedelta(days=30)),
        ("Last 90 days", end_date - timedelta(days=90)),
        ("Last 365 days", end_date - timedelta(days=365))
    ]
    
    for range_name, start_date in date_ranges:
        console.print(f"\n[bold blue]Testing {range_name}[/bold blue]")
        
        # Get transactions
        transactions = client.get_red_flag_transactions(
            start_date=start_date,
            end_date=end_date
        )
        
        if not transactions:
            console.print(f"[yellow]No red-flagged transactions found in {range_name}[/yellow]")
            continue
        
        # Create a table to display transactions
        table = Table(title=f"Red Flag Transactions - {range_name}")
        table.add_column("Date", style="cyan")
        table.add_column("Payee", style="green")
        table.add_column("Category", style="yellow")
        table.add_column("Amount", style="red")
        table.add_column("Account", style="blue")
        table.add_column("Notes", style="magenta")
        
        # Add transactions to table
        total_amount = 0
        for t in transactions:
            amount = float(t["amount"]) / 1000  # Convert to CNY
            total_amount += amount
            table.add_row(
                t["date"],
                t["payee_name"],
                t["category_name"],
                f"¥{amount:,.2f}",
                t["account_name"],
                t.get("memo", "")
            )
        
        # Print the table
        console.print(table)
        console.print(f"\nTotal amount: ¥{total_amount:,.2f}")
        console.print(f"Number of transactions: {len(transactions)}")

if __name__ == "__main__":
    test_red_flags() 