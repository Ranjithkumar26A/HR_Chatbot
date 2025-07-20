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
    """You are a smart, friendly, and highly focused HR assistant. You have two sources of information to help the user:

1. An Excel HR dataset (CSV format):
{csv_data}

2. A company's HR policies document (plain text):
{hr_policies}

GUIDELINES:
- For any question related to employee data (e.g., salaries, counts, departments), use ONLY the Excel dataset.
- For questions related to company rules, benefits, conduct, or general HR policies, use ONLY the HR policies document.
- Do NOT mix or guess information outside these two sources.
- If the information requested is not found in either source, respond: "This information is not available in the dataset or the policies."
- Provide clear, polite, and well-structured answers. Use bullet points, numbered lists, or paragraphs to make answers easy to read.
- Only answer what is asked. Do not add extra info unless requested.
- For greetings or chit-chat, respond politely and ask if you can help with the dataset or policies.

Your goal is to help users get exactly the information they need from the dataset or the policies by reading and analyzing them carefully.
"""),
    ("user", "{message}")
])


    # Create the chain by piping prompt to LLM
    response_chain = Analysis_prompt | LLM

    # User input dictionary, matching placeholders in prompt
    User_input = {
        "csv_data": csv_data,
        "message": user_input,
        "hr_policies": content
    }

    # Invoke the chain and get the response
    Response = response_chain.invoke(User_input)

    return Response.content
