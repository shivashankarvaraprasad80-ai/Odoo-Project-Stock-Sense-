# MBTI compatibility scores

MBTI_COMPATIBILITY = {
    "INTJ": ["ENFP", "ENTP"],
    "INTP": ["ENTJ", "ENFJ"],
    "ENTJ": ["INTP", "INFP"],
    "ENTP": ["INFJ", "INTJ"],
    "INFJ": ["ENTP", "ENFP"],
    "INFP": ["ENFJ", "ENTJ"],
    "ENFJ": ["INFP", "ISFP"],
    "ENFP": ["INTJ", "INFJ"],
    "ISTJ": ["ESFP", "ESTP"],
    "ISFJ": ["ESFP", "ESTP"],
    "ESTJ": ["ISFP", "ISTP"],
    "ESFJ": ["ISFP", "ISTP"],
    "ISTP": ["ESFJ", "ESTJ"],
    "ISFP": ["ENFJ", "ESFJ"],
    "ESTP": ["ISFJ", "ISTJ"],
    "ESFP": ["ISFJ", "ISTJ"]
}

def get_mbti_score(user_mbti, candidate_mbti):
    if candidate_mbti in MBTI_COMPATIBILITY.get(user_mbti, []):
        return 100
    elif user_mbti == candidate_mbti:
        return 80
    else:
        return 50