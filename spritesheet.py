import pygame

class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

        # Gets the image of a frame from the sheet image
        # Sheet is image, frame_num is the frame number, width and height is the size of the single frame, scale is how big we want it, color is to make background transparent
    def get_image(self, frame_num, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame_num * width), 0, width,
                                   height))  # you can blit the whole sheet on this surface at the surface's 0, 0, but we are only taking a portion of the sheet
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)  # makes the surface transparent
        return image