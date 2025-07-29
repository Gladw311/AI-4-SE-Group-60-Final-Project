import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

from contentloader import load_content_from_json, get_categories, get_topics, get_topic_details

# Dropdown to select content file
selected_file = st.sidebar.selectbox(
    "📂 Choose Content Source:",
    ["civic.json", "financial.json"]
)

# Load content from the selected file
content = load_content_from_json(selected_file)


category = st.selectbox("Select a Category:", get_categories(content))
topic = st.selectbox("Choose a Topic:", get_topics(content, category))
topic_info = get_topic_details(content, category, topic)

st.markdown(f"### {topic_info['title']}")
for point in topic_info['content']:
    st.markdown(f"- {point}")
st.info(f"**Summary:** {topic_info['summary']}")



# Page configuration
st.set_page_config(
    page_title="Civic & Financial Education Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for user progress
if 'user_progress' not in st.session_state:
    st.session_state.user_progress = {
        'civic_lessons_completed': 0,
        'financial_lessons_completed': 0,
        'quizzes_completed': 0,
        'total_score': 0,
        'badges_earned': []
    }

def main():
    # Custom CSS for enhanced styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .section-header {
        font-size: 2rem;
        color: #4ECDC4;
        margin: 1.5rem 0;
        border-bottom: 2px solid #4ECDC4;
        padding-bottom: 0.5rem;
    }
    .highlight-box {
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        font-weight: bold;
    }
    .stat-card {
        background-color: #F0F2F6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #FF6B6B;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("🎓 Navigation")
    
    # Progress overview in sidebar
    st.sidebar.markdown("### Your Progress")
    progress_data = st.session_state.user_progress
    
    st.sidebar.metric("Civic Lessons", progress_data['civic_lessons_completed'], delta=None)
    st.sidebar.metric("Financial Lessons", progress_data['financial_lessons_completed'], delta=None)
    st.sidebar.metric("Quizzes Completed", progress_data['quizzes_completed'], delta=None)
    
    if progress_data['badges_earned']:
        st.sidebar.markdown("### 🏆 Badges Earned")
        for badge in progress_data['badges_earned']:
            st.sidebar.markdown(f"🎖️ {badge}")

    # Main navigation
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🏠 Home", "🏛️ Civic Education", "💰 Financial Literacy", "📝 Quizzes"]
    )

    if page == "🏠 Home":
        show_home_page()
    elif page == "🏛️ Civic Education":
        show_civic_education()
    elif page == "💰 Financial Literacy":
        show_financial_literacy()
    elif page == "📝 Quizzes":
        show_quizzes()

def show_home_page():
    # Hero section
    st.markdown('<h1 class="main-header">🎓 Civic & Financial Education Platform</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight-box">
    Welcome to your journey toward becoming a more informed citizen and financially literate individual! 
    Our platform combines engaging civic education with practical financial literacy to empower you 
    with the knowledge and skills needed for active citizenship and financial success.
    </div>
    """, unsafe_allow_html=True)

    # Platform overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<h3 class="section-header">🏛️ Civic Education</h3>', unsafe_allow_html=True)
        st.markdown("""
        - Government structures and processes
        - Voting rights and responsibilities  
        - Constitutional principles
        - Community engagement
        - Interactive civic simulations
        """)
        if st.button("Start Civic Learning", key="civic_start``"):
            st.session_state.current_page = "civic"
            st.rerun()

    with col2:
        st.markdown('<h3 class="section-header">💰 Financial Literacy</h3>', unsafe_allow_html=True)
        st.markdown("""
        - Personal budgeting and saving
        - Investment fundamentals
        - Understanding credit and debt
        - Financial planning tools
        - Interactive calculators
        """)
        if st.button("Start Financial Learning", key="financial_start"):
            st.session_state.current_page = "financial"
            st.rerun()

    with col3:
        st.markdown('<h3 class="section-header">📝 Interactive Quizzes</h3>', unsafe_allow_html=True)
        st.markdown("""
        - Multiple choice questions
        - True/false assessments
        - Fill-in-the-blank exercises
        - Instant feedback
        - Progress tracking
        """)
        if st.button("Take a Quiz", key="quiz_start"):
            st.session_state.current_page = "quizzes"
            st.rerun()

    # Statistics and engagement
    st.markdown('<h2 class="section-header">📊 Platform Statistics</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
        <h3>25+</h3>
        <p>Civic Lessons Available</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
        <h3>30+</h3>
        <p>Financial Topics Covered</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
        <h3>100+</h3>
        <p>Interactive Quizzes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="stat-card">
        <h3>Real-time</h3>
        <p>Progress Tracking</p>
        </div>
        """, unsafe_allow_html=True)

    # Learning path visualization
    st.markdown('<h2 class="section-header">🛤️ Your Learning Journey</h2>', unsafe_allow_html=True)
    
    # Create progress visualization
    progress_data = pd.DataFrame({
        'Category': ['Civic Education', 'Financial Literacy', 'Quizzes'],
        'Completed': [
            st.session_state.user_progress['civic_lessons_completed'],
            st.session_state.user_progress['financial_lessons_completed'],
            st.session_state.user_progress['quizzes_completed']
        ],
        'Total': [25, 30, 100]
    })
    
    fig = px.bar(progress_data, x='Category', y=['Completed', 'Total'], 
                 title="Your Learning Progress",
                 barmode='group',
                 color_discrete_sequence=['#FF6B6B', '#E0E0E0'])
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Quick tips section
    st.markdown('<h2 class="section-header">💡 Learning Tips</h2>', unsafe_allow_html=True)
    
    tips_col1, tips_col2 = st.columns(2)
    
    with tips_col1:
        st.info("""
        **📚 Study Strategy:**
        - Start with basics in each section
        - Take regular quiz breaks
        - Apply concepts to real-life scenarios
        - Track your progress regularly
        """)
    
    with tips_col2:
        st.success("""
        **🎯 Engagement Tips:**
        - Set daily learning goals
        - Join community discussions
        - Share your achievements
        - Challenge yourself with advanced topics
        """)

