# Study Guide Creator Crew

An AI-powered multi-agent system built with [CrewAI](https://crewai.com) that automatically generates a complete study guide for any topic — including explanations, a quiz, and flashcards — in minutes.

---

## What It Does

Give it any topic and four specialized AI agents collaborate to produce a full `study_guide.md` file:

| Agent | Role |
|---|---|
| Curriculum Designer | Outlines the 5 most important concepts in the best learning order |
| Expert Teacher | Writes clear explanations with real-world examples |
| Assessment Specialist | Creates a multi-section quiz with a full answer key |
| Flashcard Maker | Produces 25 Anki-style flashcards across 3 categories |

---

## Example Output

For the topic `"Machine Learning fundamentals"` the system produces:

- A structured outline of 5 key concepts with time estimates
- Beginner-friendly explanations with analogies and key takeaways
- A quiz with multiple choice, short answer, and scenario-based questions
- 25 flashcards split across Core Definitions, Concept Connections, and Apply It categories

---

## Getting Started

### Prerequisites

- Python 3.9+
- A free [Groq API key](https://console.groq.com) (no credit card required)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/study-guide-crew.git
cd study-guide-crew

# Install dependencies
pip install crewai python-dotenv
```

### Configuration

Create a `.env` file in the root of the project:

```
GROQ_API_KEY=your_groq_api_key_here
```

### Usage

Open `study_crew.py` and set your topic:

```python
TOPIC = "Machine Learning fundamentals"  # change this to anything you like
```

Then run it:

```bash
python study_crew.py
```

Your study guide will be saved to `study_guide.md` when the agents finish.

---

## Changing the Topic

You can set `TOPIC` to anything, for example:

```python
TOPIC = "How the stock market works"
TOPIC = "The history of the Roman Empire"
TOPIC = "Cooking techniques for beginners"
TOPIC = "How DNS works"
TOPIC = "Introduction to Python programming"
```

---

## Changing the Model

The project uses Groq's free tier. You can swap the model at the top of the script:

```python
LLM = "groq/llama3-70b-8192"    # default — best quality
LLM = "groq/mixtral-8x7b-32768" # great for long outputs
LLM = "groq/llama3-8b-8192"     # fastest
```

---

## Project Structure

```
study-guide-crew/
├── study_crew.py      # main script with all agents and tasks
├── .env               # your API key (never commit this)
├── .gitignore         # keeps .env and output files out of git
└── README.md          # this file
```

---

## How It Works

This project is built on the concepts taught in the [DeepLearning.AI Multi AI Agents with CrewAI](https://learn.deeplearning.ai) course. The four agents run sequentially, with each agent passing its output to the next:

```
Curriculum Designer → Expert Teacher → Assessment Specialist → Flashcard Maker
        ↓                    ↓                   ↓                    ↓
    Outline (5          Explanations          Quiz with            25 Anki-style
    concepts)           + examples           answer key            flashcards
```

Key CrewAI concepts used:
- **Role-playing** — each agent has a specific expert persona
- **Focus** — each agent does exactly one job
- **Sequential execution** — output of each task feeds the next
- **File output** — final result saved to `study_guide.md`

---

## Built With

- [CrewAI](https://github.com/joaomdmoura/crewAI) — multi-agent framework
- [Groq](https://groq.com) — free LLM inference (LLaMA 3, Mixtral)
- [python-dotenv](https://github.com/theskumar/python-dotenv) — environment variable management

---

## Contributing

Pull requests are welcome. Feel free to open an issue if you have ideas for new agents or improvements.

---

## License

MIT
