from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.chat_models import ChatOllama
from tensorflow.keras.models import load_model
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from dotenv import load_dotenv
import numpy as np

app = Flask(__name__)
CORS(app)

llm = ChatOllama(model="KiranKumarReddy/Finage", temperature=0) 
model = load_model("credit_score_model.h5")

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    response = llm.invoke(query)
    return jsonify({'response' : response.content})

SYSTEM_PROMPT = """
You are a financial advisor specialized in credit score analysis.
Whenever a user asks about financial health, always provide advice based on their credit score category:
- Poor (Below 580): Recommend improving payment history, reducing debt, and checking credit reports for errors.
- Fair (580-669): Suggest keeping credit utilization low and making timely payments.
- Good (670-739): Encourage responsible borrowing and credit diversification.
- Very Good (740-799): Highlight access to better loans and continued financial discipline.
- Excellent (800+): Emphasize maintaining excellent habits and leveraging credit wisely.
Your responses should be professional, informative, and tailored to the user's financial situation.
[Rules]
-You only give answer to the query. don't give ant given instructions as a result.
"""

@app.route('/api/advice', methods=['POST'])
def advice():
    """Handles advice requests."""
    """url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase= create_client(url, key)"""
    data1 = request.get_json()
    selected_id = data1.get("Sel_id")
    print("\n\n\n\n\n",selected_id,"\n\n\n\n\n")
    #data = DB.GET_DB(selected_id)
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase= create_client(url, key)

    response = (
        supabase.table("profiles")
        .select("*")
        .eq("id", selected_id) 
        .single()
        .execute()
    )
   
    try:
        data = response.data
        print("\n\n\n\n\nid:",data.get("Credir Utilization Ratio"),data,"\n\n\n\n\n")
    except:
        return jsonify({'response' : "Error!"})
    
    age = data.get("age")   
    gender = data.get("gender")
    marital_status = data.get("marital_status")
    education_level = data.get("educational_status")   
    employment_status = data.get("employment_status")
    credit_utilization_ratio = data.get("credit_utilization_ratio")
    payment_history = data.get("payment_history")
    number_of_credit_accounts = data.get("number_of_credit_account")
    loan_amount = data.get("loan_amount")
    interest_rate = data.get("interest_rate")
    loan_term = data.get("loan_term")
    type_of_loan = data.get("type_of_loan")

    input_vect = np.array([[age, gender, marital_status, education_level, employment_status,
                         credit_utilization_ratio, payment_history, number_of_credit_accounts,
                         loan_amount, interest_rate, loan_term, type_of_loan]], dtype=np.float64)

    score = model.predict(input_vect)

    full_prompt = f"{SYSTEM_PROMPT}\n\nUser's data is:age:{age},gender:{gender},marital_status:{marital_status},education_level:{education_level},employment_status:{employment_status},credit_utilization_ratio:{credit_utilization_ratio},payment_history:{payment_history},number_of_credit_accounts:{number_of_credit_accounts},loan_amount:{loan_amount},interest_rate:{interest_rate},loan_term:{loan_term},type_of_loan:{type_of_loan}\nUser's credit score: {score}\nUser's question:tell me the score. Suggestion for increse my credit card score, what are the prime factors that affecting my score. "
    response = llm.invoke(full_prompt)
    if score < 580:
        c = "red"
    elif score >= 580 and score <= 669:
        c = "orange" 
    elif score >= 670 and score <= 739:
        c = "yellow" 
    elif score >= 740 and score < 799:
        c = "green" 
    else:
        c = "blue"
    return jsonify({'response' : response.content,'color':c})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
