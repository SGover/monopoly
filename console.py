import gameClasses
class console():
    
    def __init__(self):
        pass
        
    def display(self, string):
        print(string)
     
    def start(self):
        print("***************\nNew Game of Monopoly!\n***************")
     
    def get_player_name(self):
        return input("Enter the Player name :_ ");
    
    def show_winner(self, winner):
        print(winner,"is the winner!")
        
    def prompt_commands(self, list_cmds):
        print("Select a command:")
        return input(" {} : ".format(list_cmds))
    def printBoard(self,board):
        for block in board:
            bType=type(block)
            if bType=type(gameClasses.block):
                if bType=type(gameClasses.assetBlock):
                    print (block.asset.name+" in : "+block.asset.groupName)
                elif bType=type(gameClasses.cardBlock):
                    print ("Deck : "+block.deck.name
