from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage
from dotenv import load_dotenv
from ai_rpg_core.prompt_templates import starting_template
from ai_rpg_core.inventory import initial_inventory_basic, initial_inventory_advanced
import streamlit as st
import json

load_dotenv()

if "conversation_chain" not in st.session_state:
    st.session_state["conversation_chain"] = None

st.title('AI RPG Text Adventure')

initial_inventory = st.text_area("Initial inventory: ", initial_inventory_advanced)

if initial_inventory is None:
    initial_inventory = "sword, torch"

def create_conversation_chain(initial_inventory):
    llm = ChatOpenAI(model="gpt-4o-mini")
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=starting_template.replace("{player_inventory_initial}", initial_inventory))
    memory = ConversationBufferMemory(human_prefix="Player", ai_prefix="Dungeon Master")
    return ConversationChain(
        prompt=PROMPT,
        llm=llm,
        verbose=False,
        memory=memory,
    )

if st.session_state["conversation_chain"] is None:
    print("Initializing conversation chain...")
    conversation = create_conversation_chain(initial_inventory)
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

def load_conversation(filename, initial_inventory):
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
    conversation = create_conversation_chain(initial_inventory)
    conversation.memory.chat_memory.messages = memory_contents

    return conversation


if st.button("Save Game"):
    save_conversation(conversation, "conversation")
    st.success("Game saved successfully!")

if st.button("Load Game"):
    conversation = load_conversation("conversation", initial_inventory)
    st.session_state["conversation_chain"] = conversation
    st.success("Game loaded successfully!")

user_input = st.chat_input("Input your action or dialogue")
if user_input:
    # main game loop for text adventure
    with st.spinner("Performing action..."):
        response = conversation.predict(input=user_input)
        with st.chat_message("assistant"):
            st.write(response)


