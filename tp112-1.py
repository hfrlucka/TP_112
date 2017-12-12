from pykinect2 import PyKinectRuntime, PyKinectV2
from pykinect2.PyKinectV2 import *

import ctypes
import _ctypes
import pygame
import sys
import math

class GameRuntime(object): #repeats over and over while game runs
    def __init__(self):
        pygame.init()

#used example from Kinect Workshop as a template
        self.timeStart = 0
        self.timeAdded = 1000 #milliseconds
        self.screen_width = 1920
        self.screen_height = 1080
        self.white_box_x = 150
        self.white_box_y = 300
        self.tree = False
        self.triangle = False
        self.warrior = False
        self.downward_dog = False
        self._font = pygame.font.Font(None,36)
        self.cur_head_height = 0
        self.cur_head_x = 0
        self.cur_left_ankle_height = 0
        self.cur_left_ankle_x = 0
        self.cur_left_hand_height = 0
        self.cur_left_hand_x = 0
        self.cur_left_knee_height = 0
        self.cur_left_knee_x = 0
        self.cur_right_ankle_height = 0
        self.cur_right_ankle_x = 0
        self.cur_right_hand_height = 0
        self.cur_right_hand_x = 0
        self.cur_right_knee_height = 0
        self.cur_right_knee_x = 0
        self.cur_spine_base_x = 0

        self._clock = pygame.time.Clock() 
        #creating a new class/parameters and flag
        self._screen = pygame.display.set_mode((self.screen_width//2, self.screen_height//2), pygame.HWSURFACE|pygame.DOUBLEBUF, 32) 
        #color for people to see themselves, and body for skeletal tracking
        self._kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
        
        self._bodies = None 
        #surface we will draw on , 32 bts for color
        self._frame_surface = pygame.Surface((self._kinect.color_frame_desc.Width, self._kinect.color_frame_desc.Height), 0, 32)
        self._done = False #game over

    def draw_color_frame(self, frame, target_surface):
        target_surface.lock()
        address = self._kinect.surface_as_array(target_surface.get_buffer())
        ctypes.memmove(address, frame.ctypes.data, frame.size)
        del address
        target_surface.unlock(           )

    
    def draw_tree(self):
        #white box
        pygame.draw.rect(self._frame_surface, (255,255,255), (self.white_box_x, self.white_box_y, 220, 350))
        #name box
        pygame.draw.rect(self._frame_surface, (0, 190, 70), (self.white_box_x, self.white_box_y-70, 220, 70))
        #head and upper body
        pygame.draw.circle(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+100), 22)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+100), 
                         (self.white_box_x+110, self.white_box_y+200), 5)
        #legs, left first
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+200),
                         (self.white_box_x+100, self.white_box_y+310), 5)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+200),
                         (self.white_box_x+150, self.white_box_y+250), 5)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+150, self.white_box_y+250),
                         (self.white_box_x+105, self.white_box_y+260), 5)
        #finally, arms
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+160),
                         (self.white_box_x+70, self.white_box_y+100), 5)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+70, self.white_box_y+100),
                         (self.white_box_x+110, self.white_box_y+60), 5)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+160),
                         (self.white_box_x+150, self.white_box_y+100), 5)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+150, self.white_box_y+100),
                         (self.white_box_x+110, self.white_box_y+60), 5)

    def draw_warrior(self):
        #white box
        pygame.draw.rect(self._frame_surface, (255,255,255), (self.white_box_x, self.white_box_y, 220, 350))
        #name box
        pygame.draw.rect(self._frame_surface, (0, 190, 70), (self.white_box_x, self.white_box_y-70, 220, 70))
        #head and upper body
        pygame.draw.circle(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+100), 22)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+100), 
                         (self.white_box_x+110, self.white_box_y+200), 5)
        #arms
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+40, self.white_box_y+140),
                         (self.white_box_x+180, self.white_box_y+135), 5)
        #legs
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+200),
                         (self.white_box_x+150,self.white_box_y+203),5)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+150,self.white_box_y+203),
                         (self.white_box_x+153, self.white_box_y+248), 5)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+200),
                         (self.white_box_x+40, self.white_box_y+248), 5)

    def draw_triangle(self):
        #white box
        pygame.draw.rect(self._frame_surface, (255,255,255), (self.white_box_x, self.white_box_y, 290, 300))
        #name box
        pygame.draw.rect(self._frame_surface, (0, 190, 70), (self.white_box_x, self.white_box_y-70, 290, 70))
        #head and upper body
        pygame.draw.circle(self._frame_surface, (0,0,0), (self.white_box_x+80, self.white_box_y+150), 22)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+80, self.white_box_y+150), 
                         (self.white_box_x+180, self.white_box_y+170), 5)
        #arms
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+110, self.white_box_y+220), 
                         (self.white_box_x+120, self.white_box_y+100), 5)
        #legs
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+180, self.white_box_y+170),
                        (self.white_box_x+100, self.white_box_y+240), 5)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+180, self.white_box_y+170),
                        (self.white_box_x+220, self.white_box_y+240), 5)

    def draw_downward_dog(self):
        #white box
        pygame.draw.rect(self._frame_surface, (255,255,255), (self.white_box_x, self.white_box_y, 290, 300))
        #name box
        pygame.draw.rect(self._frame_surface, (0, 190, 70), (self.white_box_x, self.white_box_y-70, 290, 70))
        #head and upperbody
        pygame.draw.circle(self._frame_surface, (0,0,0), (self.white_box_x+220, self.white_box_y+210), 22)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+220, self.white_box_y+210),
                         (self.white_box_x+150, self.white_box_y+130), 5)
        #arms
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+190, self.white_box_y+180),
                         (self.white_box_x+240, self.white_box_y+250), 5)
        pygame.draw.line(self._frame_surface, (0,0,0), (self.white_box_x+190, self.white_box_y+180),
                         (self.white_box_x+240, self.white_box_y+270), 5)
        #legs
        pygame.draw.line(self._frame_surface, (0,0,0),(self.white_box_x+150, self.white_box_y+130),
                         (self.white_box_x+85, self.white_box_y+250), 5)
        pygame.draw.line(self._frame_surface, (0,0,0),(self.white_box_x+150, self.white_box_y+130),
                         (self.white_box_x+60, self.white_box_y+270), 5)
        
       

    def run(self):
        while not self._done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._done = True