def show_civic_education():
    st.markdown('<h1 class="main-header">🏛️ Civic Education</h1>', unsafe_allow_html=True)
    
    # Topic selection
    civic_topics = [
        "Government Structure",
        "Constitutional Rights",
        "Voting Process",
        "Local Government",
        "Federal vs State Powers",
        "Civic Responsibilities"
    ]
    
    selected_topic = st.selectbox("Choose a topic to explore:", civic_topics)
    
    # Content based on selected topic
    if selected_topic == "Government Structure":
        st.markdown('<h2 class="section-header">🏛️ Understanding Government Structure</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### The Three Branches of Government
            
            **Executive Branch:**
            - Led by the President
            - Enforces laws
            - Includes federal agencies and departments
            
            **Legislative Branch:**
            - Congress (House and Senate)
            - Makes laws
            - Controls government spending
            
            **Judicial Branch:**
            - Supreme Court and federal courts
            - Interprets laws
            - Ensures constitutional compliance
            """)
            
            # Interactive element
            if st.button("Test Your Knowledge", key="gov_structure_quiz"):
                st.session_state.quiz_topic = "government_structure"
                st.success("✅ Great! Let's test what you've learned.")
                
                quiz_question = st.radio(
                    "Which branch of government is responsible for making laws?",
                    ["Executive", "Legislative", "Judicial"]
                )
                
                if st.button("Submit Answer"):
                    if quiz_question == "Legislative":
                        st.success("🎉 Correct! The Legislative Branch makes laws.")
                        st.session_state.user_progress['civic_lessons_completed'] += 1
                        st.balloons()
                    else:
                        st.error("❌ Not quite. The Legislative Branch makes laws.")
        
        with col2:
            # Visualization of government structure
            fig = go.Figure(data=[go.Sankey(
                node = dict(
                    pad = 15,
                    thickness = 20,
                    line = dict(color = "black", width = 0.5),
                    label = ["Government", "Executive", "Legislative", "Judicial", "President", "Congress", "Courts"],
                    color = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8"]
                ),
                link = dict(
                    source = [0, 0, 0, 1, 2, 3],
                    target = [1, 2, 3, 4, 5, 6],
                    value = [1, 1, 1, 1, 1, 1]
                )
            )])
            
            fig.update_layout(title_text="Government Structure", font_size=10, height=400)
            st.plotly_chart(fig, use_container_width=True)

    elif selected_topic == "Voting Process":
        st.markdown('<h2 class="section-header">🗳️ The Voting Process</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### Your Right to Vote
        
        Voting is one of the most fundamental rights in a democracy. Here's what you need to know:
        
        **Voter Registration:**
        - Must be 18 years or older
        - Must be a U.S. citizen
        - Register in your state of residence
        - Update registration when you move
        
        **Types of Elections:**
        - **Primary Elections:** Choose party candidates
        - **General Elections:** Choose between party nominees
        - **Local Elections:** City, county, and state positions
        - **Special Elections:** Fill vacant positions or decide on issues
        """)
        
        # Interactive voting simulation
        st.markdown("### 🎯 Interactive Voting Simulation")
        
        with st.expander("Try a Sample Ballot"):
            st.write("**Sample Presidential Election:**")
            
            candidate = st.radio(
                "Choose your candidate:",
                ["Candidate A (Democratic)", "Candidate B (Republican)", "Candidate C (Independent)"]
            )
            
            proposition = st.radio(
                "Proposition 1 - Increase funding for public education:",
                ["Yes", "No"]
            )
            
            if st.button("Cast Your Vote"):
                st.success(f"✅ Vote recorded!\nPresident: {candidate}\nProposition 1: {proposition}")
                st.session_state.user_progress['civic_lessons_completed'] += 1
                st.info("💡 Remember: In real elections, your vote is private and secure!")

