from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from ...tools.custom_tool import MyCustomTool


@CrewBase
class WinnerDeciderCrew():
	"""Winner Decider Crew"""

	agents_config = '/content/card_game/src/card_game/crews/winner_decider_crew/config/agents.yaml'
	tasks_config = '/content/card_game/src/card_game/crews/winner_decider_crew/config/tasks.yaml'
    

	@agent
	def scores_calculator(self) -> Agent:
		return Agent(
			config=self.agents_config['scores_calculator'],
            llm = ChatOpenAI(model="gpt-4o"),
            tools = [MyCustomTool()]
		)

	@task
	def calculate_scores(self) -> Task:
		return Task(
			config=self.tasks_config['calculate_scores'],
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
