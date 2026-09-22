import streamlit as st
import pandas as pd

from llm_handler import get_book_preferences
from fuzzy_logic import calculate_suitability


# Load books
books = pd.read_csv("books.csv")


# Page settings
st.set_page_config(
    page_title="Smart Library Management System",
    page_icon="📚",
    layout="wide"
)


# Title
st.title("📚 Smart Library Management System")
st.subheader("AI + Fuzzy Logic Based Library Assistant")

st.write(
    "Welcome! Describe your library requirement in natural language "
    "and our AI system will analyze it."
)


# User input
user_input = st.text_area(
    "📝 Describe your library requirement:",
    placeholder="Example: I need an easy Python book for my exam..."
)


# General availability
availability = st.slider(
    "📖 General Book Availability",
    min_value=0,
    max_value=100,
    value=80
)


# Analyze request
if st.button("🔍 Analyze Request"):

    if user_input.strip():

        # AI Analysis
        with st.spinner("🤖 AI is analyzing your requirement..."):
            ai_result = get_book_preferences(user_input)

        st.success("Request analyzed successfully!")

        st.write("### 🧠 AI Understanding")
        st.write(ai_result)


        # -------------------------------
        # EXTRACT SUBJECT
        # -------------------------------

        subject_line = [
            line for line in ai_result.splitlines()
            if line.lower().startswith("subject:")
        ]

        subject = (
            subject_line[0].split(":", 1)[1].strip()
            if subject_line
            else ""
        )


        # -------------------------------
        # EXTRACT DIFFICULTY
        # -------------------------------

        ai_result_lower = ai_result.lower()

        if "difficulty: easy" in ai_result_lower:
            difficulty = 20

        elif "difficulty: medium" in ai_result_lower:
            difficulty = 50

        elif "difficulty: hard" in ai_result_lower:
            difficulty = 80

        else:
            # If AI does not specify difficulty,
            # use Medium as default.
            difficulty = 50


        # -------------------------------
        # BOOK RECOMMENDATION
        # -------------------------------

        recommendations = []

        for _, book in books.iterrows():

            book_subject = str(book["subject"]).lower()

            requested_subject = subject.lower()


            # Subject matching
            if (
                requested_subject in book_subject
                or book_subject in requested_subject
                or requested_subject.replace(
                    " programming", ""
                ) in book_subject
            ):
                relevance = 90
            else:
                relevance = 30


            # Fuzzy Logic
            score = calculate_suitability(
                relevance,
                difficulty,
                book["availability"]
            )


            recommendations.append({
                "title": book["title"],
                "subject": book["subject"],
                "difficulty": book["difficulty"],
                "availability": book["availability"],
                "score": score
            })


        # Create DataFrame
        recommendations_df = pd.DataFrame(
            recommendations
        )


        # Sort by fuzzy score
        recommendations_df = recommendations_df.sort_values(
            by="score",
            ascending=False
        )


        # -------------------------------
        # SHOW RECOMMENDATIONS
        # -------------------------------

        st.write("### 📚 Recommended Books")

        top_books = recommendations_df.head(3)


        for _, book in top_books.iterrows():

            st.write(
                f"**📖 {book['title']}**"
            )

            st.write(
                f"Subject: {book['subject']} | "
                f"Difficulty: {book['difficulty']} | "
                f"Availability: {book['availability']}%"
            )

            st.metric(
                "Fuzzy Suitability Score",
                f"{book['score']}/100"
            )

            st.divider()


        # -------------------------------
        # RESULT MESSAGE
        # -------------------------------

        best_score = top_books.iloc[0]["score"]


        if best_score >= 80:

            st.success(
                "⭐ Excellent book match for your requirement!"
            )

        elif best_score >= 60:

            st.info(
                "👍 Good book match for your requirement."
            )

        else:

            st.warning(
                "⚠️ No highly suitable book was found."
            )


    else:

        st.warning(
            "Please enter your library requirement."
        )