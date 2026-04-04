import os
from crewai import Agent, Task, Crew
from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────

GROQ_FAST = "groq/llama-3.1-8b-instant"

GROQ_SMART = "groq/llama-3.3-70b-versatile"

# ─────────────────────────────────────────
# TOPIC — change this to anything you like
# ─────────────────────────────────────────

TOPIC = "Machine Learning fundamentals"

# ─────────────────────────────────────────
# AGENTS
# ─────────────────────────────────────────

curriculum_designer = Agent(
    role="Expert Curriculum Designer",
    goal=f"Outline the most important concepts for learning {TOPIC} in the best possible order",
    backstory="""You are a seasoned curriculum designer with 20 years of experience 
    building learning programs at top universities. You identify exactly which concepts 
    matter most and the ideal sequence to teach them in.""",
    llm=GROQ_FAST,       
    verbose=True,
    allow_delegation=False
)

expert_teacher = Agent(
    role="Expert Teacher and Explainer",
    goal=f"Transform the curriculum outline into clear, engaging explanations with memorable examples for {TOPIC}",
    backstory="""You are a brilliant educator who has taught at MIT and Stanford. 
    You are famous for making complex concepts feel simple and intuitive. 
    You always use real-world analogies and concrete examples.""",
    llm=GROQ_SMART,      
    verbose=True,
    allow_delegation=False
)

assessment_specialist = Agent(
    role="Assessment and Quiz Specialist",
    goal=f"Create a comprehensive, effective quiz that tests genuine understanding of {TOPIC}",
    backstory="""You are an expert in educational assessment design with a PhD in 
    learning science. You know the difference between questions that test memorization 
    and questions that test real understanding.""",
    llm=GROQ_SMART,      
    verbose=True,
    allow_delegation=False
)

flashcard_maker = Agent(
    role="Expert Flashcard and Memory Specialist",
    goal=f"Create a complete set of Anki-style flashcards that make {TOPIC} easy to memorize and retain long-term",
    backstory="""You are a memory and learning expert who has spent 15 years studying 
    spaced repetition and active recall techniques. You are famous for creating flashcards 
    that test exactly one idea per card using simple language.""",
    llm=GROQ_SMART,      
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
        * Estimated time to understand it
    
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
    - Use plain, conversational language
    - Define any jargon immediately
    - Format everything as clean markdown with headers""",
    
    expected_output="""A complete markdown document with explanations, 
    real-world examples, and key takeaways for all 5 concepts.""",
    
    agent=expert_teacher
)

# ── PARALLEL: quiz and flashcards run at the same time ──

quiz_task = Task(
    description=f"""Using the study material provided, create a thorough quiz to test understanding of {TOPIC}.

    The quiz must include:

    ## Section 1: Multiple Choice (5 questions)
    - 4 answer options each (A, B, C, D)
    - Mix of easy, medium, and hard questions

    ## Section 2: Short Answer (3 questions)
    - Require 2-4 sentence answers
    - Focus on explaining concepts in the student's own words

    ## Section 3: Apply It! (2 scenario questions)
    - Real-world scenarios that test genuine understanding

    ## Answer Key
    - Full answers for every question
    - For multiple choice: explain WHY each answer is correct

    Format everything as clean markdown.""",
    
    expected_output="""A complete quiz with all three sections plus a full answer key.""",
    
    agent=assessment_specialist,
)

flashcard_task = Task(
    description=f"""Using ALL of the study material and explanations created so far,
    produce a complete set of Anki-style flashcards for {TOPIC}.

    Rules for great flashcards:
    - Each card tests EXACTLY one idea
    - Front: a question or prompt
    - Back: a short direct answer (1-3 sentences max)
    - Include a Memory Hook on harder cards

    ### Category 1: Core Definitions (10 cards)
    - Front: "What is [term]?"
    - Back: crisp 1-2 sentence definition + Memory Hook if helpful

    ### Category 2: Concept Connections (8 cards)
    - Front: "What is the difference between X and Y?"
    - Back: clear comparison or explanation

    ### Category 3: Apply It (7 cards)
    - Front: a short real-world scenario
    - Back: the correct approach with brief explanation

    Format every card exactly like this:

    ---
    **Card [number] — [Category Name]**
    **Front:** [question or prompt]
    **Back:** [answer]
    **Memory Hook:** [optional]
    ---

    Total: 25 cards.""",

    expected_output="""Exactly 25 flashcards split across 3 categories. 
    Each card has a Front and Back. Harder cards have a Memory Hook.""",

    agent=flashcard_maker,
    async_execution=True   
)

# ─────────────────────────────────────────
# CREW
# ─────────────────────────────────────────

study_crew = Crew(
    agents=[curriculum_designer, expert_teacher, assessment_specialist, flashcard_maker],
    tasks=[outline_task, explanations_task, quiz_task, flashcard_task],
    verbose=True
)

# ─────────────────────────────────────────
# FLOW
# ─────────────────────────────────────────

class StudyGuideFlow(Flow):

    @start()
    def load_topic(self):
        print(f"\nStudy Guide Flow started for: {TOPIC}\n")
        print("=" * 60)
        return TOPIC

    @listen(load_topic)
    def run_crew(self, topic):
        print(f"\nAgents are working on: {topic}\n")
        result = study_crew.kickoff()
        return result

    @listen(run_crew)
    def save_output(self, result):
        print("\n💾 Saving study guide...\n")

        # Combine all task outputs into one markdown file
        output = f"# Study Guide: {TOPIC}\n\n"
        output += "---\n\n"

        for i, task_output in enumerate(study_crew.tasks):
            if hasattr(task_output, 'output') and task_output.output:
                output += f"{task_output.output}\n\n"
                output += "---\n\n"

        # Save to file
        filename = f"study_guide_{TOPIC.lower().replace(' ', '_')}.md"
        with open(filename, "w") as f:
            f.write(output)

        print(f"Study guide saved to: {filename}")
        return filename

    @listen(save_output)
    def finish(self, filename):
        print("\n" + "=" * 60)
        print(f"Done! Your study guide is ready: {filename}")
        print("=" * 60)
        return filename


# ─────────────────────────────────────────
# RUN
# ─────────────────────────────────────────

if __name__ == "__main__":
    flow = StudyGuideFlow()
    flow.kickoff()