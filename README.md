# N.E.X.U.S. (Núcleo de Extração eXpansível para Unificação de Sistemas)

N.E.X.U.S. is an **Agentic AI system** designed to bridge the gap between non-technical users and complex databases by automating **Natural Language to SQL (NL2SQL)** translation.

## 🚀 Key Features
* **Multi-Agent Orchestration**: Built with **CrewAI** to manage specialized agents that handle query planning, SQL generation, and result validation.
* **Anti-Hallucination Logic**: Features optimized agent personas and refined tool-calling logic to ensure the reliability of complex database operations.
* **Unstructured Data Handling**: Designed to process and translate ambiguous natural language queries into precise, executable SQL code.
* **Scalable Architecture**: Flexible backend capable of integrating with various data sources to unify system accessibility.

## 🛠️ Tech Stack
* **Orchestration**: CrewAI.
* **Language**: Python (Advanced).
* **Data**: SQL & PostgreSQL.
* **AI Models**: Integration with GPT-4/local LLMs for reasoning and code generation.

## 📁 Repository Structure
* **/agents**: Definitions of specialized AI personas and their goals.
* **/tools**: Custom tools for database connection and execution logic.
* **/config**: Prompt templates and agent configurations.
* **main.py**: Entry point for the agentic workflow.

## 🔧 Installation & Setup
1. **Clone the repository**.
2. **Install dependencies**:  
   `pip install -r requirements.txt`
3. **Set up your `.env`** with the required LLM API keys.
4. **Run the application**:  
   `streamlit run app.py`