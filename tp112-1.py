#Hana Frluckaj, hfrlucka
from pykinect2 import PyKinectRuntime, PyKinectV2
from pykinect2.PyKinectV2 import *

import ctypes
import _ctypes
import pygame
import sys
import math
import time

class GameRuntime(object): #repeats over and over while game runs
    def __init__(self):
        pygame.init()
        
        self.timeStart = 0
        self.timeAdded = 1000 #milliseconds
        self.screen_width = 1920 #recommended)
        self.screen_height = 1080
        self.timer_x = 0
        self.distance_y = self.screen_height - 100 #on top of one another
        self.calories_y = self.screen_height - 50
        self.cur_right_wrist_height = 0
        self.cur_left_wrist_height = 0
        self.cur_right_knee_height = 0
        self.cur_left_knee_height = 0
        self.prev_right_wrist_height = 0
        self.prev_left_wrist_height = 0
        self.prev_right_knee_height = 0
        self.prev_left_knee_height = 0
        self.calorieFire = 0
        self.runningDis = 0 
        self.jointDis = 0
        self._font = pygame.font.Font(None,36)

        #Kinect runtime object, allowing for color and body frames(skeletal)
        self._kinect = PyKinectRuntime.PyKinectRuntime(
          PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        
        #back buffer surface for getting Kinect color frames, 32b color, w & h
        self._frame_surface = pygame.Surface(
                (self._kinect.color_frame_desc.Width,
                self._kinect.color_frame_desc.Height), 0, 32)
        
        #Loop until the user clicks the close button 
        self._done = False
        
        #used to manage how fast the screen updates
        self._clock = pygame.time.Clock()
        
        #initialize screen
        self._screen = pygame.display.set_mode((960, 540), 
                                pygame.HWSURFACE|pygame.DOUBLEBUF, 32)
                                
        #number of people play(should only be 1 though)
        self._bodies = None
        
        #surface we will draw on , 32 bts for color
        self._frame_surface = pygame.Surface(
                (self._kinect.color_frame_desc.Width, 
                self._kinect.color_frame_desc.Height), 0, 32)
        self._done = False #game over

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock()

    def draw_timer(self): 
    #tuple with 3 digits for colors - red in this case
        pygame.draw.rect(self._frame_surface, (120, 0, 0), 
                        (self.timer_x, 0, 90, 50))
        time_display = (
            self._font.render("Time: "+str(self._clock.get_time()),1,(0,0,0)))
        #display mins and seconds
        '''pygame.draw.text(self._frame_surface, (45, 25), 
            text = "Time: " + str(self.timeMins) + ":" + str(self.timeSecs),
            font = "Arial 16")'''
            
    def draw_calories(self):
        pygame.draw.rect(self._frame_surface, (0, 200, 0), #green color
                        (0, self.calories_y, 90, self.screen_height))
        '''pygame.draw.text(self._frame_surface, (45, self.calories_y+25),
            text = "Calories: " + str(self.calorieFire), font = "Arial 16")'''
        calories_display = (
            self._font.rend("cal: "+str(self.calorieFire),1,(0,0,0)))
            
    def draw_distance(self):
        pygame.draw.rect(self._frame_surface, (0, 0, 200), #blue color
                        (0, self.distance_y, 90, self.calories_y))#on top of cal
        '''pygame.draw.text(self._frame_surface, (45, self.distance_y+25),
            text = "Distance: " + str(self.runningDis), font = "Arial 16")'''
        

    def run(self):
        while not self._done:
            #game code here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._done= True
                    
            #We have a color frame. Fill out back buffer surface w/ frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None
                
            #we've got a body!  now grab the skeleten outta the closet      
            if self._kinect.has_new_body_frame():
                self._bodies = self._kinect.get_last_body_frame()
                
                if self._bodies is not None:
                    for i in range(0, self._kinect.max_body_count):
                        body = self._bodies.bodies[i]
                        if body.is_tracked:
                            #check to see if you can find joint
                            if (
                            joints[PyKinectV2.JointType_WristLeft].TrackingState 
                            != PyKinectV2.TrackingState_NotTracked):
                                (self.cur_left_wrist_height =
                              joints[PyKinectV2.JointType_WristLeft].Position.y)
                            '''if (
                        joints[PyKinectV2.JointType_WristRight].TrackingState 
                            != PyKinectV2.TrackingState_NotTracked):
                                (self.cur_right_wrist_height =
                            joints[PyKinectV2.JointType_WristRight].Position.y)
                            if (
                            joints[PyKinectV2.JointType_KneeLeft].TrackingState
                            != PyKinectV2.TrackingState_NotTracked):
                                (self.cur_left_knee_height = 
                            joints[PyKinectV2.JointType_KneeLeft].Position.y)'''
                            if (
                        joints[PyKinectV2.JointType_KneeRight].TrackingState 
                            != PyKinectV2.TrackingState_NotTracked):
                                (self.cur_right_knee_height =
                            joints[PyKinectV2.JointType_KneeRight].Position.y)
                            
                            #calculate change in knees and wrists
                            #weigh wrist movement more than knee movement
                            self.jointDis=((self.prev_right_knee_height-
                                            self.cur_right_knee_height)*0.2 + 
                (self.prev_left_wrist_height-self.cur_left_wrist_height)*0.8)
                            if (math.isnan(self.jointDis) = True or 
                                self.jointDis < 0):
                                    self.jointDis = 0 #reset if past bounds
                             
                            #reset new prev and current after each movement
                            (self.prev_right_knee_height = 
                                            self.cur_right_knee_height)
                            (self.prev_left_wrist_height =
                                            self.cur_left_wrist_height)
                            #not in use atm
                            '''(self.prev_left_knee_height =
                                            self.cur_left_knee_height)
                            (self.prev_right_wrist_height =
                                            self.cur_right_wrist_height)'''
            #Game essentials
            
            #counting up
            self.timeStart += self.timeAdded
            self.timeMins = self.timeStart % 60000 #1 minute
            self.timeSecs = self.timeStart % 1000 #1 second
            if self.timeStart >= 360000: #if player goes over an hour
                self.timeStart = 0 #reset timer
                
            #distance traveled         += or =??, also estimated
            self.runningDis=(self.timeMins*0.0175*self.jointDis) #for 1 sec
            
            #calorie count (directly correlated with time and jointDis
            self.calorieFire = (self.runningDis//0.01)
                
            #render the camera's color image
            h_to_w = float((self._frame_surface.get_height())//
                            self._frame_surface.get_width())
            target_height = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transfrom.scale(self._frame_surface,
                                (self._screen.get_width(), target_height));
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()
                    
            self._clock.tick(60)
            
        self._kinect.close() #close our sensor and then quit   
        pygame.quit()
                                
game = GameRuntime()
game.run()

######################################################################
#possible mode implementation:
def __init__(self):
    self.mode = "startScreen"
    
    def startScreenRedrawAll(self._frame_surface, self):
        def draw_Basic_Box(self):
            pygame.draw.rect(self._frame_surface, (0, 200, 0), #green color
                            (self.screen_width//3-50, self.screen_height//2,
                            self.screen_width//3+50, self.screen_height//2))
            '''pygame.draw.text(self._frame_surface, 
                                (self.screen_width//3, self.screen_height//2),
                                    text = "Basic", font = "Arial 16")'''
                                    
        def draw_Yoga_Box(self):
            pygame.draw.rect(self._frame_surface, (0, 0, 200), #blue color
                            (self.screen_width//2-50, self.screen_height//2,
                            self.screen_width//2+50, self.screen_height//2))
            '''pygame.draw.text(self._frame_surface, 
                                (self.screen_width//2, self.screen_height//2),
                                    text = "Yoga", font = "Arial 16")'''
                                    
        def draw_Brutus_Box(self):
            pygame.draw.rect(self._frame_surface, (200, 0, 200), #red color
                            ((2*self.screen_width//3)-50, self.screen_height//2,
                            (2*self.screen_width//3)+50, self.screen_height//2))
            '''pygame.draw.text(self._frame_surface, 
                                (self.screen_width//2, self.screen_height//2),
                                    text = "Brutus", font = "Arial 16")'''
                                
    def run(self):
        while not self._done:
            #game code here
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._done= True
                    
            #We have a color frame. Fill out back buffer surface w/ frame's data 
            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None
                
            #we've got a body!  now grab the skeleten outta the closet      
            if self._kinect.has_new_body_frame():
                self._bodies = self._kinect.get_last_body_frame()
                
                if self._bodies is not None:
                    for i in range(0, self._kinect.max_body_count):
                        body = self._bodies.bodies[i]
                        if body.is_tracked:
                            #check to see if you can find joint
                            if (
                            joints[PyKinectV2.JointType_Head].TrackingState 
                            != PyKinectV2.TrackingState_NotTracked):
                                (self.cur_head_height =
                              joints[PyKinectV2.JointType_Head].Position.x)
                            $=#assign mode based on head Position
                            if (self.cur_head <= self.screen_width//3+50 and
                                self.cur_head >= self.screen_width//3-50):
                                    self.mode = "basicMode"
                            elif (self.cur_head <= self.screen_width//2+50 and
                                self.cur_head >= self.screen_width//2-50):
                                    self.mode = "yogaMode"
                            elif (self.cur_head <= (2*self.screen_width//3)+50
                                and self.cur_head>=(2*self.screen_width//3)+50):
                                    self.mode = "brutusMode"
                                    