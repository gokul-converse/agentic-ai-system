##################### test_classification_agent.py

# from app.agents.domain.document_classification_agent import ClassificationAgent

# agent = ClassificationAgent()

# print(agent.classify("The new iPhone uses advanced AI chips"))

################## test_sentiment_agent.py

# from app.agents.domain.sentiment_analysis_agent import SentimentAgent
# agent = SentimentAgent()

# print(agent.analyse("The new iPhone uses advanced AI chips"))

################### test_summarization_agent.py

from app.agents.domain.summarization_agent import SummarizationAgent
agent = SummarizationAgent()

print(agent.summarize("Who is MS Dhoni?"))
