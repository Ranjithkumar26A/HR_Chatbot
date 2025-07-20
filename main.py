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

    # Create the prompt template with csv_data injected using an f-string!
    Analysis_prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a smart, friendly, and highly focused data analysis assistant. You analyze the provided Excel HR dataset and respond clearly and precisely in natural language.

Excel dataset (CSV):
{csv_data}

GUIDELINES:
1. Use ONLY the data directly present in the Excel dataset above for ALL responses.
2. You are allowed and expected to perform simple data analysis tasks on the dataset such as sorting, filtering, aggregation (e.g., finding the highest salary, average, counts).
3. If the user asks for the highest paid employee, find the employee with the maximum salary by analyzing the dataset and respond with a clear sentence like: "Saran is the highest paid employee with a salary of $20,000."
4. If the requested information is not present or cannot be determined from the data, respond clearly: "This information is not available in the dataset."
5. Do NOT guess, infer, or fabricate data outside what is given.
6. Answer ONLY what the user asks. Do not provide extra summaries or charts unless requested.
7. For greetings or general chit-chat, respond politely and ask if you can help with the dataset.

Your goal is to help users quickly get exactly the information they need from the dataset by reading and analyzing it.
"""),
        ("placeholder", "{message}")
    ])

    # Create chain by piping prompt and LLM
    response_chain = Analysis_prompt | LLM

    # User input dictionary for the prompt
    User_input = {
        "message": user_input 
    }

    # Invoke chain and get response
    Response = response_chain.invoke(User_input)

    return Response.content
