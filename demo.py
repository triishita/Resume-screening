import streamlit as st
import pdfplumber
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import smtplib

# Function to calculate match percentage
def get_match_percentage(job_description, resume):
    cv = CountVectorizer()
    matrix = cv.fit_transform([job_description, resume])
    similarity_matrix = cosine_similarity(matrix)
    match_percentage = similarity_matrix[0][1] * 100
    return round(match_percentage, 2)

# Streamlit app
st.title("Candidate Selection Tool")

option = st.sidebar.radio("Select an Option", ("Resume Screening", "HR Authentication"))

# Session state to store match percentage and resume details
session_state = st.session_state

if option == "Resume Screening":
    st.subheader("NLP Based Resume Screening")

    input_text = st.text_input("Your email")
    uploadedResume = st.file_uploader("Upload resume", type="pdf")

    click = st.button("Process")

    if click and uploadedResume:
        with pdfplumber.open(uploadedResume) as pdf:
            pages = pdf.pages[0]
            resume = pages.extract_text()

        job_description = "Your job description text here..."

        if job_description and resume:
            match_percentage = get_match_percentage(job_description, resume)
            session_state.match_percentage = match_percentage
            session_state.resume_details = resume
            st.write("Resume submitted!")
            st.write("Match Percentage: ",match_percentage,"%")
            
            if match_percentage >= 40:
                email = "abhiramchintalpati99@gmail.com"
                receiver_email = input_text

                subject = 'Invitation to Interview'
                message = f"""
                Dear {receiver_email},

                We would like to invite you to an interview for the position. 
                The interview will take place on input at input.

                Please let us know if you are available to attend.

                Best regards,
                HR Department
                """

                text = f"Subject: {subject}\n\n{message}"

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()

                server.login(email, "lzoq hyes dhcq irqn")

                server.sendmail(email, receiver_email, text)

                print("Email sent")
                st.write("Invitation email sent!")

            else:
                email = "abhiramchintalpati99@gmail.com"
                receiver_email = input_text

                subject = 'Invitation to Interview'
                message = f"""
                Dear {receiver_email},

                We are sorry to say you are rejected. lol. cry.

                Best regards,
                HR Department
                """

                text = f"Subject: {subject}\n\n{message}"

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()

                server.login(email, "lzoq hyes dhcq irqn")

                server.sendmail(email, receiver_email, text)

                print("Email sent")
                st.write("Rejection email sent.")


elif option == "HR Authentication":
    st.subheader("HR Authentication")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "viraj" and password == "Viraj":  # Replace with actual HR credentials
            st.success("Login successful! You can now view applicant resumes.")

            # Display match percentage and resume details if available
            if "match_percentage" in session_state and "resume_details" in session_state:
                st.subheader("Resume Details")
                st.write(f"Match Percentage: {session_state.match_percentage}%")
                st.write("Resume Text:")
                st.write(session_state.resume_details)
        else:
            st.error("Invalid credentials. Please try again.")
