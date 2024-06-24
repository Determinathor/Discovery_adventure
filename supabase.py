import os
from
from supabase import create_client, Client

url: str = os.environ.get("https://thdgkvetrnhgucvunqse.supabase.co")
key: str = os.environ.get("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRoZGdrdmV0cm5oZ3VjdnVucXNlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg5MDA1MTcsImV4cCI6MjAzNDQ3NjUxN30.9HEhs_Vvo-Mqvkh_WsnF1h9gpTSuOJtbkrS9W62azCY")
supabase: Client = create_client(url, key)

