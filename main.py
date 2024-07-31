from langchain_openai import ChatOpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from ai_rpg_core.prompt_templates import starting_template

load_dotenv()

llm = ChatOpenAI()
output_parser = StrOutputParser()


PROMPT = PromptTemplate(input_variables=["history", "input"], template=starting_template.replace("{player_inventory_initial}", "torch, sword with 100 damage,healing potion x 3, 500 gold"))
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=False,
    memory=ConversationBufferMemory(human_prefix="Player",ai_prefix="Dungeon Master"),
)

# main game loop for text adventure
while True:
    user_input = input(">>> ")
    if user_input == "exit":
        print
        break
    response = conversation.predict(input=user_input)
    print(response)