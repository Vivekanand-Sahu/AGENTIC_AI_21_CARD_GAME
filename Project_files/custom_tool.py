from typing import Type

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


# class MyCustomToolInput(BaseModel):
#     """Input schema for MyCustomTool."""

#     argument: str = Field(..., description="Description of the argument.")


# class MyCustomTool(BaseTool):
#     name: str = "Name of my tool"
#     description: str = (
#         "Clear description for what this tool is useful for, you agent will need this information to use it."
#     )
#     args_schema: Type[BaseModel] = MyCustomToolInput

#     def _run(self, argument: str) -> str:
#         # Implementation goes here
#         return "this is an example of a tool output, ignore it and move along."


from typing import Type, Dict, List
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class MyCustomToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    players: Dict[str, List[str]] = Field(
        ..., 
        description="A dictionary where keys are player names, and values are lists of cards they have."
    )

class MyCustomTool(BaseTool):
    name: str = "Card Score Calculator"
    description: str = (
        "Calculates the total score of cards for each player based on the rules: Cards 2-10 score their number, face cards (J, Q, K) score 10, A scores 11. If the total exceeds 21, the score becomes 0."
    )
    args_schema: Type[BaseModel] = MyCustomToolInput

    def _run(self, players: Dict[str, List[str]]) -> Dict[str, int]:

        def calculate_score(cards: List[str]) -> int:
            scores = {"J": 10, "Q": 10, "K": 10, "A": 11}  # Predefined scores for non-numeric cards
            total = 0
            for card in cards:
                # Check if the card is in the scores dictionary; otherwise, convert it to an integer
                if card in scores:
                    total += scores[card]
                else:
                    total += int(card)
            return total if total <= 21 else 0  



        # Calculate scores for all players
        result = {player: calculate_score(cards) for player, cards in players.items()}
        return result
