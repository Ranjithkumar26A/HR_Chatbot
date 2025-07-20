from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import pandas as pd
from dotenv import load_dotenv
import os
import streamlit as st

def Main_function(user_input):
    # Load env vars once (you can move this outside the function in your real app)
    load_dotenv()
    os.environ['GOOGLE_API_KEY'] = st.secrets["GOOGLE_API_KEY"]

    # Initialize the LLM (handle exceptions)
    try:
        LLM = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)
    except Exception as ex:
        st.error(f"LLM Initialization Error: {ex}")
        return "Error initializing language model."

    # Read Excel file (make sure the path is correct)
    Excel_data = pd.read_excel('HR_Employee_Data.xlsx')

    # Convert DataFrame to CSV string
    csv_data = Excel_data.to_csv(index=False)

    with open('policies.txt', 'r', encoding='utf-8') as file:
        content = file.read()


       # Define prompt template with placeholders
    Analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", 
    """You are a smart, friendly, and highly focused HR assistant. You are here to help employees understand the company's HR policies and procedures.

You have access to the company's official HR policy document, shown below:

HR Policies:
{hr_policies}

GUIDELINES:
- Use ONLY the HR policies provided above to answer questions.
- Do NOT guess, assume, or fabricate any information that is not explicitly stated in the policy text.
- If the information is not mentioned in the policies, respond clearly: "This information is not available in the HR policy document."
- Present your answers in a polite, clear, and helpful tone.
- Use bullet points or short paragraphs to improve readability if the answer contains multiple points.
- Only answer what the user asks — do not include extra summaries or context unless requested.
- For greetings or general questions, respond warmly and ask how you can assist with the HR policies.

Your goal is to help employees quickly and accurately understand the policies that affect them.
"""),
    ("user", "{message}")
])


    # Create the chain by piping prompt to LLM
    response_chain = Analysis_prompt | LLM

    # User input dictionary, matching placeholders in prompt
    User_input = {
        "message": user_input,
        "hr_policies": content
    }

    # Invoke the chain and get the response
    Response = response_chain.invoke(User_input)

    return Response.content
