import fitz

def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text


def calculate_score(resume_text, job_desc):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_desc.lower().split())

    if len(job_words) == 0:
        return 0

    matched = resume_words.intersection(job_words)
    return round((len(matched) / len(job_words)) * 100, 2)