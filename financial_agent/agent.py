from google.adk.agents.llm_agent import Agent

financial_agent = Agent(
    model='gemini-2.5-flash',
    name='financial_agent',
    description='A helpful assistant for user financial guidance.',
    instruction='Answer user questions to the best of your knowledge about financial matters and create plans for them to achive financial goals.',
)
