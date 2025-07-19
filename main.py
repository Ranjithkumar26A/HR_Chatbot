from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import pandas as pd
from dotenv import load_dotenv
import os
import streamlit as st
from langchain.schema import HumanMessage 


def Main_function(user_input):
    load_dotenv()
    os.environ['GOOGLE_API_KEY']
    try:
        LLM = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=.7)
    except Exception as ex:
        print(ex)

    Excel_data = pd.read_excel(r'HR_Employee_Data.xlsx')

    Analysis_prompt = ChatPromptTemplate.from_messages([
    ("system",
    """You are a smart, friendly, and highly focused data analysis assistant. You analyze the provided Excel HR dataset and respond in a natural, clear, and precise way.

    Excel dataset: {Excel_data}

    YOUR GUIDELINES:
    1. Use ONLY the data **directly present** in the uploaded Excel dataset for **all** responses. Do not guess, infer, or fabricate any information.
    2. If the requested information **exists in the dataset**, extract it exactly and answer precisely.
    3. If the requested information is truly **not present** in the dataset, respond clearly: "This information is not available in the dataset."
    4. Respond **only to what the user asks**. Do not add summaries, extra stats, or charts unless directly requested.
    5. Use **natural language** to make your answers concise, friendly, and human-like.
    6. Keep answers precise and to the point (e.g., "Saran is the highest paid employee with a salary of $20,000").
    7. For general chat like "hi", "thanks", or "how are you", respond politely and ask if help is needed with the dataset.
    
    Your goal is to help users quickly get exactly what they need from the dataset.
    """),
    ("placeholder", "{message}")
])



    response_chain = Analysis_prompt | LLM

    User_input = {

        "message" : [user_input],
        "Excel_data": Excel_data
    }

    Response = response_chain.invoke(User_input)

    return Response.content