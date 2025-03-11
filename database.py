import os
from supabase import create_client, Client
from supabase.client import ClientOptions

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase= create_client(url, key)

response = (
    supabase.table("Customer_DB")
    .select("*")
    .eq("id", 8) 
    .single()
    .execute()
)

data = response.data
print(data)

class DB:
    def GET_DB(a):
        response = (
            supabase.table("Customer_DB")
            .select("*")
            .eq("id", 1) 
            .single()
            .execute()
        )
        return response.data

    def CREATE_USER():
        response = supabase.auth.admin.create_user(
            {
                "email": "ki2003167@gmail.com", 
                "password": "qpwo1029#yytyuboinpom",
                "options": {
                    "data": {
                        "name":"kiran",
                        "age":21,
                        "gender":1,
                        "marital_status":1,
                        "educational_status":1,
                        "employment_status":1,
                        "credit_utilization_ratio":23.0,
                        "payment_history":2546.0,
                        "number_of_credit_account":1,
                        "load_amount":125000.0,
                        'interest_rate':1.0,
                        "loan_term":24,
                        "type_of_loan":1
                    }
                }
            }
        )

            
print(DB.CREATE_USER())
