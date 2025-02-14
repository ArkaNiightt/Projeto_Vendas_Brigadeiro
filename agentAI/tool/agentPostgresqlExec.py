# Removed unused import: os
from langchain import hub
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from utils.models import getModel
from agentAI.prompts.prompt import agents_prompts
import streamlit as st


def agents_executors_database(question: str):
    model = getModel("gpt-4o-2024-11-20")
    database_url = st.secrets["DATABASE_URL"]

    db = SQLDatabase.from_uri(database_uri=database_url)

    toolkit = SQLDatabaseToolkit(
        db=db,
        llm=model
    )

    react_instructions = hub.pull(agents_prompts("PROMPT_REACT_AGENT"))

    agent = create_react_agent(
        llm=model,
        tools=toolkit.get_tools(),
        prompt=react_instructions
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=toolkit.get_tools(),
        verbose=True,
        handle_parsing_errors=True
    )

    prompt_template = PromptTemplate.from_template(
        agents_prompts("PROMPT_BASE_AGENT"))


    output = agent_executor.invoke(
        {
            "input": prompt_template.format(question=question)
        }
    )

    return output.get("output")
