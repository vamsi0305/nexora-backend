import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials in environment variables")

# Standard client using anon key
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Admin client with service_role key to bypass RLS when required
admin_supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
