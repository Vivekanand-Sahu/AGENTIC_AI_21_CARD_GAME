from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI


@CrewBase
class DistributeCrew():
	"""Distribute Crew"""

	agents_config = '/content/card_game/src/card_game/crews/distribute_crew/config/agents.yaml'
	tasks_config = '/content/card_game/src/card_game/crews/distribute_crew/config/tasks.yaml'


	@agent
	def game_host(self) -> Agent:
		return Agent(
			config=self.agents_config['game_host'],
            llm = ChatOpenAI(model="gpt-4o")
		)

	@task
	def distribute_cards(self) -> Task:
		return Task(
			config=self.tasks_config['distribute_cards'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Research Crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
		)