#actually tracking hand movements
            if self._kinect.has_new_body_frame():
                self._bodies = self._kinect.get_last_body_frame() 
                if self._bodies is not None: 
                    for i in range(0, self._kinect.max_body_count): 
                        body = self._bodies.bodies[i]
                        if body.is_tracked: 
                            joints = body.joints 
                            if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                               self.cur_right_hand_height = joints[PyKinectV2.JointType_HandRight].Position.y
                            if joints[PyKinectV2.JointType_HandRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                               self.cur_right_hand_x = joints[PyKinectV2.JointType_HandRight].Position.x

                            if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                               self.cur_left_hand_height = joints[PyKinectV2.JointType_HandLeft].Position.y
                            if joints[PyKinectV2.JointType_HandLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                               self.cur_left_hand_x = joints[PyKinectV2.JointType_HandLeft].Position.x

                            if joints[PyKinectV2.JointType_Head].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_head_height = joints[PyKinectV2.JointType_Head].Position.y
                            if joints[PyKinectV2.JointType_Head].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_head_x = joints[PyKinectV2.JointType_Head].Position.x

                            if joints[PyKinectV2.JointType_AnkleLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_left_ankle_height = joints[PyKinectV2.JointType_AnkleLeft].Position.y
                            if joints[PyKinectV2.JointType_AnkleLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_left_ankle_x = joints[PyKinectV2.JointType_AnkleLeft].Position.x

                            if joints[PyKinectV2.JointType_AnkleRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_right_ankle_height = joints[PyKinectV2.JointType_AnkleRight].Position.y
                            if joints[PyKinectV2.JointType_AnkleRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_right_ankle_x = joints[PyKinectV2.JointType_AnkleRight].Position.x

                            if joints[PyKinectV2.JointType_KneeLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_left_knee_height = joints[PyKinectV2.JointType_KneeLeft].Position.y
                            if joints[PyKinectV2.JointType_KneeLeft].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_left_knee_x = joints[PyKinectV2.JointType_KneeLeft].Position.x

                            if joints[PyKinectV2.JointType_KneeRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_right_knee_height = joints[PyKinectV2.JointType_KneeRight].Position.y
                            if joints[PyKinectV2.JointType_KneeRight].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_right_knee_x = joints[PyKinectV2.JointType_KneeRight].Position.x

                            if joints[PyKinectV2.JointType_SpineBase].TrackingState != PyKinectV2.TrackingState_NotTracked:
                                self.cur_spine_base_x = joints[PyKinectV2.JointType_SpineBase].Position.x

            if self._kinect.has_new_color_frame():
                frame = self._kinect.get_last_color_frame()
                self.draw_color_frame(frame, self._frame_surface)
                frame = None

            # time for game logic!!
            if self.tree == True:
                if self.cur_right_hand_height > self.cur_head_height:
                    if (self.cur_right_ankle_height > self.cur_left_knee_height) or (self.cur_left_ankle_height > self.cur_right_knee_height):
                        return True #insert picture with good form signal
                return False #bad form pic and pause timer

            if self.warrior == True:
                #test that they're a reasonable distance form one another
                if (self.cur_left_hand_height < self.cur_right_hand_height +70) and self.cur_right_hand_height < self.cur_left_hand_height +70:
                    if self.cur_right_knee_x >= self.cur_right_ankle_x - 80:
                        return True
                return False

            if self.triangle == True:
                if self.cur_head_x <= self.cur_left_ankle_x +100:
                    if self.cur_right_hand_height > self.cur_head_height:
                        if self.cur_left_hand_x <= self.cur_left_ankle_x + 100:
                            return True
                return False

            if self.downward_dog == True:
                if self.cur_left_hand_height <= self.cur_left_ankle_height + 20:
                    if self.cur_head_height <= self.cur_left_knee_height +50:
                        if self.cur_spine_base_x > self.cur_left_ankle_x:
                            return True
                return False

            
           
            
            #now we draw  
            self.draw_tree()
            #self.draw_warrior()
            #self.draw_triangle()
            #self.draw_downward_dog()
            

            h_to_w = float(self._frame_surface.get_height()/self._frame_surface.get_width())
            target = int(h_to_w * self._screen.get_width())
            surface_to_draw = pygame.transform.scale(self._frame_surface, (self._screen.get_width(), target))
            self._screen.blit(surface_to_draw, (0,0))
            surface_to_draw = None
            pygame.display.update()   


            self._clock.tick(60) #human register

        self._kinect.close()
        pygame.quit()

game = GameRuntime()
game.run();
