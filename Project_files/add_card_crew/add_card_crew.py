from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI


@CrewBase
class AddCardCrew():
	"""Add Card Crew"""

	agents_config = '/content/card_game/src/card_game/crews/add_card_crew/config/agents.yaml'
	tasks_config = '/content/card_game/src/card_game/crews/add_card_crew/config/tasks.yaml'


	@agent
	def card_adder(self) -> Agent:
		return Agent(
			config=self.agents_config['card_adder'],
            llm = ChatOpenAI(model="gpt-4o")
		)

	@task
	def card_adder_for_user(self) -> Task:
		return Task(
			config=self.tasks_config['card_adder_for_user'],
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
