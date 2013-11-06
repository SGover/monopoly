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
        