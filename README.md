# Study Guide Creator Crew

An AI-powered multi-agent system built with [CrewAI](https://crewai.com) that automatically generates a complete study guide for any topic — including explanations, a quiz, and flashcards — in minutes.

---

## What It Does

Give it any topic and four specialized AI agents collaborate inside a CrewAI Flow to produce a complete markdown study guide:

| Agent | Model | Role |
|---|---|---|
| Curriculum Designer | Groq Llama 3 8b (fast) | Outlines the 5 most important concepts in the best learning order |
| Expert Teacher | Groq Llama 3 70b (smart) | Writes clear explanations with real-world examples |
| Assessment Specialist | Groq Llama 3 70b (smart) | Creates a multi-section quiz with a full answer key |
| Flashcard Maker | Groq Llama 3 70b (smart) | Produces 25 Anki-style flashcards across 3 categories |

The quiz and flashcard tasks run in **parallel**, cutting total runtime significantly.

---

## Example Output

For the topic `"Machine Learning fundamentals"` the system produces a file called `study_guide_machine_learning_fundamentals.md` containing:

- A structured outline of 5 key concepts with time estimates
- Beginner-friendly explanations with analogies and key takeaways
- A quiz with multiple choice, short answer, and scenario-based questions plus a full answer key
- 25 flashcards split across Core Definitions, Concept Connections, and Apply It categories

---

## How It Works

The system uses a **CrewAI Flow** to orchestrate everything in four stages:

```
load_topic → run_crew → save_output → finish
```

Inside the crew, tasks run in this order:

```
Curriculum Designer → Expert Teacher → [Quiz Specialist + Flashcard Maker in parallel]
        ↓                    ↓                          ↓
    Outline (5          Explanations             Both outputs saved
    concepts)           + examples               to one markdown file
```

Key concepts used:
- **Multi-model** — simple tasks use a smaller faster model, complex writing tasks use a larger smarter one
- **Parallel execution** — quiz and flashcard tasks run at the same time
- **CrewAI Flow** — wraps the crew with load, run, save, and finish stages
- **Role-playing** — each agent has a specific expert persona
- **Sequential + async execution** — outline and explanations run first, then quiz and flashcards run together

---

## Getting Started

### Prerequisites

- Python 3.9+
- A free [Groq API key](https://console.groq.com) (no credit card required)

### Installation

```bash
# Clone the repository
git clone https://github.com/malavika-anand/study-guide-crew.git
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

Your study guide will be saved as `study_guide_<topic>.md` when the flow finishes.

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

## Changing the Models

All models use Groq's free tier. You can swap them at the top of the script:

```python
GROQ_FAST = "groq/llama3-8b-8192"     # used for simpler tasks — fastest
GROQ_SMART = "groq/llama3-70b-8192"   # used for writing tasks — best quality
```

Other free options on Groq:
```python
"groq/mixtral-8x7b-32768"   # great for long outputs
```

---

## Project Structure

```
study-guide-crew/
├── study_crew.py      # main script — agents, tasks, crew, and flow
├── .env               # your API key (never commit this)
├── .gitignore         # keeps .env and output files out of git
└── README.md          # this file
```

---

## What Gets Generated

Running the script produces a file named after your topic, for example:

```
study_guide_machine_learning_fundamentals.md
```

The file contains all four sections in order: outline, explanations, quiz, and flashcards.

---

## Built With

- [CrewAI](https://github.com/joaomdmoura/crewAI) — multi-agent framework with Flows support
- [Groq](https://groq.com) — free LLM inference (LLaMA 3 8b and 70b)
- [python-dotenv](https://github.com/theskumar/python-dotenv) — environment variable management

---

## Contributing

Pull requests are welcome. Feel free to open an issue if you have ideas for new agents or improvements.

---

## License

MIT
