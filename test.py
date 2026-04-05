import warnings, pandas as pd, numpy as np,logging
from  utils import mark_time, debug

warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.ERROR)

from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.tools import tool
mark_time("process time")
mark_time("model intiation")
# 1. Connect to your local Gemma
model = ChatOllama(model="llama3.2", temperature=0)
mark_time("model intiation")

# 2. Define a dummy tool
@tool
def get_current_balance():
    """Check the current balance of the imaginary bank account."""
    return "₹1,45,000"

# 3. Create the agent
mark_time("initiate agent")
tools = [get_current_balance]
app = create_agent(model, tools )
results = []
i=0
mark_time("initiate agent")
# 4. Ask it a question
mark_time("Agent call")
for chunk in app.stream({"messages": [("user", "What is my balance?")]}):
    mark_time(str(i)+"..iteration")
    results.append(chunk)
    mark_time(str(i)+"..iteration")
    i+=1
mark_time("Agent call")
df = pd.json_normalize(results)

if not df.empty:
    # We look for the last non-null entry in the messages column
    # The column name is usually 'agent.messages' after json_normalize
    last_messages = df['model.messages'].dropna().iloc[-1]
    
    # The last message in that list is the final AI response
    final_ai_msg = last_messages[-1]
    
    print("\n--- Final AI Response ---")
    print(final_ai_msg.content)
else:
    print("No results found in stream.")

mark_time("process time")