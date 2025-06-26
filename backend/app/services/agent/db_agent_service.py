# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This class differs from the Agent Service & Agent Service Request in that it instantiates agents directly from classes
rather than relying code. This approach may be more suitable for very complex agents that you don't intend end users or even
Admins to modify

This class is instantiated on the app load
"""
import os
from datetime import date

from fastapi.background import P
from google.genai import types

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import load_artifacts, ToolContext

from tools.bigquery_agent import (
    get_database_settings as get_bq_database_settings,
)
from orm.data_science_agents import return_instructions_root, return_instructions_bigquery, return_instructions_bqml, return_instructions_ds
from tools.db_ds_multiagent import call_db_agent, call_ds_agent
from tools.bigquery_ml_agent import call_db_agent_for_bq_ml

from tools.bigquery_agent import (
    initial_bq_nl2sql,
    run_bigquery_validation,
)


from tools.bigquery_ml_agent import (
    check_bq_models,
    execute_bqml_code,
    rag_response,
)
from orm.data_science_agents import return_instructions_bqml
from enum import Enum


from tools.bigquery_agent import (
    get_database_settings as get_bq_database_settings,
)
from google.adk.code_executors import BuiltInCodeExecutor

from functools import partial


class DBAgentType(Enum):
  bigquery = "BigQuery"
  bigquery_ml = "BigQuery ML"
  analytics = "Analytics"
  root = "Root"


class DBAgentService:

  def __init__(self, instantiate_root_agent: bool = True) -> None:
    """Because we have AgentTools, we use this class in two ways

    1. As a persistent service used by requests to FastAPI endpoints via lifespan
    2. As a way to load the various agents that are utilized as AgentTools in the
        tools functions

    Args:
        instantiate_root_agent: Wheter to create and assign a root agent
    """
    if instantiate_root_agent:
      self.root_agent = self.initialize_root_ml_agent()

  def instantiate_ds_agent(self) -> Agent:
    return Agent(
        model=os.getenv("FLASH_MODEL"),
        name="data_science_agent",
        instruction=return_instructions_ds(),
        # TODO: Play around with VertexAICodeExecutor
        code_executor=BuiltInCodeExecutor(
            stateful=True, optimize_data_file=True
        ),
    )

  # TODO: add in chase ML
  def instantiate_db_agent(self) -> Agent:
    return Agent(
        model=os.getenv("FLASH_MODEL"),
        name="database_agent",
        instruction=return_instructions_bigquery(),
        tools=[
            initial_bq_nl2sql,
            run_bigquery_validation,
        ],
        before_agent_callback=self._setup_before_db_agent_call,
        generate_content_config=types.GenerateContentConfig(temperature=0.01),
    )

  def instantiate_bigquery_ml_agent(self) -> Agent:
    partial_db_agent = partial(
        call_db_agent_for_bq_ml, self.instantiate_db_agent()
    )

    async def helper_db_bq_ml(question: str, tool_context: ToolContext):
      return await partial_db_agent(question, tool_context)

    return Agent(
        model=os.getenv("FLASH_MODEL"),
        name="bq_ml_agent",
        instruction=return_instructions_bqml(
            call_db_agent_name="helper_db_bq_ml"
        ),
        before_agent_callback=self._setup_before_bq_ml_agent_call,
        tools=[
            execute_bqml_code,
            check_bq_models,
            helper_db_bq_ml,
            rag_response,
        ],
    )

  def initialize_root_ml_agent(self) -> Agent:
    """Initialize the root ML agent."""
    bqml_agent = self.instantiate_bigquery_ml_agent()
    partial_db_agent = partial(call_db_agent, self.instantiate_db_agent())
    partial_ds_agent = partial(call_ds_agent, self.instantiate_ds_agent())

    async def helper_db(
        question: str,
        tool_context: ToolContext,
    ):
      return await partial_db_agent(question, tool_context)

    async def helper_ds(
        question: str,
        tool_context: ToolContext,
    ):
      return await partial_ds_agent(question, tool_context)

    return Agent(
        model=os.getenv("PRO_MODEL"),
        name="db_ds_multiagent",
        instruction=return_instructions_root(
            call_db_agent_name="helper_db", call_ds_agent_name="helper_ds"
        ),
        global_instruction=(f"""
                You are a Data Science and Data Analytics Multi Agent System.
                Todays date: {date.today()}
                """),
        sub_agents=[bqml_agent],
        tools=[helper_db, helper_ds, load_artifacts],
        before_agent_callback=self._setup_before_root_agent_call,
        generate_content_config=types.GenerateContentConfig(temperature=0.01),
    )

  # TODO: DRY out the below code
  def _setup_before_root_agent_call(self, callback_context: CallbackContext):
    """Setup the agent."""

    # setting up database settings in session.state
    if "database_settings" not in callback_context.state:
      db_settings = dict()
      db_settings["use_database"] = "BigQuery"
      callback_context.state["all_db_settings"] = db_settings

    # setting up schema in instruction
    if callback_context.state["all_db_settings"]["use_database"] == "BigQuery":
      callback_context.state["database_settings"] = get_bq_database_settings()
      schema = callback_context.state["database_settings"]["bq_ddl_schema"]

      callback_context._invocation_context.agent.instruction = (
          return_instructions_root(
              call_db_agent_name="helper_db", call_ds_agent_name="helper_ds"
          )
          + f"""

        --------- The BigQuery schema of the relevant data with a few sample rows. ---------
        {schema}

        """
      )

  def _setup_before_bq_ml_agent_call(self, callback_context: CallbackContext):
    """Setup the agent."""

    # setting up database settings in session.state
    if "database_settings" not in callback_context.state:
      db_settings = dict()
      db_settings["use_database"] = "BigQuery"
      callback_context.state["all_db_settings"] = db_settings

    # setting up schema in instruction
    if callback_context.state["all_db_settings"]["use_database"] == "BigQuery":
      callback_context.state["database_settings"] = get_bq_database_settings()
      schema = callback_context.state["database_settings"]["bq_ddl_schema"]

      callback_context._invocation_context.agent.instruction = (
          return_instructions_bqml() + f"""

    </BQML Reference for this query>
        
        <The BigQuery schema of the relevant data with a few sample rows>
        {schema}
        </The BigQuery schema of the relevant data with a few sample rows>
        """
      )

  def _setup_before_db_agent_call(self, callback_context: CallbackContext):
    """Setup the agent."""

    if "database_settings" not in callback_context.state:
      callback_context.state["database_settings"] = get_bq_database_settings()
