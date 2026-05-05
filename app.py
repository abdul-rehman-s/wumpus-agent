from flask import Flask, render_template, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

ROWS, COLS = 4, 4

# ---------------- WORLD ----------------
class World:
    def __init__(self):
        self.pits = {(2, 3), (3, 1)}
        self.wumpus = (3, 3)
        self.gold = (4, 4)

# ---------------- AGENT ----------------
class Agent:
    def __init__(self):
        self.r, self.c = 1, 1
        self.visited = {(1, 1)}
        self.score = 0
        self.done = False

# ---------------- KB ----------------
KB = []
inference_steps = 0

def tell(clause):
    if clause not in KB:
        KB.append(clause)

# ---------------- RESOLUTION ----------------
def resolve(ci, cj):
    resolvents = []
    for di in ci:
        for dj in cj:
            if di == ("~" + dj) or ("~" + di) == dj:
                new_clause = list(set(ci + cj) - {di, dj})
                resolvents.append(new_clause)
    return resolvents

def resolution(query):
    global inference_steps
    clauses = KB.copy()
    clauses.append([query])

    while True:
        inference_steps += 1
        n = len(clauses)

        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i+1, n)]
        new_clauses = []

        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)

            if [] in resolvents:
                return True

            for r in resolvents:
                if r not in clauses and r not in new_clauses:
                    new_clauses.append(r)

        if not new_clauses:
            return False

        clauses.extend(new_clauses)

# ---------------- INIT ----------------
world = World()
agent = Agent()

# ---------------- PERCEPTS ----------------
def get_percepts(r, c):
    percepts = []

    for pr, pc in world.pits:
        if abs(pr - r) + abs(pc - c) == 1:
            percepts.append("Breeze")

    if abs(world.wumpus[0] - r) + abs(world.wumpus[1] - c) == 1:
        percepts.append("Stench")

    if (r, c) == world.gold:
        percepts.append("Glitter")

    return percepts if percepts else ["Nothing"]

# ---------------- KB UPDATE ----------------
def update_kb(r, c, percepts):
    neighbors = [
        (r+1, c),
        (r-1, c),
        (r, c+1),
        (r, c-1)
    ]

    valid = [(nr, nc) for nr, nc in neighbors if 1 <= nr <= ROWS and 1 <= nc <= COLS]

    # Breeze logic
    if "Breeze" in percepts:
        tell([f"P_{nr}_{nc}" for nr, nc in valid])
    else:
        for nr, nc in valid:
            tell([f"~P_{nr}_{nc}"])

    # Stench logic
    if "Stench" in percepts:
        tell([f"W_{nr}_{nc}" for nr, nc in valid])
    else:
        for nr, nc in valid:
            tell([f"~W_{nr}_{nc}"])

# ---------------- SAFE CHECK ----------------
def is_safe(r, c):
    if not (1 <= r <= ROWS and 1 <= c <= COLS):
        return False

    no_pit = resolution(f"~P_{r}_{c}")
    no_wumpus = resolution(f"~W_{r}_{c}")

    return no_pit and no_wumpus

# ---------------- MOVE ----------------
def step():
    # Stop if gold already found
    if agent.done:
        return

    percepts = get_percepts(agent.r, agent.c)
    update_kb(agent.r, agent.c, percepts)

    # Check if gold found at current cell
    if (agent.r, agent.c) == world.gold:
        agent.score += 1000
        agent.done = True
        return

    moves = [
        (agent.r+1, agent.c),
        (agent.r-1, agent.c),
        (agent.r, agent.c+1),
        (agent.r, agent.c-1)
    ]

    safe_moves = []
    unknown_moves = []

    for r, c in moves:
        if 1 <= r <= ROWS and 1 <= c <= COLS and (r, c) not in agent.visited:
            if is_safe(r, c):
                safe_moves.append((r, c))
            else:
                unknown_moves.append((r, c))

    # Prefer safe unvisited moves
    if safe_moves:
        r, c = random.choice(safe_moves)
        agent.r, agent.c = r, c
        agent.visited.add((r, c))
        agent.score -= 1
        return

    # Explore unknown unvisited
    if unknown_moves:
        r, c = random.choice(unknown_moves)
        agent.r, agent.c = r, c
        agent.visited.add((r, c))
        agent.score -= 1
        return

    # Fallback — revisit any adjacent valid cell
    all_moves = [
        (agent.r+1, agent.c),
        (agent.r-1, agent.c),
        (agent.r, agent.c+1),
        (agent.r, agent.c-1)
    ]
    valid_moves = [(r, c) for r, c in all_moves if 1 <= r <= ROWS and 1 <= c <= COLS]
    if valid_moves:
        r, c = random.choice(valid_moves)
        agent.r, agent.c = r, c
        agent.score -= 1

# ---------------- ROUTES ----------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/state")
def state():
    step()
    return jsonify({
        "agent": [agent.r, agent.c],
        "visited": list(agent.visited),
        "pits": list(world.pits),
        "wumpus": world.wumpus,
        "gold": world.gold,
        "percepts": get_percepts(agent.r, agent.c),
        "score": agent.score,
        "inference_steps": inference_steps,
        "done": agent.done
    })

@app.route("/reset")
def reset():
    global agent, KB, inference_steps
    agent = Agent()
    KB = []
    inference_steps = 0
    return jsonify({"status": "reset"})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
