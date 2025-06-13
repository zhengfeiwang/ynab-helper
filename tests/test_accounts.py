from ynab_client import YNABClient
from rich.console import Console
from rich.table import Table

def test_accounts():
    console = Console()
    client = YNABClient()
    
    # Get all accounts
    accounts = client.get_accounts()
    
    # Create a table to display accounts
    table = Table(title="YNAB Accounts")
    table.add_column("Name", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Balance", style="yellow")
    table.add_column("On Budget", style="magenta")
    table.add_column("Closed", style="red")
    table.add_column("ID", style="blue")
    
    # Add accounts to table
    for account in accounts:
        balance = float(account["balance"]) / 1000  # Convert to CNY
        table.add_row(
            account["name"],
            account["type"],
            f"¥{balance:,.2f}",
            str(account["on_budget"]),
            str(account["closed"]),
            account["id"]
        )
    
    # Print the table
    console.print(table)
    
    # Print summary
    console.print(f"\nTotal accounts found: {len(accounts)}")
    console.print(f"On-budget accounts: {sum(1 for acc in accounts if acc['on_budget'])}")
    console.print(f"Off-budget accounts: {sum(1 for acc in accounts if not acc['on_budget'])}")
    console.print(f"Closed accounts: {sum(1 for acc in accounts if acc['closed'])}")

if __name__ == "__main__":
    test_accounts() 