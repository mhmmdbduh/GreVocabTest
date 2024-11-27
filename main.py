import streamlit as st
import pandas as pd
import random

st.title('GRE Vocabulary Test')
st.text('This is a simple GRE vocabulary test.')

# Load the vocabulary list
vocab_df = pd.read_csv('gre_vocab.csv')

# Function to generate multiple-choice options
def generate_options(correct_meaning, all_meanings, num_options=4):
    options = [correct_meaning]
    while len(options) < num_options:
        option = random.choice(all_meanings)
        if option not in options:
            options.append(option)
    random.shuffle(options)
    return options

# Function to generate questions
def generate_questions(num_questions):
    all_meanings = vocab_df['Meaning'].tolist()
    questions = random.sample(vocab_df.to_dict('records'), num_questions)
    for question in questions:
        question['options'] = generate_options(question['Meaning'], all_meanings)
    return questions

# Select number of questions
number_questions = st.selectbox('How many questions would you like to answer?', [10, 25, 50])

# Initialize session state
if 'num_questions' not in st.session_state:
    st.session_state.num_questions = number_questions

if 'questions' not in st.session_state or st.session_state.num_questions != number_questions:
    st.session_state.questions = generate_questions(number_questions)
    st.session_state.num_questions = number_questions

# Display questions
for i, question in enumerate(st.session_state.questions):
    st.write(f"Question {i+1}: What is the meaning of the word '{question['Word']}'?")
    st.radio(f"Answer {i+1}", question['options'], key=f"answer_{i+1}")

# Buttons to finish and regenerate questions
col1, col2 = st.columns(2)

with col1:
    if st.button('Finish'):
        score = 0
        for i, question in enumerate(st.session_state.questions):
            selected_option = st.session_state.get(f"answer_{i+1}")
            if selected_option == question['Meaning']:
                st.write(f"Question {i+1}: Correct!")
                st.write(f"The meaning of '{question['Word']}' is '{question['Meaning']}'.")
                score += 1
            else:
                st.write(f"Question {i+1}: Incorrect!")
                st.write(f"The meaning of '{question['Word']}' is '{question['Meaning']}'.")
        st.subheader(f"Your score is {score} out of {number_questions}")
        

with col2:
    if st.button('Regenerate Questions'):
        st.session_state.questions = generate_questions(number_questions)
        st.session_state.num_questions = number_questions