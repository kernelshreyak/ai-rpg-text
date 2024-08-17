from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv
from ai_rpg_core.game_types import RPGBasicRandom,RPGFixedCampaign
from ai_rpg_core.character_backgrounds import *
from ai_rpg_core.inventory import *
import streamlit as st
import json

load_dotenv()

if "conversation_chain" not in st.session_state:
    st.session_state["conversation_chain"] = None

st.title('AI RPG Text Adventure')

# create a game based on a template
# game = RPGBasicRandom(inventory=initial_inventory_mage_advanced,is_fixed=True)
game = RPGFixedCampaign(inventory=king_alof_inventory,backstory=king_alof_backstory)

llm_chosen = st.radio("LLM", ("GPT-4-o-mini", "Gemini-1.5-flash"), key="llm_chosen")
st.text_area("Initial inventory: ", game.inventory,disabled=True)

def create_conversation_chain():
    if llm_chosen == "GPT-4-o-mini":
        # good for detailed responses (this is the default LLM to be usd in the project)
        llm = ChatOpenAI(model="gpt-4o-mini") 
    elif llm_chosen == "Gemini-1.5-flash":
        # good for short and quick responses with large context window
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash") 

    PROMPT = PromptTemplate(input_variables=["history", "input"], template=game.template)
    memory = ConversationBufferMemory(human_prefix="Player", ai_prefix="Dungeon Master")
    return ConversationChain(
        prompt=PROMPT,
        llm=llm,
        verbose=False,
        memory=memory,
    )

if st.session_state["conversation_chain"] is None:
    print("Initializing conversation chain...")
    conversation = create_conversation_chain()
    st.session_state["conversation_chain"] = conversation
    print("Conversation chain initialized.")
else:
    print("Reusing conversation chain...")
    conversation = st.session_state["conversation_chain"]


def save_conversation(conversation, filename):
    # Extract and save memory contents
    memory_contents = conversation.memory.chat_memory.messages
    serializable_memory = []
    for msg in memory_contents:
        if isinstance(msg, HumanMessage):
            serializable_memory.append({"type": "human", "content": msg.content})
        elif isinstance(msg, AIMessage):
            serializable_memory.append({"type": "ai", "content": msg.content})
    
    with open(f'{filename}_memory.json', 'w') as f:
        json.dump(serializable_memory, f)

def load_conversation(filename):
    # Load memory contents
    with open(f'{filename}_memory.json', 'r') as f:
        serializable_memory = json.load(f)
    
    memory_contents = []
    for msg in serializable_memory:
        if msg["type"] == "human":
            memory_contents.append(HumanMessage(content=msg["content"]))
        elif msg["type"] == "ai":
            memory_contents.append(AIMessage(content=msg["content"]))

    # Recreate the conversation chain and memory
    conversation = create_conversation_chain()
    conversation.memory.chat_memory.messages = memory_contents

    return conversation


if st.button("Save Game"):
    save_conversation(conversation, "conversation")
    st.success("Game saved successfully!")

if st.button("Load Game"):
    conversation = load_conversation("conversation")
    st.session_state["conversation_chain"] = conversation
    st.success("Game loaded successfully!")

# st.markdown("Welcome to the adventure: " + game.template)

user_input = st.chat_input("Input your action or dialogue")
if user_input:
    # main game loop for text adventure
    with st.spinner("Performing action..."):
        response = conversation.predict(input=user_input)
        with st.chat_message("assistant"):
            st.write(response)


