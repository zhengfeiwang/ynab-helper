from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import plotly.utils
import json
from ynab_client import YNABClient

app = Flask(__name__)
client = YNABClient()
CNY_BUDGET_ID = "639270bb-7e47-4a46-b622-8308ce02b3d8"

def get_transactions_data(start_date, end_date, account_id=None):
    """Get and process transactions data."""
    transactions = client.get_red_flag_transactions(
        start_date=start_date,
        end_date=end_date,
        account_id=account_id
    )
    
    if not transactions:
        return pd.DataFrame()
    
    df = pd.DataFrame(transactions)
    df["amount"] = df["amount"].astype(float) / 1000  # Convert to CNY
    df["date"] = pd.to_datetime(df["date"])
    return df

def create_category_chart(df):
    """Create category breakdown chart."""
    if df.empty:
        return None
    
    category_stats = df.groupby("category_name")["amount"].sum().reset_index()
    category_stats = category_stats.sort_values("amount", ascending=False)
    
    fig = px.pie(
        category_stats,
        values="amount",
        names="category_name",
        title="Red Flag Transactions by Category",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_trend_chart(df):
    """Create daily trend chart."""
    if df.empty:
        return None
    
    daily_stats = df.groupby(df["date"].dt.date)["amount"].sum().reset_index()
    daily_stats["date"] = pd.to_datetime(daily_stats["date"])
    
    fig = px.line(
        daily_stats,
        x="date",
        y="amount",
        title="Daily Red Flag Transaction Amounts",
        labels={"amount": "Amount (CNY)", "date": "Date"}
    )
    
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Amount (CNY)",
        hovermode="x unified"
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

@app.route("/")
def index():
    """Render the main dashboard page."""
    # Get default date range (last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # Get accounts for the dropdown
    accounts = client.get_accounts()
    cny_accounts = [acc for acc in accounts if acc["on_budget"]]
    
    return render_template(
        "dashboard.html",
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        accounts=cny_accounts
    )

@app.route("/api/data")
def get_data():
    """API endpoint to get dashboard data."""
    start_date = datetime.strptime(request.args.get("start_date"), "%Y-%m-%d")
    end_date = datetime.strptime(request.args.get("end_date"), "%Y-%m-%d")
    account_id = request.args.get("account_id")
    
    df = get_transactions_data(start_date, end_date, account_id)
    
    if df.empty:
        return jsonify({
            "summary": {
                "total_amount": 0,
                "avg_amount": 0,
                "transaction_count": 0
            },
            "transactions": [],
            "category_chart": None,
            "trend_chart": None
        })
    
    # Calculate summary statistics
    summary = {
        "total_amount": df["amount"].sum(),
        "avg_amount": df["amount"].mean(),
        "transaction_count": len(df)
    }
    
    # Prepare transactions data
    transactions = df.sort_values("date", ascending=False).head(100).to_dict("records")
    for t in transactions:
        t["date"] = t["date"].strftime("%Y-%m-%d")
        t["amount"] = f"¥{t['amount']:,.2f}"
    
    # Create charts
    category_chart = create_category_chart(df)
    trend_chart = create_trend_chart(df)
    
    return jsonify({
        "summary": summary,
        "transactions": transactions,
        "category_chart": category_chart,
        "trend_chart": trend_chart
    })

@app.route('/api/red-flag-amount', methods=['GET'])
def get_red_flag_amount():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    if not start_date_str or not end_date_str:
        return jsonify({"error": "start_date and end_date are required"}), 400
    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    transactions = client.get_red_flag_transactions(start_date=start_date, end_date=end_date)
    total_amount = sum(float(t["amount"]) / 1000 for t in transactions)
    return jsonify({"total_amount": total_amount, "count": len(transactions)})

if __name__ == "__main__":
    app.run(debug=True) 