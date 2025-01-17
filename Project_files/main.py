#!/usr/bin/env python
from random import randint
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, or_, and_
#from .crews.poem_crew.poem_crew import PoemCrew
#from .crews.poem_crew.game_crew import GameCrew
from .crews.distribute_crew.distribute_crew import DistributeCrew
from .crews.players_crew.players_crew import PlayersCrew
from .crews.add_card_crew.add_card_crew import AddCardCrew
from .crews.winner_decider_crew.winner_decider_crew import WinnerDeciderCrew

import ast

final_records = {'Player1': 0, 'Player2': 0, 'Player3': 0,  'User': 0}

def string_to_dict(input_string):
    try:
        result_dict = ast.literal_eval(str(input_string))
        if isinstance(result_dict, dict):
            return(result_dict)
        else:
            raise ValueError("The input string does not represent a dictionary.")
    except (SyntaxError, ValueError) as e:
        print(f"Error: {e}")
        return None


def find_winner(final_records):
    print(f"\n {final_records}")
    # Check if all scores are 0
    if all(score == 0 for score in final_records.values()):
        print("No winner")
        return
    
    # Find the highest score
    max_score = max(final_records.values())
    
    # Find all players with the highest score
    winners = [player for player, score in final_records.items() if score == max_score]
    

    # Output the result
    if len(winners) > 1:
        print(f"It's a tie! Winners: {', '.join(winners)} with a score of {max_score}")
    else:
        
        if winners[0] == "User":
            print(f"You Win with a score of {max_score}")
        else:
            print(f"The winner is {winners[0]} with a score of {max_score}")


class GameState(BaseModel):
    player_scores: dict = {}
    player_cards: dict = {'Player1':[], 'Player2':[], 'Player3':[], 'User':[]}
    player_cards_hidden: dict = {}
    player1_decision: str = ''


class GameFlow(Flow[GameState]):

    @start()
    def dealer_distributes_cards(self):
        print("Distributing cards to all plaryers")
        result = (
            DistributeCrew()
            .crew()
            .kickoff(
                inputs={
                    "player_cards" : self.state.player_cards
                }
            )            
        )
        result_dict = string_to_dict(result)
        print('The round starts with these cards', result_dict)
        self.state.player_cards = result_dict
        self.state.player_cards_hidden = result_dict

    @listen(dealer_distributes_cards)
    def agent_player_decides(self):
        agent_players = list(self.state.player_cards.keys())
        agent_players.remove('User')

        for player in agent_players:
            print(f"Asking {player}")
            result = (
                PlayersCrew()
                .crew()
                .kickoff(
                    inputs={
                        "player_cards" : self.state.player_cards,
                        "player" : player
                        }
                    )
            )
            assert str(result) == 'yes' or str(result) == 'no'

            # appending a card
            if str(result) == 'yes':
                print(f"Adding card for {player}")
                result_2 = (
                    AddCardCrew()
                    .crew()
                    .kickoff(
                        inputs={
                            "player_cards" : self.state.player_cards,
                            "player" : player
                            }
                        )
                )
                print(f'{player} took an additional card', result_2)
                result_dict = string_to_dict(result_2)
                self.state.player_cards_hidden[player] = result_dict[player]

            else:
                print(f'{player} did not take an additional card')
        
        print('All the other players took/rejected additional cards')

    @listen(agent_player_decides)
    def user_decides_and_adds(self):
        print('Do you want another card? Write "yes"/"no"/"help"')
        inp = input()
        assert inp == "yes" or inp == "no" or inp == "help"

        if inp == 'yes':
            print("Adding card for You")
            result = (
                AddCardCrew()
                .crew()
                .kickoff(
                    inputs={
                        "player_cards" : self.state.player_cards,
                        "player" : "User"
                        }
                    )
            )
            print(f'Card added for You', result)
            result_dict = string_to_dict(result)
            self.state.player_cards_hidden["User"] = result_dict["User"]

        elif inp == "help":
            print(f"Asking Expert to help You")
            result = (
                PlayersCrew()
                .crew()
                .kickoff(
                    inputs={
                        "player_cards" : self.state.player_cards,
                        "player" : "User"
                        }
                    )
            )
            assert str(result) == 'yes' or str(result) == 'no'

            # appending a card
            if str(result) == 'yes':
                result_2 = (
                    AddCardCrew()
                    .crew()
                    .kickoff(
                        inputs={
                            "player_cards" : self.state.player_cards,
                            "player" : "User"
                            }
                        )
                )
                print(f'The expert took an additional card for You', result_2)
                result_dict = string_to_dict(result_2)
                self.state.player_cards_hidden["User"] = result_dict["User"]
            else:
                print('The expert did not take any additional card for You')

        else:
            print(f'You did not take any additional card')
    
    @listen(and_(dealer_distributes_cards, agent_player_decides, user_decides_and_adds))
    def round_winner_announcement(self):
        print('All the players completed their moves"')
        result = (
            WinnerDeciderCrew()
            .crew()
            .kickoff(
                inputs={
                    "player_cards" : self.state.player_cards,
                    }
                )
        )
        result_dict = string_to_dict(result)
        self.state.player_scores = result_dict

        find_winner(self.state.player_scores)



    @listen(and_(dealer_distributes_cards, agent_player_decides, user_decides_and_adds, round_winner_announcement))
    def print_current_status(self):
        print("Cards at the end of this Round", self.state.player_cards_hidden)
        return self.state.player_scores

    # Declare winners of this round 



def kickoff():
    rounds = 3
    for i in range(rounds):
        print()
        print(f"\n--------------------------------- Round {i+1} Starts ---------------------------------")
        game_flow = GameFlow()
        # game_flow.kickoff()
        round_results = game_flow.kickoff()
        for i in list(final_records.keys()):
            final_records[i] += round_results[i]

    print('\n------------------------------ Final Results --------------------------------------')
    
    find_winner(final_records)
    print('Game Over')


def plot():
    poem_flow = GameFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
