from enum import Enum


class AgentType(Enum):
  LLM = "LLM"
  Sequential = "Sequential"
  Parallel = "Parallel"
  Loop = "Loop"
  CodeExecutor = "CodeExecutor"


class AgentNames(Enum):
  ROOT = "root_agent"
