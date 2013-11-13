import gameClasses
class console():
    
    def __init__(self):
        pass
        
    def display(self, string):
        print(string)
     
    def start(self):
        print("******************************\n    New Game of Monopoly!\n******************************")
     
    def get_player_name(self):
        name = input("Enter the Player name :_ ");
        while name=="":
            name = input("Empty input string, Please Enter the Player name :_ ");
        return name 
    
    def show_winner(self, winner):
        print(winner,"is the winner!")
        
    def prompt_commands(self, list_cmds):
        print("\nSelect a command:")
        return input(" {} : ".format(list_cmds))
    
    def prompt_commands_index(self,list_cmds):
        print ("use the number to select an option from the following options:")
        str1=''
        for cmd in list_cmds:
            str1+=" "+str(list_cmds.index(cmd)+1)+". "+str(cmd)
        index = -1
        while index<0 or index>=len(list_cmds):
            index= int(input(str1+'\n'))-1
        return list_cmds[index]
            
        
    def printBoard(self,board):
        for block in board.blocks:
            bType=type(block)
            if bType==type(gameClasses.block):
                if bType==type(gameClasses.assetBlock):
                    print (block.asset.name+" in : "+block.asset.groupName)
                elif bType==type(gameClasses.cardBlock):
                    print ("Deck : "+block.deck.name)
    
    def chooseFromOptions(self,actions):    
        """take a name:value pair as actions"""
        print("\nSelect a command :")
        i=0
        for key in actions.keys():
            i+=1
            print (str(i)+". "+key)
        cmd=input(" select :")
        while not (cmd in actions):
            print ("wrong command try again")
            cmd=input(" select :")
        print(" ")
        actions[cmd]()
        
