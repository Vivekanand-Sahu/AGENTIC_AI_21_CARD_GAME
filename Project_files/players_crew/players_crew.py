from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI


@CrewBase
class PlayersCrew():
	"""Players Crew"""

	agents_config = '/content/card_game/src/card_game/crews/players_crew/config/agents.yaml'
	tasks_config = '/content/card_game/src/card_game/crews/players_crew/config/tasks.yaml'


	@agent
	def players(self) -> Agent:
		return Agent(
			config=self.agents_config['players'],
            llm = ChatOpenAI(model="gpt-4o")
		)

	@task
	def add_card_for_player(self) -> Task:
		return Task(
			config=self.tasks_config['add_card_for_player'],
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
