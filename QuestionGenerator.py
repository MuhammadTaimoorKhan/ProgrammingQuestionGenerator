import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Load API key from environment

api_key=st.secrets["GOOGLE_API_KEY"]
# Initialize model
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=api_key)

# Programming languages list
Programming_Languages = ["Python", "Java", "C++", "C#", "JavaScript"]

# Prompt template
prompt = PromptTemplate.from_template(
    input=["ProgrammingLanguage"],
    template="""
You are a helpful AI assistant. Your task is to generate questions for candidates based on the provided programming language.

## Commands:
1. Only output the questions—do not include any extra phrases or context (e.g., "Here are your questions").
2. Generate 10 technical programming questions covering a range of concepts to thoroughly assess the candidate.
3. Each question should be solvable in approximately 6 minutes.
4. Use a single `/` character as a separator between questions (for easy string splitting later).
5. Ensure the questions vary in difficulty from easy to medium to hard.
6. Each question must be of different concepts (Conditional Statements, Looping, Data Structures, Functional Programming, Object Oriented), the questions are blend of all of these concepts.
7. The question will be coding questions not theoretical.

### Programming Language:
{ProgrammingLanguage}
"""
)

# Function to get model response
def get_response(programming_language):
    prompt_format = prompt.format(ProgrammingLanguage=programming_language)
    response = model.invoke(prompt_format)
    return response.content

# Streamlit layout
st.set_page_config(page_title="Coding Interview Question Generator", layout="wide")
st.title("💻 Coding Interview Question Generator")

# Layout: Two columns
col1, col2 = st.columns([1, 2], gap="large")

# Left Column – Controls
with col1:
    st.header("🔧 Select Options")
    selected_language = st.selectbox("Choose a Programming Language", Programming_Languages)
    
    if st.button("🎯 Generate Questions"):
        with st.spinner("Generating questions..."):
            question_bank = get_response(selected_language)
            list_of_questions = question_bank.strip().split("/")

            formatted_questions = ""
            for i, question in enumerate(list_of_questions, start=1):
                formatted_questions += f"Q{i}. {question.strip()}\n\n"

            st.session_state["generated_questions"] = formatted_questions

# Right Column – Output
with col2:
    st.header("📋 Generated Questions")
    if "generated_questions" in st.session_state:
        st.text_area("Your Questions:", st.session_state["generated_questions"], height=500)
    else:
        st.info("Questions will appear here after generation.")
