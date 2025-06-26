from app.services.agent.db_agent_service import DBAgentService

db_agent_service = DBAgentService()
root_agent = db_agent_service.initialize_root_ml_agent()
#
