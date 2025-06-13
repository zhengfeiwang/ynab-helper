from ynab_client import YNABClient
from rich.console import Console
from rich.table import Table
from datetime import datetime, timedelta


def list_red_flagged_cny():
    console = Console()
    client = YNABClient()  # Uses .env YNAB_BUDGET_ID
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    transactions = client.get_red_flag_transactions(
        start_date=start_date,
        end_date=end_date
    )

    if not transactions:
        console.print("[yellow]No red-flagged transactions found in the last year for this budget.[/yellow]")
        return

    table = Table(title="Red-Flagged Transactions (CNY Budget, Last Year)")
    table.add_column("Date", style="cyan")
    table.add_column("Payee", style="green")
    table.add_column("Category", style="yellow")
    table.add_column("Account", style="blue")
    table.add_column("Amount", style="red")
    table.add_column("Flag", style="magenta")
    table.add_column("Notes", style="white")

    for t in transactions:
        amount = float(t["amount"]) / 1000
        table.add_row(
            t["date"],
            t.get("payee_name", ""),
            t.get("category_name", ""),
            t.get("account_name", ""),
            f"¥{amount:,.2f}",
            str(t.get("flag_color", "")),
            t.get("memo", "")
        )

    console.print(table)
    console.print(f"\nTotal red-flagged transactions: {len(transactions)}")

if __name__ == "__main__":
    list_red_flagged_cny() 