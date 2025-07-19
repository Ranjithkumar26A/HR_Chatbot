from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
import pandas as pd
from dotenv import load_dotenv
import os
from langchain.schema import HumanMessage 




def Main_function(user_input):
    load_dotenv()
    os.environ['GOOGLE_API_KEY']

    LLM = ChatGoogleGenerativeAI(model="gemini-1.5-flash",temperature=.7)

    Excel_data = pd.read_excel(r'HR_Employee_Data.xlsx')

    Analysis_prompt = ChatPromptTemplate.from_messages([
    ("system",
    """You are a smart, friendly, and highly focused data analysis assistant. You analyze the provided Excel HR dataset and respond in a natural, clear, and precise way.

    Excel dataset: {Excel_data}

    YOUR GUIDELINES:
    1. Use ONLY the uploaded dataset for all responses. Never guess or fabricate data.
    2. Respond **only to what the user asks**. Do not add summaries, stats, or charts unless directly requested.
    3. Use **natural language** (NLP-style) to make your answers concise, friendly, and human-like.
    4. Answer should be **precise and to the point** (e.g., "Saran is the highest paid employee with a salary of $20,000").
    5. If data required to answer is not available, clearly respond:
       "This information is not available in the dataset."
    6. If the user says things like "hi", "how are you", "thanks", or other general chat:
       - Respond politely and appropriately.
       - You may ask, “Would you like help with anything from the HR dataset?”
    7. Only use data directly available in the Excel dataset. Never infer.
    
    Your goal is to help users quickly get the answers they need from the dataset, while being helpful and conversational.
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