def show_financial_literacy():
    st.markdown('<h1 class="main-header">💰 Financial Literacy</h1>', unsafe_allow_html=True)
    
    # Topic selection
    financial_topics = [
        "Personal Budgeting",
        "Saving Strategies",
        "Investment Basics",
        "Understanding Credit",
        "Debt Management",
        "Financial Planning"
    ]
    
    selected_topic = st.selectbox("Choose a financial topic:", financial_topics)
    
    if selected_topic == "Personal Budgeting":
        st.markdown('<h2 class="section-header">📊 Personal Budgeting</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### The 50/30/20 Rule
        
        A simple budgeting framework:
        - **50%** for needs (rent, groceries, utilities)
        - **30%** for wants (entertainment, dining out)
        - **20%** for savings and debt repayment
        """)
        
        # Interactive budget calculator
        st.markdown("### 🧮 Budget Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            monthly_income = st.number_input("Monthly Income ($)", min_value=0.0, value=3000.0, step=100.0)
            
            st.markdown("**Monthly Expenses:**")
            rent = st.number_input("Rent/Mortgage ($)", min_value=0.0, value=1200.0, step=50.0)
            food = st.number_input("Food ($)", min_value=0.0, value=400.0, step=25.0)
            utilities = st.number_input("Utilities ($)", min_value=0.0, value=200.0, step=25.0)
            entertainment = st.number_input("Entertainment ($)", min_value=0.0, value=300.0, step=25.0)
            other = st.number_input("Other Expenses ($)", min_value=0.0, value=200.0, step=25.0)
        
        with col2:
            total_expenses = rent + food + utilities + entertainment + other
            remaining = monthly_income - total_expenses
            
            st.markdown("### 📈 Budget Analysis")
            st.metric("Total Income", f"${monthly_income:,.2f}")
            st.metric("Total Expenses", f"${total_expenses:,.2f}")
            st.metric("Remaining", f"${remaining:,.2f}", delta=remaining)
            
            # Budget breakdown pie chart
            expenses_data = pd.DataFrame({
                'Category': ['Rent/Mortgage', 'Food', 'Utilities', 'Entertainment', 'Other', 'Savings'],
                'Amount': [rent, food, utilities, entertainment, other, max(0, remaining)]
            })
            
            fig = px.pie(expenses_data, values='Amount', names='Category', 
                        title="Budget Breakdown",
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
            
            if remaining > 0:
                st.success(f"✅ Great! You have ${remaining:,.2f} left for savings!")
                st.session_state.user_progress['financial_lessons_completed'] += 1
            else:
                st.warning(f"⚠️ You're overspending by ${abs(remaining):,.2f}. Consider reducing expenses.")

    elif selected_topic == "Investment Basics":
        st.markdown('<h2 class="section-header">📈 Investment Basics</h2>', unsafe_allow_html=True)
        
        st.markdown("""
        ### Key Investment Principles
        
        **1. Start Early:** The power of compound interest
        **2. Diversify:** Don't put all eggs in one basket
        **3. Risk vs Return:** Higher potential returns often mean higher risk
        **4. Dollar-Cost Averaging:** Invest regularly regardless of market conditions
        """)
        
        # Investment growth calculator
        st.markdown("### 💹 Investment Growth Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            initial_investment = st.number_input("Initial Investment ($)", min_value=0.0, value=1000.0, step=100.0)
            monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0.0, value=100.0, step=50.0)
            annual_return = st.slider("Expected Annual Return (%)", min_value=1.0, max_value=15.0, value=7.0, step=0.5)
            years = st.slider("Investment Period (years)", min_value=1, max_value=40, value=10)
        
        with col2:
            # Calculate compound growth
            months = years * 12
            monthly_return = annual_return / 100 / 12
            
            # Future value calculation
            if monthly_return > 0:
                future_value = initial_investment * (1 + monthly_return) ** months
                if monthly_contribution > 0:
                    future_value += monthly_contribution * (((1 + monthly_return) ** months - 1) / monthly_return)
            else:
                future_value = initial_investment + (monthly_contribution * months)
            
            total_invested = initial_investment + (monthly_contribution * months)
            total_growth = future_value - total_invested
            
            st.metric("Total Invested", f"${total_invested:,.2f}")
            st.metric("Future Value", f"${future_value:,.2f}")
            st.metric("Total Growth", f"${total_growth:,.2f}", delta=f"{(total_growth/total_invested)*100:.1f}%")
            
            # Growth visualization
            years_range = list(range(1, years + 1))
            values = []
            
            for year in years_range:
                months_elapsed = year * 12
                if monthly_return > 0:
                    value = initial_investment * (1 + monthly_return) ** months_elapsed
                    if monthly_contribution > 0:
                        value += monthly_contribution * (((1 + monthly_return) ** months_elapsed - 1) / monthly_return)
                else:
                    value = initial_investment + (monthly_contribution * months_elapsed)
                values.append(value)
            
            growth_df = pd.DataFrame({
                'Year': years_range,
                'Investment Value': values
            })
            
            fig = px.line(growth_df, x='Year', y='Investment Value', 
                         title="Investment Growth Over Time",
                         line_shape='spline')
            fig.update_traces(line_color='#FF6B6B', line_width=3)
            st.plotly_chart(fig, use_container_width=True)

def show_quizzes():
    st.markdown('<h1 class="main-header">📝 Interactive Quizzes</h1>', unsafe_allow_html=True)
    
    # Quiz categories
    quiz_categories = ["Civic Knowledge", "Financial Literacy", "Mixed Topics"]
    selected_category = st.selectbox("Choose quiz category:", quiz_categories)
    
    if selected_category == "Civic Knowledge":
        st.markdown('<h2 class="section-header">🏛️ Civic Knowledge Quiz</h2>', unsafe_allow_html=True)
        
        # Sample civic quiz questions
        civic_questions = [
            {
                "question": "How many branches of government are there in the United States?",
                "options": ["Two", "Three", "Four", "Five"],
                "correct": 1,
                "explanation": "The U.S. government has three branches: Executive, Legislative, and Judicial."
            },
            {
                "question": "What is the minimum age to vote in federal elections?",
                "options": ["16", "18", "21", "25"],
                "correct": 1,
                "explanation": "The 26th Amendment established 18 as the minimum voting age."
            },
            {
                "question": "Which document begins with 'We the People'?",
                "options": ["Declaration of Independence", "Bill of Rights", "Constitution", "Federalist Papers"],
                "correct": 2,
                "explanation": "The U.S. Constitution begins with the famous preamble 'We the People...'"
            }
        ]
        
        # Quiz interface
        if 'current_civic_question' not in st.session_state:
            st.session_state.current_civic_question = 0
            st.session_state.civic_score = 0
            st.session_state.civic_answers = []
        
        current_q = st.session_state.current_civic_question
        
        if current_q < len(civic_questions):
            question_data = civic_questions[current_q]
            
            st.markdown(f"### Question {current_q + 1} of {len(civic_questions)}")
            st.write(question_data["question"])
            
            answer = st.radio("Choose your answer:", question_data["options"], key=f"civic_q_{current_q}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Submit Answer", key=f"submit_civic_{current_q}"):
                    selected_index = question_data["options"].index(answer)
                    is_correct = selected_index == question_data["correct"]
                    
                    st.session_state.civic_answers.append({
                        "question": question_data["question"],
                        "selected": answer,
                        "correct": is_correct,
                        "explanation": question_data["explanation"]
                    })
                    
                    if is_correct:
                        st.success("✅ Correct!")
                        st.session_state.civic_score += 1
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: {question_data['options'][question_data['correct']]}")
                    
                    st.info(f"💡 {question_data['explanation']}")
                    st.session_state.current_civic_question += 1
                    st.rerun()
            
            with col2:
                progress = (current_q + 1) / len(civic_questions)
                st.progress(progress)
                st.write(f"Progress: {current_q + 1}/{len(civic_questions)}")
        
        else:
            # Quiz completed
            st.markdown('<h2 class="section-header">🎉 Quiz Completed!</h2>', unsafe_allow_html=True)
            
            score_percentage = (st.session_state.civic_score / len(civic_questions)) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{st.session_state.civic_score}/{len(civic_questions)}")
            with col2:
                st.metric("Percentage", f"{score_percentage:.1f}%")
            with col3:
                if score_percentage >= 80:
                    badge = "🏆 Civic Champion"
                elif score_percentage >= 60:
                    badge = "🥉 Civic Scholar"
                else:
                    badge = "📚 Keep Learning"
                st.metric("Badge Earned", badge)
            
            # Performance visualization
            correct_answers = st.session_state.civic_score
            incorrect_answers = len(civic_questions) - correct_answers
            
            fig = px.pie(
                values=[correct_answers, incorrect_answers],
                names=['Correct', 'Incorrect'],
                title="Quiz Performance",
                color_discrete_sequence=['#4ECDC4', '#FF6B6B']
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Update user progress
            st.session_state.user_progress['quizzes_completed'] += 1
            st.session_state.user_progress['total_score'] += st.session_state.civic_score
            
            if score_percentage >= 80 and "Civic Champion" not in st.session_state.user_progress['badges_earned']:
                st.session_state.user_progress['badges_earned'].append("Civic Champion")
                st.balloons()
            
            if st.button("Take Another Quiz"):
                # Reset quiz state
                st.session_state.current_civic_question = 0
                st.session_state.civic_score = 0
                st.session_state.civic_answers = []
                st.rerun()

    elif selected_category == "Financial Literacy":
        st.markdown('<h2 class="section-header">💰 Financial Literacy Quiz</h2>', unsafe_allow_html=True)
        
        # Sample financial quiz questions
        financial_questions = [
            {
                "question": "What is compound interest?",
                "options": ["Interest on the principal only", "Interest on principal and accumulated interest", "A type of loan", "A banking fee"],
                "correct": 1,
                "explanation": "Compound interest is earned on both the initial principal and previously earned interest."
            },
            {
                "question": "What percentage of income should ideally go to savings according to the 50/30/20 rule?",
                "options": ["10%", "15%", "20%", "25%"],
                "correct": 2,
                "explanation": "The 50/30/20 rule suggests 20% for savings and debt repayment."
            },
            {
                "question": "Which investment typically has the highest risk and potential return?",
                "options": ["Savings account", "Government bonds", "Corporate stocks", "Certificate of deposit"],
                "correct": 2,
                "explanation": "Stocks generally offer higher potential returns but come with higher risk."
            }
        ]
        
        # Similar quiz interface for financial questions
        if 'current_financial_question' not in st.session_state:
            st.session_state.current_financial_question = 0
            st.session_state.financial_score = 0
            st.session_state.financial_answers = []
        
        current_q = st.session_state.current_financial_question
        
        if current_q < len(financial_questions):
            question_data = financial_questions[current_q]
            
            st.markdown(f"### Question {current_q + 1} of {len(financial_questions)}")
            st.write(question_data["question"])
            
            answer = st.radio("Choose your answer:", question_data["options"], key=f"financial_q_{current_q}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Submit Answer", key=f"submit_financial_{current_q}"):
                    selected_index = question_data["options"].index(answer)
                    is_correct = selected_index == question_data["correct"]
                    
                    if is_correct:
                        st.success("✅ Correct!")
                        st.session_state.financial_score += 1
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: {question_data['options'][question_data['correct']]}")
                    
                    st.info(f"💡 {question_data['explanation']}")
                    st.session_state.current_financial_question += 1
                    st.rerun()
            
            with col2:
                progress = (current_q + 1) / len(financial_questions)
                st.progress(progress)
                st.write(f"Progress: {current_q + 1}/{len(financial_questions)}")
        
        else:
            # Quiz completed - similar to civic quiz completion
            st.markdown('<h2 class="section-header">🎉 Financial Quiz Completed!</h2>', unsafe_allow_html=True)
            
            score_percentage = (st.session_state.financial_score / len(financial_questions)) * 100
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{st.session_state.financial_score}/{len(financial_questions)}")
            with col2:
                st.metric("Percentage", f"{score_percentage:.1f}%")
            with col3:
                if score_percentage >= 80:
                    badge = "💎 Financial Expert"
                elif score_percentage >= 60:
                    badge = "💰 Money Smart"
                else:
                    badge = "📈 Keep Learning"
                st.metric("Badge Earned", badge)
            
            # Update progress
            st.session_state.user_progress['quizzes_completed'] += 1
            st.session_state.user_progress['total_score'] += st.session_state.financial_score
            
            if score_percentage >= 80 and "Financial Expert" not in st.session_state.user_progress['badges_earned']:
                st.session_state.user_progress['badges_earned'].append("Financial Expert")
                st.balloons()
            
            if st.button("Take Another Quiz"):
                st.session_state.current_financial_question = 0
                st.session_state.financial_score = 0
                st.session_state.financial_answers = []
                st.rerun()

if __name__ == "__main__":
    main()
