from difflib import SequenceMatcher

def similarity_score(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def evaluate_response(predicted, expected):
    score = similarity_score(predicted, expected)

    return {
        "similarity": score,
        "is_correct": score > 0.6
    }