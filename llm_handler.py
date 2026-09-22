import os
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate


def get_book_preferences(user_query):

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        return "GOOGLE_API_KEY is not set."

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=api_key,
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template("""
You are a smart library assistant.

Analyze the user's request and identify these four things:

1. Subject
2. Difficulty level
3. Purpose
4. Book preference

IMPORTANT RULES:

- Difficulty MUST be exactly one of these:
  Easy
  Medium
  Hard

- If the user says easy, beginner, basic, simple, or beginner-friendly,
  return Easy.

- If the user says intermediate, moderate, or normal level,
  return Medium.

- If the user says advanced, difficult, expert, or hard,
  return Hard.

- If difficulty is not mentioned, return Medium.

- Do not write "Not specified" for Difficulty.

User request:
{query}

Return exactly in this format:

Subject: ...
Difficulty: Easy/Medium/Hard
Purpose: ...
Preference: ...
""")

    chain = prompt | llm

    response = chain.invoke({
        "query": user_query
    })

    if isinstance(response.content, list):
        return response.content[0].get("text", "")

    return response.content