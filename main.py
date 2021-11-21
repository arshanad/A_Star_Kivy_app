import random
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from database import DataBase
from a_StarGraph import AStarGraph
from kivy.lang import Builder


class IntroScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.my_root_widget = BoxLayout(spacing=10, padding=100, orientation='vertical')
        self.play_button = Button(text="Play")
        self.play_button.bind(on_press=self.start_game)
        self.length_label = Label(text="Length")
        self.width_label = Label(text="Width")
        self.length_input = TextInput(text='', multiline=False)
        self.width_input = TextInput(text='', multiline=False)
        self.begin_label = Label(text="Beginning position")
        self.end_label = Label(text="End position")
        self.begin_input = TextInput(text='', multiline=False)
        self.end_input = TextInput(text='', multiline=False)
        self.my_root_widget.add_widget(self.length_label)
        self.my_root_widget.add_widget(self.length_input)
        self.my_root_widget.add_widget(self.width_label)
        self.my_root_widget.add_widget(self.width_input)
        self.my_root_widget.add_widget(self.begin_label)
        self.my_root_widget.add_widget(self.begin_input)
        self.my_root_widget.add_widget(self.end_label)
        self.my_root_widget.add_widget(self.end_input)
        self.my_root_widget.add_widget(self.play_button)
        self.add_widget(self.my_root_widget)

    def start_game(self, _):
        length = self.length_input.text
        width = self.width_input.text
        begin = self.begin_input.text
        end = self.end_input.text
        # validating user input
        if not length.isnumeric() or not width.isnumeric() or not begin.isnumeric() or not end.isnumeric():
            invalidForm()
            return
        max_cell=int(length)*int(width)
        if int(begin)<0 or int(end)<0 or int(begin)>=max_cell or int(end)>=max_cell or int(length) <= 0 or int(width) <= 0:
            invalidForm()
            return
        length = int(length)
        width = int(width)
        begin=int(begin)
        end=int(end)
        # init game screen and set as current
        game_screen_name = 'game'
        game_screen = sm.get_screen(game_screen_name)
        game_screen.init(length, width,begin,end)
        sm.current = game_screen_name


class GameScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.my_root_widget = None
        self.tile_list = None
        self.no_rows = None
        self.no_cols = None
        self.beg=None
        self.finish=None
       

    def init(self, length, width,beg,finish):
        self.no_rows = length
        self.no_cols = width
        self.beg=beg
        self.finish=finish

        # create root layout
        self.my_root_widget = BoxLayout(spacing=10, padding=100, orientation='vertical')
        self.table = GridLayout(cols=self.no_cols,rows=self.no_rows)
        self.my_root_widget.add_widget(self.table)
        self.play_button = Button(text="Play",size_hint=(.2,.2),pos_hint={'x':0.4,'y':0})
        self.play_button.bind(on_press=self.start_game)
        # create list of tiles
        self.tile_list = [Tile(self,i) for i in range(self.no_cols * self.no_rows)]
        # populate the layout
        for tile in self.tile_list:
            self.table.add_widget(tile)
        self.my_root_widget.add_widget(self.play_button)
        self.add_widget(self.my_root_widget)
        self.tile_list[beg].disabled=True
        self.tile_list[beg].background_disabled_normal='player.png'
        self.tile_list[finish].disabled=True
        self.tile_list[finish].background_disabled_normal='finish_line.png'
        
    def on_press_callback(self, index):
        flag=self.tile_list[index].is_obstacle()
        if flag:
            self.tile_list[index].set_obstacles(False)
            self.tile_list[index].background_normal= 'atlas://data/images/defaulttheme/button_disabled'
        else:
            self.tile_list[index].set_obstacles(True)
            self.tile_list[index].background_normal='barrier.png'
                   

    def start_game(self, _):
            self.my_root_widget.remove_widget(self.play_button)
            barriers = []
            no_rows=self.no_rows
            no_cols=self.no_cols
            start=(int(self.beg/no_cols),self.beg%no_cols)
            end=(int(self.finish/no_cols),self.finish%no_cols)
            for i in range (no_rows):
                    for j in range (no_cols):
                            index=i*no_cols+j
                            self.tile_list[index].disabled=True
                            
                            if self.tile_list[index].is_obstacle():
                                    barriers.append((i,j))
                                    self.tile_list[index].background_disabled_normal='barrier.png'
            graph = AStarGraph(barriers,no_rows,no_cols)
            G = {} #Actual movement cost to each position from the start position
            F = {} #Estimated movement cost of start to end going via this position
 
	    #Initialize starting values
            G[start] = 0
            F[start] = graph.heuristic(start, end)

            closedVertices = set()
            openVertices = set([start])
            cameFrom = {}
            try:
             while len(openVertices) > 0:
		#Get the vertex in the open list with the lowest F score
                current = None
                currentFscore = None
                for pos in openVertices:
                        if current is None or F[pos] < currentFscore:
                                currentFscore = F[pos]
                                current = pos
             
		#Check if we have reached the goal
                if current == end:
                       #Retrace our route backward
                        path = [current]
                        while current in cameFrom:
                                current = cameFrom[current]
                                path.append(current)
                        path.reverse()
                        print(path)
                        path.pop()
                        print(path)
                        for node in path:
                                self.tile_list[node[0]*no_cols+node[1]].background_disabled_normal='player.png'
                        self.tile_list[self.finish].background_disabled_normal='finish_player.png'
                        self.play_again_button = Button(text="Play Again",size_hint=(.2,.2),pos_hint={'x':0.4,'y':0})
                        self.play_again_button.bind(on_press=self.again_game)
                        self.my_root_widget.add_widget(self.play_again_button)
                        self.logout_button = Button(text="Logout",size_hint=(.2,.2),pos_hint={'x':0.4,'y':0})
                        self.logout_button.bind(on_press=self.logout)
                        self.my_root_widget.add_widget(self.logout_button)
                        return
	
		#Mark the current vertex as closed
                openVertices.remove(current)
                closedVertices.add(current)
 
		#Update scores for vertices near the current position
                for neighbour in graph.get_vertex_neighbours(current):
                        if neighbour in closedVertices:
                                continue #We have already processed this node exhaustively
                        candidateG = G[current] + graph.move_cost(current, neighbour)
                        if neighbour not in openVertices:
                                openVertices.add(neighbour) #Discovered a new vertex
                        elif candidateG >= G[neighbour]:
                                continue #This G score is worse than previously found
 
			#Adopt this G score
                        cameFrom[neighbour] = current
                        G[neighbour] = candidateG
                        H = graph.heuristic(neighbour, end)
                        F[neighbour] = G[neighbour] + H

            except RuntimeError:
                 pop = Popup(title='Error',
                  content=Label(text='A star failed to find solution'),
                  size_hint=(None, None), size=(400, 400))
                 pop.open()
                

    def again_game(self,_):
                self.remove_widget(self.my_root_widget)
                sm.current = 'intro'

    def logout(self,_):
        sm.current = "login"
	    
        

class Tile(Button):
    def __init__(self, game, index, is_obstacle_flag=False,**kwargs):
        super().__init__(**kwargs)
        self.game = game
        self.tile_index = index
        self.is_obstacle_flag = is_obstacle_flag
    def set_obstacles(self,flag):
        self.is_obstacle_flag = flag

    def is_obstacle(self):
        return self.is_obstacle_flag

    def on_press(self):
        self.game.on_press_callback(self.tile_index)
        

    def get_tile_index(self):
        return self.tile_index

class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if self.namee.text != "" and self.email.text != "" and self.email.text.count("@") == 1 and self.email.text.count(".") > 0:
            if self.password != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)

                self.reset()

                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            self.reset()
            sm.current = "intro"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""



class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("my.kv")

sm = WindowManager()
db = DataBase("users.txt")

screens = [LoginWindow(name='login'), CreateAccountWindow(name='create'),IntroScreen(name='intro'),GameScreen(name='game')]
for screen in screens:
    sm.add_widget(screen)

sm.current = 'login'


class MyApp(App):
    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()
