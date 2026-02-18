from app.agents.base import BaseAgent

agent = BaseAgent(name="base-test-agent", role="Testing BaseAgent behavior")

response = agent.run("Who is MSDhoni?")
print(response)
