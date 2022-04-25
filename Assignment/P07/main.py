import pygame
import sys
import random


#setting main window size
MAIN_WINDOW_SIZE = (400,400)
def GeneratePoint(max_x ,max_y):
    # random x and y point 
    XVal = random.randint(0, max_x)
    YVal = random.randint(0, max_y)
    return (XVal, YVal)
     
def PointQuery():
    
    pygame.init()
    # creating pygame window
    WindowScreen = pygame.display.set_mode(MAIN_WINDOW_SIZE)
    #title
    pygame.display.set_caption('Bounding box Query')

    Rect_XVal = 0 # x   
    Rect_YVal = 0   # y
    #rectangel height and width
    Rect_Width = 100   
    Rect_Height = 100  
    Rectangle = pygame.Rect(Rect_XVal, Rect_YVal, Rect_Width, Rect_Height)

    ListOfPoints = []
    NumPoints = 300
    for i in range(NumPoints):
        GeneratedPoint = GeneratePoint(MAIN_WINDOW_SIZE[0], MAIN_WINDOW_SIZE[1])
        # adding point
        ListOfPoints.append(GeneratedPoint)

    while True:
        #window background color
        WindowScreen.fill(pygame.Color('blue')) 
        pygame.draw.rect(WindowScreen, pygame.Color('black'), Rectangle, 2)
        
        for event in pygame.event.get():
            #exit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)  

        RadiusOfPoints = 7

        for point in ListOfPoints:
            if Rectangle.collidepoint(point):
                print(point)
                point_color = pygame.Color(random.randint(0,255), random.randint(0,255), random.randint(0,255))
                pygame.draw.circle(WindowScreen, point_color, point, RadiusOfPoints,0)

               
            else:
               
                pygame.draw.circle(WindowScreen, pygame.Color('gray'), point, RadiusOfPoints, 0)   
       
        Rectangle.move_ip(2,0)
        if Rectangle.right > MAIN_WINDOW_SIZE[0]:
            Rectangle.move_ip(-MAIN_WINDOW_SIZE[0],100)
        pygame.display.update()
        # setting 60 fps
        pygame.time.Clock().tick(60)
        if Rectangle.bottom > MAIN_WINDOW_SIZE[1]:
            Rectangle.move_ip(-MAIN_WINDOW_SIZE[0],-MAIN_WINDOW_SIZE[1])
        #update
        pygame.display.update()
        # # setting 60 fps(mainscreen)
        pygame.time.delay(60)
        
        pygame.display.flip()      
if __name__ == '__main__':
    PointQuery()
