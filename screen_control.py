# coding: utf-8

import screeninfo
import cv2
import numpy as np
import uuid

class Screen:

    def __init__(self, monitor_id, gamma=2.2):
        """[summary]
        
        Arguments:
            monitor_id {int} -- monitor id.
        
        Keyword Arguments:
            gamma {float} -- gamma value (default: {2.2})
        """

        self.monitor = screeninfo.get_monitors()[monitor_id]
        self.w = self.monitor.width
        self.h = self.monitor.height
        self.image = np.zeros((self.h, self.w), dtype=np.uint8)
        self.gamma = gamma
        self.vmax = 255
    
    def show(self, img, wait_time=10):
        """show image to the screen.
        img should be scaled to 0 to 1.
        
        Args:
            img (numpy array): image to be displayed
        
        """
        corrected = self.correct_gamma(img)

        window_name = uuid.uuid4().hex.upper() # give unique name

        cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.moveWindow(window_name, self.monitor.x - 1, self.monitor.y - 1)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                            cv2.WINDOW_FULLSCREEN)
        cv2.imshow(window_name, corrected)
        
        # any number except for 0 works.
        # if 0 is set, it cannot be back to the main program.
        # image can be over-written when this function is called. 
        # the number wait time does not matter.
        cv2.waitKey(wait_time)
        cv2.destroyWindow(window_name)
    
    def correct_gamma(self, img):
        """correct gamma. 
        http://w3.kcua.ac.jp/~fujiwara/infosci/gamma.html 
        
        Arguments:
            img {np.array} -- input image to be corrected
        
        Returns:
            [np.array(uint8)] -- corrected image
        """
        y = img ** (1 / self.gamma)
        corrected = np.round(y * self.vmax).astype(np.uint8)

        return corrected 

    def show_black(self):
        self.show(np.zeros((self.h, self.w), dtype=np.uint8))
    
    def show_white(self):
        self.show(np.ones((self.h, self.w), dtype=np.uint8)*255)
    
    def show_gray(self, v):
        self.show(np.ones((self.h, self.w), dtype=np.uint8)*v)
    
    def destroy_windows(self):
        cv2.destroyAllWindows()
