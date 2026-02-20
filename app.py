import streamlit as st
import os
import sqlite3
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for Gemini AI
prompt = ["""
You are an expert in converting English questions to SQL query!
The SQL database has the name STUDENTS and has the following columns - name, class, marks, company.

Examples:
- "How many students?" → SELECT COUNT(*) FROM STUDENTS;
- "Show INFOSYS employees" → SELECT * FROM STUDENTS WHERE company='INFOSYS';
- "Highest marks?" → SELECT * FROM STUDENTS ORDER BY marks DESC LIMIT 1;
- "Average marks?" → SELECT AVG(marks) FROM STUDENTS;

Rules:
- Only output the SQL query
- No explanation, no markdown, just the query
- Use single quotes for text values
"""]

# Function: Convert English to SQL using Gemini
def get_sql_query(question):
    model = genai.GenerativeModel("models/gemini-2.5-flash")  # CHANGED HERE
    response = model.generate_content([prompt[0], question])
    sql = response.text.replace("```sql", "").replace("```", "").strip()
    return sql

# Function: Execute SQL on database
def run_sql(sql):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return rows, columns

# ==================== PAGE 1: HOME ====================
def page_home():
    # Custom CSS for styling
    st.markdown("""
        <style>
        .main-title {
            color: #00FF00;
            text-align: center;
            font-size: 48px;
            font-weight: bold;
        }
        .sub-title {
            color: #00FF00;
            text-align: center;
            font-size: 24px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title
    st.markdown('<div class="main-title">Welcome to IntelliSQL!</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Revolutionizing Database Querying with Advanced LLM Capabilities</div>', unsafe_allow_html=True)
    
    # Two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Total Students", "5")
        st.metric("Companies", "5")
        st.metric("Average Marks", "82.4")
    
    with col2:
        st.info("""
        ✨ **Our Features:**
        - Natural Language Queries
        - Instant SQL Generation
        - Real-time Database Results
        - Intelligent Query Assistance
        - Performance Optimization
        """)

# ==================== PAGE 2: ABOUT ====================
def page_about():
    st.markdown('<h1 style="color: #00FF00;">About IntelliSQL</h1>', unsafe_allow_html=True)
    
    st.write("""
    **IntelliSQL** is a cutting-edge platform designed to revolutionize the way users interact with SQL databases.
    
    ### 🎯 Our Mission
    To democratize database access by enabling natural language interactions, making SQL querying accessible 
    to everyone regardless of their technical expertise.
    
    ### 🔧 Technology Stack
    - **Frontend:** Streamlit
    - **Backend:** Python, SQLite3
    - **AI Model:** Google Gemini Pro
    - **API:** Google Generative AI
    
    ### 💡 How It Works
    1. You ask a question in English
    2. Gemini AI converts it to SQL
    3. SQL executes on database
    4. Results displayed instantly
    """)

# ==================== PAGE 3: INTELLIGENT QUERY ====================
def page_intelligent_query():
    st.markdown('<h1 style="color: #00FF00;">🧠 Intelligent Query Assistant</h1>', unsafe_allow_html=True)
    
    st.write("Ask questions in natural language and get SQL results instantly!")
    
    # Input box
    question = st.text_input("Your question:", placeholder="e.g., Who works at INFOSYS?")
    
    # Button
    if st.button("Generate SQL & Search", type="primary"):
        if question:
            try:
                # Show thinking spinner
                with st.spinner("🤖 Generating SQL..."):
                    sql = get_sql_query(question)
                
                # Display generated SQL
                st.markdown("### 📝 Generated SQL:")
                st.code(sql, language="sql")
                
                # Execute SQL
                with st.spinner("⚡ Executing query..."):
                    results, columns = run_sql(sql)
                
                # Display results
                st.markdown("### 📊 Results:")
                if results:
                    st.success(f"Found {len(results)} record(s)")
                    
                    # Convert to nice format
                    data = []
                    for row in results:
                        row_dict = {columns[i]: row[i] for i in range(len(columns))}
                        data.append(row_dict)
                    
                    st.table(data)
                else:
                    st.info("No records found matching your query.")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Try rephrasing your question")
    
    # Example queries
    with st.expander("💡 Try These Examples"):
        st.code("Show all students")
        st.code("Who works at INFOSYS?")
        st.code("What is the average marks?")
        st.code("Which student scored highest?")
        st.code("List students in BTech class")

# ==================== MAIN APPLICATION ====================
def main():
    # Page configuration
    st.set_page_config(
        page_title="IntelliSQL",
        page_icon="⭐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    pages = {
        "🏠 Home": page_home,
        "📖 About": page_about,
        "🧠 Intelligent Query": page_intelligent_query
    }
    
    selection = st.sidebar.radio("Go to:", list(pages.keys()))
    
    # Render selected page
    pages[selection]()
    
    # Sidebar footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Powered by Google Gemini 🚀")

# Run the app
if __name__ == "__main__":
    main()