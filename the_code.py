from math import sqrt
import pygame
pygame.init()
#COMMANDS:
#'S': If you press 's' while your cursor is over a square(node),
#that square becomes the starting node.
#'G': It works the same way as 's', but it sets the goal node instead.
#'P' = If you already set the starting node and the goal, it starts the algorithm.
#'R' = Resets the path.
#'C' = Clears the obstacles
#Mouse's left button: Creates obstacles.
#Mouse's right button: Remove obstacles.
class node():
    def __init__(self, x, y):
        self.size = 20
        self.color = 'white'
        self.colors = {'white': (255, 255, 255),
                       'black': (0, 0, 0),
                       'blue': (128, 206, 225),
                       'dark blue': (0, 0, 128),
                       'orange': (255, 165, 0),
                       'green': (0, 128, 0),
                       'yellow': (255,255,0)}
        self.surface = pygame.Surface((20, 20))
        self.spc_btwn = 500 // self.size
        self.position = self.surface.get_rect(topleft=(x, y))
        self.predecessor = None
        self.found = False
        self.is_running = False
        self.is_mrbd = False
        self.is_mlbd = False
        self.s_point = None
        self.g_point = None
        self.current = None
        self.node_list = []
        self.open_set = []
        self.closed_set = []
        self.predecessor_list = []
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = self.g_cost + self.h_cost
        self.counter = len(self.predecessor_list)

    def nodes_creation(self):
        #Creates the grid of nodes and puts them inside
        #a list.
        x = 0
        y = 0
        for i in range(self.size):
            for l in range(self.size):
                self.node_list.append(node(x, y))
                x += self.spc_btwn
            x = 0
            y += self.spc_btwn

    def mouse_clicks_checker(self):
        #Checks whether the mouse's left button is being clicked or
        #the right.
        t = pygame.mouse.get_pressed()
        if t[0] == 1:
            self.is_mlbd = True
        elif t[0] == 0:
            self.is_mlbd = False
        if t[2] == 1:
            self.is_mrbd = True
        elif t[2] == 0:
            self.is_mrbd = False

    def blit_nodes(self, screen):
        #Puts all the nodes on the screen
        for i in self.node_list:
            screen.blit(i.surface, i.position)

    def create_obstacles(self):
        #If mouse's left button is down, change the color of the
        #node that it's clicking on to black, turning it into a wall.
        if self.is_mlbd:
            for i in self.node_list:
                if i.position.collidepoint(pygame.mouse.get_pos()):
                    if i.color == 'white':
                        i.color = 'black'
        #And if mouse's right button is down, change the color of the
        #node that it's clicking on to white, turning it into a normal node.
        elif self.is_mrbd:
            for i in self.node_list:
                if i.position.collidepoint(pygame.mouse.get_pos()):
                    if i.color == 'black':
                        i.color = 'white'

    def calculate_costs(self, i):
            #h_cost = Distance from the given node(i) to the goal
            #g_cost = Distance from the given node(i) to the initial
            #node through the current node.
            #f_Cost = h_cost + g_cost
            i.h_cost = abs(i.position.x - self.g_point.position.x) +\
                       abs(i.position.y -self.g_point.position.y)
            i.g_cost = self.current.g_cost + sqrt((self.current.position.x - i.position.x) ** 2 +
                                                  (self.current.position.y - i.position.y) ** 2)
            i.f_cost = i.h_cost + i.g_cost

    def astar_algorithm(self):
        if not self.found:
            if self.g_point != None and self.s_point != None:
                if self.open_set:
                    # sorts the list to see which neighbour has the cheapest cost
                    self.open_set.sort(key=lambda x: x.f_cost, reverse=False)
                    # moves the cheapest node from the open set to the closed set
                    self.closed_set.append(self.open_set.pop(0))
                    # set the current node to the cheapest one
                    self.current = self.closed_set[len(self.closed_set) - 1]
                    # if our current node is the goal node, then set 'found' to true.
                    if self.current == self.g_point:
                        self.found = True
                    for i in self.node_list:
                        # the if statement below gets all the nodes that weren't
                        # visited and that aren't walls.
                        if i not in self.closed_set \
                            and i not in self.open_set \
                            and i.color != 'black':
                                x = i.position.x
                                y = i.position.y
                            #the if statement below gets all the closest nodes
                            #from the current node and puts them in the open set
                            #And also set their predecessor to the current node
                                if self.current.position.x - x <= self.spc_btwn\
                                   and self.current.position.x - x >= -self.spc_btwn\
                                   and self.current.position.y - y <= self.spc_btwn\
                                   and self.current.position.y - y >= -self.spc_btwn\
                                   and i != self.current:
                                        i.predecessor = self.current
                                        self.calculate_costs(i)
                                        self.open_set.append(i)

    def colorize_algorithm(self):
        #This function sets the color property of the nodes and
        #Changes they accordingly to the type of node
        #(If it has been visited and etc.)
        #So it basically gives color to the algorithm
        for i in self.open_set:
            if i.color != 'green' and i.color != 'orange' and i.color != 'yellow':
                i.color = 'blue'
        for k in self.closed_set:
            if k.color != 'yellow':
                k.color = 'dark blue'
        self.s_point.color = 'green'
        self.g_point.color = 'orange'
        if self.predecessor_list and self.counter > -1:
            if self.predecessor_list[self.counter] != self.s_point:
                self.predecessor_list[self.counter].color = 'yellow'
            self.counter -=1

    def get_the_shortest_path(self):
        #If the goal was found, this function gets the shortest path
        #it has a pretty intuitive name lol.
        if self.found and len(self.predecessor_list) == 0.:
            if self.current == self.g_point:
                while self.current.predecessor != None:
                    self.predecessor_list.append(self.current.predecessor)
                    self.current = self.current.predecessor
                self.counter = len(self.predecessor_list) - 1

    def buttons_click_checker(self, event):
        #This function handles the keyboard commands, like setting the goal node,
        #The start node, and it also resets the path when you press 'r'.
        if event.type == pygame.KEYDOWN:
            key = pygame.key.get_pressed()
            if key[pygame.K_s]:
                for i in self.node_list:
                    if i.position.collidepoint(pygame.mouse.get_pos()):
                        if i.color != 'orange':
                            for g in self.node_list:
                                if g.color == 'green':
                                    g.color = 'white'
                            self.open_set.clear()
                            i.color = 'green'
                            self.s_point = i
                            if self.s_point not in self.open_set:
                                self.open_set.append(self.s_point)

            elif key[pygame.K_g]:
                for i in self.node_list:
                    if i.position.collidepoint(pygame.mouse.get_pos()):
                        if i.color != 'green':
                            for g in self.node_list:
                                if g.color == 'orange':
                                    g.color = 'white'
                            i.color = 'orange'
                            self.g_point = i
            elif key[pygame.K_p]:
                self.is_running = True
            elif key[pygame.K_c]:
                for i in self.node_list:
                    if i.color == 'black':
                        i.color = 'white'
            elif key[pygame.K_r]:
                self.found = False
                self.is_running = False
                self.current = None
                self.counter = 0
                self.predecessor_list.clear()
                self.closed_set.clear()
                self.open_set.clear()
                self.open_set.append(self.s_point)
                for i in self.node_list:
                    if i.color == 'blue' or i.color == 'dark blue' or i.color == 'yellow':
                        i.color = 'white'
                # self.s_point = None
                # self.g_point = None

    def update_colors(self):
        #This function finally get's the color property of the nodes
        #and updates them to it's color.
        for i in self.node_list:
            i.surface.fill(i.colors[i.color])


class game():
    def __init__(self):
        self.fps = 30
        self.s_width = 500
        self.screen = pygame.display.set_mode((self.s_width, self.s_width))
        pygame.display.set_caption('A* PathFinder')
        self.clock = pygame.time.Clock()
        self.n = node(700, 700)

    def main_loop(self):
        # And here, everything is finally put together.
        self.n.nodes_creation()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit(0)
                self.n.buttons_click_checker(event)
            self.clock.tick(self.fps)
            self.screen.fill(0)
            self.n.mouse_clicks_checker()
            self.n.create_obstacles()
            if self.n.is_running:
                self.n.astar_algorithm()
                self.n.get_the_shortest_path()
                self.n.colorize_algorithm()
            self.n.update_colors()
            self.n.blit_nodes(self.screen)
            pygame.display.update()

game().main_loop()
