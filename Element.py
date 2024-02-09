'''
    Creates the Element and Button classes, which defines each element of the board
    An element is any image drawn on the screen
    A button is an element that can be clicked
'''

import pygame

'''
Element: defines each Element of the game
@attributtes:
    image: image object of the Element (see pygame)
    x, y: starting coordinates of the Element on the screen
    size_x, size_y: dimensions of the Element
'''
class Element:
    # init takes the path to the image of the Element, as well as its starting coordinates and dimensions
    def __init__(self, image_path, x, y, size_x, size_y):
        self.image = pygame.transform.scale(pygame.image.load(image_path), (size_x, size_y))
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        return None
    
    '''
    draw: draws the Element on the screen
    @parameters:
        self
        screen: the screen object to drawn on
    @return: None
    '''
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        return None
    


'''
Button: defines each Button of the game
@attributtes: same as Element
'''
class Button(Element):
    '''
    clicked: checks if Button was clicked
    @parameters:
        self
        x, y: coordinates of the click
    @return: True if clicked; False otherwise
    '''
    def clicked(self, x, y):
        return (self.x <= x <= self.x + self.size_x) and (self.y <= y <= self.y + self.size_y)
    
    '''
    place_click: returns in what part of the button it was clicked (ex: (0.2, 0.3) means at 20% distance from self.x in x-axis and 30% distance from self.y in y-axis)
    @parameters:
        self
        x, y: coordinates of the click
    @return: (-1, -1) if not clicked; otherwise, distance from (self.x, self.y) proportional to size 
    '''
    def place_click(self, x, y):
        if not self.clicked(x,y):
            return (-1, -1)
        else:
            return ( (x - self.x) / (self.size_x), (y - self.y) / (self.size_y) )
