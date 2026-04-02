import os
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

# ─────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────

load_dotenv()  # Load environment variables from .env file

LLM = "groq/llama-3.3-70b-versatile"

TOPIC = "Machine Learning fundamentals"  # ← change this to anything you like!

# ─────────────────────────────────────────
# AGENTS
# ─────────────────────────────────────────

curriculum_designer = Agent(
    role="Expert Curriculum Designer",
    goal=f"Outline the most important concepts for learning {TOPIC} in the best possible order",
    backstory="""You are a seasoned curriculum designer with 20 years of experience 
    building learning programs at top universities. You have a gift for identifying 
    exactly which concepts matter most and the ideal sequence to teach them in. 
    You always think about what a beginner needs to understand first before they 
    can grasp more advanced ideas.""",
    llm=LLM,
    verbose=True,
    allow_delegation=False
)

expert_teacher = Agent(
    role="Expert Teacher and Explainer",
    goal=f"Transform the curriculum outline into clear, engaging explanations with memorable examples for {TOPIC}",
    backstory="""You are a brilliant educator who has taught at MIT and Stanford. 
    You are famous for making complex concepts feel simple and intuitive. 
    You always use real-world analogies and concrete examples. 
    Students love your explanations because they make things click immediately.""",
    llm=LLM,
    verbose=True,
    allow_delegation=False
)

assessment_specialist = Agent(
    role="Assessment and Quiz Specialist",
    goal=f"Create a comprehensive, effective quiz that tests genuine understanding of {TOPIC}",
    backstory="""You are an expert in educational assessment design with a PhD in 
    learning science. You know the difference between questions that test memorization 
    and questions that test real understanding. You always include a mix of question 
    types and difficulty levels, and you write clear, unambiguous answer keys.""",
    llm=LLM,
    verbose=True,
    allow_delegation=False
)

# ─────────────────────────────────────────
# 4TH AGENT: FLASHCARD MAKER
# ─────────────────────────────────────────

flashcard_maker = Agent(
    role="Expert Flashcard and Memory Specialist",
    goal=f"Create a complete set of Anki-style flashcards that make {TOPIC} easy to memorize and retain long-term",
    backstory="""You are a memory and learning expert who has spent 15 years studying 
    spaced repetition and active recall techniques. You are famous in the learning 
    community for creating flashcards that are perfectly scoped — never too broad, 
    never too narrow. You know that the best flashcard tests exactly one idea per card, 
    uses simple language, and forces the brain to actively retrieve information rather 
    than passively recognize it. You have helped thousands of students pass exams and 
    retain knowledge for life using your flashcard systems.""",
    llm=LLM,
    verbose=True,
    allow_delegation=False
)

# ─────────────────────────────────────────
# TASKS
# ─────────────────────────────────────────

outline_task = Task(
    description=f"""Create a comprehensive learning outline for the topic: {TOPIC}

    Your outline must include:
    - Exactly 5 key concepts, listed in the ideal learning order
    - For each concept:
        * A one-sentence description of what it is
        * Why it is important to understand
        * What prior knowledge is needed (prerequisites)
        * Estimated time to understand it (e.g. "30 minutes", "1 hour")
    
    Keep the language clear and beginner-friendly.
    Format your output as clean, readable markdown.""",
    
    expected_output="""A markdown outline with exactly 5 key concepts. 
    Each concept has a description, importance, prerequisites, and time estimate.""",
    
    agent=curriculum_designer
)

explanations_task = Task(
    description=f"""Using the outline provided, write detailed study content for each of the 5 concepts in {TOPIC}.

    For EACH concept write:
    - A clear explanation (2-3 short paragraphs, beginner friendly)
    - One real-world analogy or example that makes it concrete
    - A "Key Takeaways" section with exactly 3 bullet points

    Requirements:
    - Use plain, conversational language — no unnecessary jargon
    - If jargon is unavoidable, define it immediately
    - Format everything as clean, well-structured markdown with headers
    - Make sure each explanation builds naturally on the previous one""",
    
    expected_output="""A complete markdown document with explanations, 
    real-world examples, and key takeaways for all 5 concepts.""",
    
    agent=expert_teacher
)

