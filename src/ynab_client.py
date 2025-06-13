import os
from typing import Dict, List, Optional
from datetime import datetime
import requests
from dotenv import load_dotenv
import time

class YNABClient:
    def __init__(self, budget_id: Optional[str] = None):
        load_dotenv()
        self.api_token = os.getenv("YNAB_API_TOKEN")
        if not self.api_token:
            raise ValueError("YNAB API token not found in environment variables")
        
        # Set up API configuration
        self.base_url = "https://api.ynab.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        # Cache for storing data
        self._cache = {}
        self._cache_timeout = 300  # 5 minutes
        
        # Budget selection logic
        self.budget_id = (
            budget_id or
            os.getenv("YNAB_BUDGET_ID")
        )
        if not self.budget_id:
            self.budget_id = self._get_first_budget_id()
    
    def _get_first_budget_id(self) -> str:
        """Get the first budget ID with caching."""
        cache_key = "budget_id"
        if cache_key in self._cache:
            cache_time, budget_id = self._cache[cache_key]
            if time.time() - cache_time < self._cache_timeout:
                return budget_id
        
        try:
            response = requests.get(
                f"{self.base_url}/budgets",
                headers=self.headers
            )
            response.raise_for_status()
            
            data = response.json()
            if not data["data"]["budgets"]:
                raise ValueError("No budgets found in your YNAB account")
            
            budget_id = data["data"]["budgets"][0]["id"]
            self._cache[cache_key] = (time.time(), budget_id)
            return budget_id
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, "status_code") and e.response.status_code == 401:
                raise ValueError("Invalid API token. Please check your YNAB API token in the .env file.")
            raise
    
    def get_red_flag_transactions(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        category_id: Optional[str] = None,
        account_id: Optional[str] = None,
        use_cache: bool = True
    ) -> List[Dict]:
        """
        Retrieve red-flagged transactions with optional filtering.
        
        Args:
            start_date: Start date for filtering transactions
            end_date: End date for filtering transactions
            category_id: Optional category ID to filter by
            account_id: Optional account ID to filter by
            use_cache: Whether to use cached data if available
            
        Returns:
            List of transaction dictionaries
        """
        try:
            # Check cache if enabled
            if use_cache:
                cache_key = f"transactions_{start_date}_{end_date}_{category_id}_{account_id}"
                if cache_key in self._cache:
                    cache_time, transactions = self._cache[cache_key]
                    if time.time() - cache_time < self._cache_timeout:
                        return transactions
            
            # Build URL with parameters
            url = f"{self.base_url}/budgets/{self.budget_id}/transactions"
            params = {}
            if start_date:
                params["since_date"] = start_date.strftime("%Y-%m-%d")
            
            # Get transactions
            response = requests.get(
                url,
                headers=self.headers,
                params=params
            )
            response.raise_for_status()
            
            # Filter for red flags
            transactions = response.json()["data"]["transactions"]
            red_flag_transactions = [
                t for t in transactions
                if t.get("flag_color") == "red" or t.get("flag_color") == "red_flag"
            ]
            
            # Apply date filters
            if start_date:
                red_flag_transactions = [
                    t for t in red_flag_transactions
                    if datetime.strptime(t["date"], "%Y-%m-%d") >= start_date
                ]
            
            if end_date:
                red_flag_transactions = [
                    t for t in red_flag_transactions
                    if datetime.strptime(t["date"], "%Y-%m-%d") <= end_date
                ]
            
            # Apply category filter
            if category_id:
                red_flag_transactions = [
                    t for t in red_flag_transactions
                    if t["category_id"] == category_id
                ]
            
            # Apply account filter
            if account_id:
                red_flag_transactions = [
                    t for t in red_flag_transactions
                    if t["account_id"] == account_id
                ]
            
            # Update cache
            if use_cache:
                self._cache[cache_key] = (time.time(), red_flag_transactions)
            
            return red_flag_transactions
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, "status_code"):
                if e.response.status_code == 401:
                    raise ValueError("Invalid API token. Please check your YNAB API token in the .env file.")
                elif e.response.status_code == 429:
                    raise ValueError("Rate limit exceeded. Please try again later.")
            print(f"Error fetching transactions: {str(e)}")
            return []
    
    def get_categories(self, use_cache: bool = True) -> List[Dict]:
        """Get all categories from YNAB."""
        try:
            # Check cache if enabled
            if use_cache:
                cache_key = "categories"
                if cache_key in self._cache:
                    cache_time, categories = self._cache[cache_key]
                    if time.time() - cache_time < self._cache_timeout:
                        return categories
            
            response = requests.get(
                f"{self.base_url}/budgets/{self.budget_id}/categories",
                headers=self.headers
            )
            response.raise_for_status()
            
            categories = response.json()["data"]["category_groups"]
            
            # Update cache
            if use_cache:
                self._cache[cache_key] = (time.time(), categories)
            
            return categories
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, "status_code") and e.response.status_code == 401:
                raise ValueError("Invalid API token. Please check your YNAB API token in the .env file.")
            print(f"Error fetching categories: {str(e)}")
            return []
    
    def get_accounts(self, use_cache: bool = True) -> List[Dict]:
        """Get all accounts from YNAB."""
        try:
            # Check cache if enabled
            if use_cache:
                cache_key = "accounts"
                if cache_key in self._cache:
                    cache_time, accounts = self._cache[cache_key]
                    if time.time() - cache_time < self._cache_timeout:
                        return accounts
            
            response = requests.get(
                f"{self.base_url}/budgets/{self.budget_id}/accounts",
                headers=self.headers
            )
            response.raise_for_status()
            
            accounts = response.json()["data"]["accounts"]
            
            # Update cache
            if use_cache:
                self._cache[cache_key] = (time.time(), accounts)
            
            return accounts
            
        except requests.exceptions.RequestException as e:
            if hasattr(e.response, "status_code") and e.response.status_code == 401:
                raise ValueError("Invalid API token. Please check your YNAB API token in the .env file.")
            print(f"Error fetching accounts: {str(e)}")
            return [] 