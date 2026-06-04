import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# -------------------------------
# CONFIG
# -------------------------------
NUM_USERS = 100
NUM_FEEDBACK = 1000

# -------------------------------
# MBTI TYPES
# -------------------------------
MBTI_TYPES = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# -------------------------------
# PROFESSIONS
# -------------------------------
PROFESSIONS = [
    "Data Scientist",
    "Software Engineer",
    "Machine Learning Engineer",
    "Business Analyst",
    "Cyber Security Analyst",
    "Cloud Engineer",
    "UI UX Designer",
    "Project Manager",
    "Product Manager",
    "DevOps Engineer",
    "AI Researcher",
    "Marketing Specialist",
    "Financial Analyst",
    "Doctor",
    "Teacher",
    "Civil Engineer",
    "Mechanical Engineer",
    "Entrepreneur"
]

# -------------------------------
# LOCATIONS
# -------------------------------
LOCATIONS = [
    "Hyderabad",
    "Bangalore",
    "Chennai",
    "Mumbai",
    "Delhi",
    "Pune",
    "Kolkata",
    "Ahmedabad",
    "Visakhapatnam",
    "Coimbatore"
]

# -------------------------------
# INTERESTS
# -------------------------------
INTERESTS = [
    "Artificial Intelligence",
    "Machine Learning",
    "Startups",
    "Fitness",
    "Reading",
    "Travel",
    "Photography",
    "Gaming",
    "Public Speaking",
    "Music",
    "Technology",
    "Finance",
    "Cooking",
    "Sports",
    "Mentoring"
]

# -------------------------------
# PROFESSIONAL SUMMARY TEMPLATES
# -------------------------------
PRO_SUMMARY = [
    "Experienced professional focused on innovation and solving complex business challenges using modern technologies.",
    "Passionate about building scalable solutions and contributing to high-performing teams.",
    "Strong background in analytics, communication, and project execution across multiple domains.",
    "Dedicated to continuous learning and delivering impactful results through collaboration.",
    "Skilled in problem solving, strategic planning, and developing efficient workflows."
]

# -------------------------------
# ABOUT ME TEMPLATES
# -------------------------------
ABOUT_ME = [
    "I enjoy solving real-world problems and collaborating with people who share a growth mindset.",
    "I value creativity, teamwork, and continuous self-improvement in both personal and professional life.",
    "I enjoy mentoring others, learning new skills, and exploring innovative ideas.",
    "I am passionate about meaningful work, strong relationships, and lifelong learning.",
    "I thrive in collaborative environments and enjoy taking on challenging opportunities."
]
 # -------------------------------
# CREATE USERS
# -------------------------------
users = []

for i in range(1, NUM_USERS + 1):

    user_id = f"U{i:03d}"

    profession = random.choice(PROFESSIONS)

    user = {
        "user_id": user_id,
        "name": fake.name(),
        "age": random.randint(21, 45),
        "location": random.choice(LOCATIONS),
        "profession": profession,
        "experience_years": random.randint(0, 20),
        "professional_summary":
            f"{profession}. {random.choice(PRO_SUMMARY)}",
        "about_me":
            random.choice(ABOUT_ME),
        "mbti": random.choice(MBTI_TYPES),
        "interests":
            ", ".join(random.sample(INTERESTS, 3))
    }

    users.append(user)

users_df = pd.DataFrame(users)
# -------------------------------
# CREATE FEEDBACK
# -------------------------------
feedback = []

for _ in range(NUM_FEEDBACK):

    viewer = random.choice(users_df["user_id"].tolist())

    matched = random.choice(users_df["user_id"].tolist())

    while viewer == matched:
        matched = random.choice(users_df["user_id"].tolist())

    if random.random() < 0.7:
        action = 1
    else:
        action = 0

    timestamp = datetime.now() - timedelta(
        days=random.randint(1, 365)
    )

    feedback.append({
        "user_id": viewer,
        "matched_user_id": matched,
        "action": action,
        "timestamp": timestamp.strftime("%Y-%m-%d")
    })

print("Length of feedback list:", len(feedback))

feedback_df = pd.DataFrame(feedback)

print("Users Generated:", len(users_df))
print("Feedback Generated:", len(feedback_df))
print(feedback_df.head())
# -------------------------------
# SAVE FILES
# -------------------------------
users_df.to_csv("../data/users.csv", index=False)
feedback_df.to_csv("../data/feedback.csv", index=False)

print("users.csv created successfully")
print("feedback.csv created successfully")
print(f"Users: {len(users_df)}")
print(f"Feedback Records: {len(feedback_df)}")