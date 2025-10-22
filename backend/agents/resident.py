
# backend/agents/resident.py
from .tools import AgentTools, RequestStatus, Prediction, RefreshMeta


RESIDENT_SYSTEM_PROMPT = """
You are the CHI-311 Copilot Resident Agent. Your goal is to provide clear, accurate, and helpful information to Chicago residents about their 311 service requests. 

RULES:
1.  **NEVER GUESS.** Only use information provided by the available tools. Do not make up dates, statuses, or reasons.
2.  **Always be helpful and empathetic**, but do not promise outcomes you cannot guarantee.
3.  When providing an ETA, you **MUST** state that it is an *estimate*.
4.  You **MUST** include the confidence level and the date the data was last refreshed in your response.
5.  If you cannot answer a question with the available tools, clearly say so and suggest what you *can* do (e.g., "I can'''t provide details on why it is slow, but I can give you the current status and the estimated completion date.").
"""

class ResidentAgent:
    """An agent that answers resident questions about 311 service requests."""

    def __init__(self, tool_client: AgentTools):
        """
        Initializes the agent with a client to call the necessary tools.
        
        Args:
            tool_client: A class that implements the AgentTools protocol.
        """
        self.tools = tool_client
        

    def get_request_summary(self, sr_number: str) -> str:
        """
        Generates a human-readable summary for a given service request.

        Args:
            sr_number: The service request number.

        Returns:
            A formatted string summarizing the request status and ETA.
        """
        print(f"Agent: Getting summary for {sr_number}")
        
        # 1. Call the tools to get all necessary information
        try:
            status: RequestStatus = self.tools.get_request_status(sr_number)
            prediction: Prediction = self.tools.predict_eta(sr_number)
            meta: RefreshMeta = self.tools.refresh_meta()
        except Exception as e:
           
            return f"I'''m sorry, I was unable to retrieve information for service request {sr_number}. There might be an issue with the system or the ID may be incorrect."

        
        response_template = f"""
        Here is the information for service request #{sr_number}:

        - **Status**: {status['status']}
        - **Category**: {status['category']}
        - **Reported on**: {status['created_date']}

        The **estimated** completion date is **{prediction['eta_date']}**.
        (Confidence: {prediction['confidence']:.0%})

        Please note this is a prediction based on historical data. Factors that might influence this estimate include: {", ".join(prediction['top_factors'])}.

        *Data last refreshed on {meta['data_last_updated']}.*
        """

        

        return response_template.strip()
