# AGENT BASED 21 CARD GAME  

## 📌 Index  
1. [Game Introduction and Rules](#game-introduction-and-rules)  
2. [Approach and Framework Selection](#approach-and-framework-selection)  
3. [Game Flow and Steps](#game-flow-and-steps)  
4. [Implementation Instructions](#implementation-instructions)  

---

## 🎮 Game Introduction and Rules  

### **Objective:**  
- Achieve the highest total score under or equal to 21.  
- If all players exceed 21, no winner is declared.  

### **Players:**  
- **User:** Plays with AI Agents.  
- **3 AI Agents:** LLM models act as players and make smart moves.  

### **Gameplay:**  
- Each player starts with **2 random cards**.  
- Players can **Hit (take another card) or Stand (pass)**.  
- Cards have values between **2 and 11**. (Face cards are **10**, Ace is always **11**).  
- **Scores are calculated** at the end of every round.  

### **Winning Criteria:**  
- The player with the **highest valid score (≤ 21) wins** the round.  
- **3 rounds** are played, and the final winner is chosen based on cumulative points.  

---

## 🛠 Approach and Framework Selection  

### **Approach**  
- **LLMs simulate human-like players**, making strategic decisions dynamically.  
- **AI assistants** provide rule explanations and analyze moves in real time.  

### **Framework**  
- **CrewAI:** Manages multiple AI agents with specific roles.  
- **LangChain:** Integrates LLMs for reasoning, memory, and game decision-making.  
- **Flow Feature:** Ensures smooth execution of actions throughout the game.  

### **Defining Agents, Tasks, and Tools**  
- **Agents:** AI-powered entities performing specific actions.  
- **Tasks:** Defined objectives assigned to agents.  
- **Tools:** Functional modules used by agents.  
- **Crew:** A group of agents working together to execute game logic.  

---

## 🔄 Game Flow and Steps  

### **Flow Steps**
1. **Distribute Cards**: Each player receives 2 cards.  
2. **Agent Players' Turn**: AI agents decide to take another card or not.  
3. **User’s Turn**: User can take a card or request advice from an AI expert.  
4. **Score Calculation**: System calculates scores and declares round winners.  
5. **Repeat for 3 Rounds**: The final winner is selected based on cumulative scores.  

### **Key AI Components**
- **Card Distributor (game_host)**: Distributes cards to players.  
- **AI Players (players)**: Decide moves intelligently.  
- **Card Adder (card_adder)**: Handles extra card requests.  
- **Expert AI**: Helps the user make strategic decisions.  

---

## 🚀 Implementation Instructions  

### **1️⃣ Install CrewAI Library**
```bash
pip install crewai
```

### 2️⃣ Set Up the Game Flow
Define agents, tasks, and interactions.
```bash
crewai create flow card_game
```

### 3️⃣ Ensure Proper File Setup
Include the following folders:
```bash
cd /content/card_game
crewai nstall
```

### 3️⃣ Ensure Proper File Setup
Include the following folders:
```bash
├── add_card_crew
├── distribute_crew
├── players_crew
├── winner_decider_crew
```

### 4️⃣ Make sure to include all the code from the attached zip file at the desired
folder.
Include the following folders in the crews folder :
1. add_card_crew
2. distribute_crew
3. players_crew
4. winner_decider_crew

Update the following files using the files in the attached zip file:
1. main.py
2. custom_tool.py

Update the ChatGPT Api key in this file:
1. .env

### 5️⃣ Run this command to start playing the game:
```bash
crewai flow kickoff
```

### Contact:
If there is any confusion, you can reach out to me at 
Email: vsahu@ucsd.edu
LinkedIn: https://www.linkedin.com/in/vivekanand-sahu/
