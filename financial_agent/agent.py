from google.adk.agents.llm_agent import Agent

financial_agent = Agent(
    model='gemini-2.5-flash',
    name='financial_agent',
    description='A helpful asistant for personal finance questions',
    instruction='Answer financial questions with detail and provide plans for the user to achieve goals.',
)