quiz_task = Task(
    description=f"""Using the study material provided, create a thorough quiz to test understanding of {TOPIC}.

    The quiz must include all of the following sections:

    ## Section 1: Multiple Choice (5 questions)
    - 4 answer options each (A, B, C, D)
    - Mix of easy, medium, and hard questions
    - Test understanding, not just memorization

    ## Section 2: Short Answer (3 questions)  
    - Require 2-4 sentence answers
    - Focus on explaining concepts in the student's own words

    ## Section 3: Apply It! (2 scenario questions)
    - Give a real-world scenario and ask the student to apply what they learned
    - These should be the most interesting and challenging questions

    ## Answer Key
    - Full answers for every question in all three sections
    - For multiple choice: explain WHY each correct answer is right
    - For short answer and scenarios: provide a model answer

    Format everything as clean markdown.""",
    
    expected_output="""A complete quiz with all three sections (multiple choice, 
    short answer, scenario) plus a full answer key. Formatted in markdown.""",
    
    agent=assessment_specialist
)

# ─────────────────────────────────────────
# 4TH TASK: FLASHCARDS
# ─────────────────────────────────────────

flashcard_task = Task(
    description=f"""Using ALL of the study material, explanations, and quiz questions created so far,
    produce a complete set of Anki-style flashcards for {TOPIC}.

    Rules for great flashcards:
    - Each card tests EXACTLY one idea — never cram two concepts into one card
    - Front of card: a question, prompt, or incomplete sentence
    - Back of card: a short, direct answer (1-3 sentences max)
    - Use simple, clear language — avoid copying long paragraphs
    - Prefer "How does X work?" or "What is the difference between X and Y?" 
      over simple "What is X?" definition cards
    - Include a "Memory Hook" on the back of harder cards — 
      a short analogy or trick to help it stick

    You must produce cards in these three categories:

    ### Category 1: Core Definitions (10 cards)
    - One card per key term or concept
    - Front: "What is [term]?"
    - Back: A crisp 1-2 sentence definition + Memory Hook if helpful

    ### Category 2: Concept Connections (8 cards)
    - Test how concepts relate to each other
    - Front: "What is the difference between X and Y?" or "How does X lead to Y?"
    - Back: A clear comparison or explanation of the relationship

    ### Category 3: Apply It (7 cards)
    - Scenario-based cards that test real understanding
    - Front: A short real-world situation or problem
    - Back: The correct approach or answer with a brief explanation

    Format every card exactly like this:

    ---
    **Card [number] — [Category Name]**
    **Front:** [question or prompt]
    **Back:** [answer]
    **Memory Hook:** [optional, only for tricky cards]
    ---

    Total: 25 cards across all three categories.
    Save everything as clean, readable markdown.""",

    expected_output="""Exactly 25 flashcards formatted in markdown, 
    split across 3 categories: Core Definitions (10), 
    Concept Connections (8), and Apply It (7). 
    Each card has a Front and Back, and harder cards have a Memory Hook.""",

    agent=flashcard_maker,
    output_file="study_guide.md"  # saves the final combined output
)

# ─────────────────────────────────────────
# CREW
# ─────────────────────────────────────────

crew = Crew(
    agents=[curriculum_designer, expert_teacher, assessment_specialist, flashcard_maker],
    tasks=[outline_task, explanations_task, quiz_task, flashcard_task],
    verbose=True
)

# ─────────────────────────────────────────
# RUN IT
# ─────────────────────────────────────────

print(f"\nStarting Study Guide Creator for: {TOPIC}\n")
print("=" * 60)

result = crew.kickoff()

print("\n" + "=" * 60)
print("Done! Your study guide has been saved to: study_guide.md")
print("=" * 60)