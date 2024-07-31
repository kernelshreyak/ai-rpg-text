# AI RPG Text Adventure

This project is a text-based RPG adventure game driven by an AI Dungeon Master (DM). The DM generates a solo RPG adventure based on Dungeons & Dragons (DnD) 5e rules, but with simplified mechanics. The player interacts with the game by typing commands, and the AI responds by advancing the story.

## Features

- AI-driven Dungeon Master to generate and control the game world.
- Memory support to maintain conversation context throughout the game session.
- Simplified DnD 5e mechanics for ease of play.

## Requirements

- Python 3.7+
- `langchain_openai`
- `langchain_core`
- `langchain`
- `dotenv`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/ai-rpg-text-adventure.git
   cd ai-rpg-text-adventure

2. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```
3. **Install the dependencies:**
4. **Set up environment variables:**


## Usage
Run the game by executing the main.py script:

```bash
python main.py
```


## Game Loop

 - User Input: Type your commands to interact with the game: performing navigation and combat actions.
 - Exit: Type exit to end the game.
    