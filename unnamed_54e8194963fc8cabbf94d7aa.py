  # Smart Contract Decentralized_Voting_System
  # Elections ordinales ou de conseils d'administration
  # Consultation par internet, 
  #  référendum en ligne et résolutions d'assemblée générale
  #                 Choisissez un vote transparent et fiable
  #                 Privilégiez l'accessibilité pour tous
  #                 Donnez du sens à l'expression collective
  #                 Favorisez une meilleure participation
  #                 Gagnez du temps pour vous consacrer à l'essentiel
  #  L'élection présidentielle/ législatives /sénatoriales/européennes .....
  #
  #

import smartpy as sp

@sp.module
def main():
    # Internal administration action type specification
    players_type: type = sp.map[
        sp.int, sp.record(name=sp.string, year=sp.string, votes=sp.nat)
    ]

    class dscentVote(sp.Contract):
        def __init__(self, players,votersAdd):
  
            self.data.players = sp.cast(players, players_type)
            self.data.votersAdd = votersAdd
            self.data.metadata="You are welcome this is the vote of Mm/M:" 


        @sp.entrypoint
        def increase_votes(self, params):

            assert not sp.sender == self.data.votersAdd, "YouAlreadyVoted"
            assert self.data.players.contains(params.playerId), "PlayerIDNotFound"
            
            self.data.players[params.playerId].votes += 1
            
            self.data.votersAdd = sp.sender
            self.data.metadata = "" 
            
        # defaut — will hold an empty string. In the next tutorial where we
        #        integrate our dApp with our smart contract, you may notice
        #        that having just one entrypoint makes Taquito not recognise your entrypoint. As such, we’ll have a dummy entrypoint and dummy variable that do nothing but keep things moving along smoothly.
        @sp.entrypoint
        def defaut(self):
            pass #
            


@sp.add_test()
def test():
    alice = sp.test_account("alice")
    bob = sp.test_account("bob")
    charlie = sp.test_account("charlie")
    adebola = sp.test_account("adebola")
    rashida = sp.test_account("rashida")
    daruis = sp.test_account("daruis")
    aldrin = sp.test_account("daldrin")
    member1 = sp.test_account("member1")
    member2 = sp.test_account("member2")
    member3 = sp.test_account("member3")

    scenario = sp.test_scenario("Basic scenario", main)
    scenario.h1("Basic scenario")
    scenario.h2("Origination")
    
    players = {
        1: sp.record(name="Choix 1 ", year="2024", votes=0),
        2: sp.record(name="Choix 2", year="2024", votes=0),
        3: sp.record(name="Choix 3", year="2024", votes=0),
        4: sp.record(name="Choix 4", year="2024", votes=0),
        5: sp.record(name="Choix 5", year="2024", votes=0),
    }

    contract = main.dscentVote(players, alice.address)
    scenario += contract

    scenario.h2("Scenario 1: Increase votes when playerId Exists")
        # Scenario 1: Increase votes when playerId Exists
    scenario.h3("votes 1 for the proposal")
    contract.increase_votes(playerId=2, _sender= rashida.address)
    scenario.verify(contract.data.players[2].votes == 1)
    scenario.h3("votes 2 for the proposal") 
    contract.increase_votes(playerId=2, _sender=daruis.address)
    scenario.verify(contract.data.players[2].votes == 2)
    scenario.h2("Scenario 2: Increase votes when playerId Exists")
    # Scenario 2: Increase votes when playerId Exists
    contract.increase_votes(playerId=2, _sender=charlie.address)
    scenario.verify(contract.data.players[2].votes == 3)
    scenario.h3("Scenario 2: Increase votes when playerId Exists") 
    scenario.h3("Scenario : Fail if User already voted") 
    # Scenario 3: Fail if User already voted
    contract.increase_votes(playerId=2, _sender = charlie.address, _valid=False, _exception= "YouAlreadyVoted")
    scenario.h3("Scenario : Fail if playerID does not exist") 
    # Scenario 4: Fail if playerID does not exist
    contract.increase_votes(playerId=6, _sender =alice.address, _valid=False, _exception="PlayerIDNotFound")

    #checking deadline

