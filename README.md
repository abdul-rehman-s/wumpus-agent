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
- Reset button to restart agent from beginning

## Tech Stack
- Python (Flask)
- Flask-CORS
- HTML / CSS / JavaScript (Jinja2 Templates)
- Vercel (Deployment)

## Project Structure
- app.py — Flask backend, Knowledge Base, Resolution engine
- templates/index.html — Frontend grid visualization
- requirements.txt — Python dependencies
- vercel.json — Vercel deployment configuration
- README.md — Project documentation

## How to Run Locally
Install dependencies:
pip install -r requirements.txt

Run the app:
python app.py

Then open http://localhost:5000 in your browser.

## Grid Color Legend
- Blue — Agent current position
- Green — Visited safe cells
- Red (bright) — Pit location
- Red (dark) — Wumpus location
- Gold/Yellow — Gold goal cell
- Gray — Unknown unvisited cells

## Algorithm
1. Agent starts at cell (1,1)
2. Receives percepts at current cell (Breeze, Stench, Glitter)
3. TELL: KB is updated with new propositional clauses
4. ASK: Resolution Refutation proves whether adjacent cells are safe
5. Agent moves to a safe cell, or explores unknown if none found
6. Agent stops and wins when Gold cell is reached

## Metrics
- Score: +1000 for finding gold, -1 per move
- Inference Steps: total Resolution algorithm deductions made

## Course Info
- Course: Artificial Intelligence
- University: FAST-NUCES, Chiniot-Faisalabad Campus
- Semester: 6th — Spring 2026
