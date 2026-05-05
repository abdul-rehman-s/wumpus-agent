# Wumpus World Logic Agent

A web-based Knowledge-Based Agent that navigates a Wumpus World grid using Propositional Logic and Resolution Refutation inference.

## Live Demo
https://wumpus-agent-drab.vercel.app/

## Project Overview
This project implements a Dynamic Pathfinding Agent operating in a Wumpus World-style grid. The agent receives percepts (Breeze, Stench, Glitter) as it moves and uses Propositional Logic to deduce safe cells before each move.

## Features
- 4x4 Wumpus World grid environment
- Propositional Logic Knowledge Base (KB)
- CNF-based Resolution Refutation inference engine
- Percept generation: Breeze (near Pit), Stench (near Wumpus), Glitter (Gold found)
- Safe cell prioritization for agent movement
- Real-time metrics: inference steps and active percepts
- Web-based visualization with Flask backend

## Tech Stack
- Python (Flask)
- Flask-CORS
- HTML/CSS/JavaScript (Jinja2 Templates)
- Vercel (Deployment)

## Project Structure

wumpus-agent/
├── app.py              # Flask backend, KB, Resolution engine
├── templates/
│   └── index.html      # Frontend grid visualization
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel deployment config
└── README.md

## How to Run Locally

pip install -r requirements.txt
python app.py

Then open http://localhost:5000 in your browser.

## Algorithm
1. Agent starts at (1,1)
2. Receives percepts at current cell
3. TELL: KB is updated with new propositional clauses
4. ASK: Resolution Refutation proves whether adjacent cells are safe
5. Agent moves to a safe cell (or explores unknown if none found)
