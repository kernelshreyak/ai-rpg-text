from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from ai_rpg_core.prompt_templates import starting_template
from ai_rpg_core.inventory import initial_inventory_basic, initial_inventory_advanced
import streamlit as st



load_dotenv()
if "conversation_chain" not in st.session_state:
    st.session_state["conversation_chain"] = None

st.title('AI RPG Text Adventure')

initial_inventory = st.text_area("Initial inventory: ", initial_inventory_advanced)

if initial_inventory is None:
    initial_inventory = "sword, torch"

if st.session_state["conversation_chain"] is None:
    print("Initializing conversation chain...")
    llm = ChatOpenAI(model="gpt-4o-mini")
    PROMPT = PromptTemplate(input_variables=["history", "input"], template=starting_template.replace("{player_inventory_initial}", initial_inventory))
    conversation = ConversationChain(
        prompt=PROMPT,
        llm=llm,
        verbose=False,
        memory=ConversationBufferMemory(human_prefix="Player",ai_prefix="Dungeon Master"),
    )
    st.session_state["conversation_chain"] = conversation
    print("Conversation chain initialized.")
else:
    print("Reusing conversation chain...")
    conversation = st.session_state["conversation_chain"]

user_input = st.chat_input("Input your action or dialogue",)

if user_input:
    # main game loop for text adventure
    with st.spinner("Generating response..."):
        response = conversation.predict(input=user_input)
        with st.chat_message("assistant"):
            st.write(response)


# if st.button("Save Game"):
#     pickle.dump(conversation, open("conversation.pkl", "wb"))

# if st.button("Load Game"):
#     conversation = pickle.load(open("conversation.pkl", "rb"))
#     st.session_state["conversation_chain"] = conversation