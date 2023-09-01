import time
import pygame 
import os 
import numpy as np
import cv2 

def main():
    pygame.init()
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    window = pygame.display.set_mode((width, height)) #, pygame.FULLSCREEN)
    
    font = pygame.font.Font(None, 74)
    text = font.render('Insert a USB Drive!', True, (255, 255, 255))
    
    currentImage, currentVideo = 0, 0
              
    # Main loop
    while True:
        driveExists, imageFiles, videoFiles = getUSB()
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
        if not driveExists:
            # Display static color with text
            window.fill((0, 0, 255))
            window.blit(text, (250, 250))
            pygame.display.flip()
        
        if imageFiles and driveExists:
            images = [pygame.image.load(path) for path in imageFiles]            
            displayImages(images, window, width, height, currentImage)
            currentImage += 1
            if currentImage >= len(imageFiles):
                currentImage = 0
                
           
        if videoFiles and driveExists:
            window.fill((0, 0, 0))
            pygame.display.flip()
            displayVideos(videoFiles, window, width, height, currentVideo)

        pygame.time.delay(10)

def getUSB():
    imageFiles, videoFiles = [], []
    volumes = os.listdir('/Volumes')
    usbDriveName = "SANDISK"
    driveExists = False 

    # below is for windows 
    '''
    usbPath = ["D", "E", "F"]
    for driveLetter in usbPath:
        if os.path.exists(driveLetter + ":\\"):
            driveExists = True
            imageFiles, videoFiles = findFiles(driveLetter + ":\\")
            if imageFiles:
                images = [pygame.image.load(path) for path in imageFiles]
            elif videoFiles:
                videos = [cv2.VideoCapture(video) for video in videoFiles]
            else:
                print(f"No media files were found in {driveLetter}")
            break '''
    
    # below is for ubuntu linux
    '''
    username = "" # get the ubuntu user and keep volumes (like Mac) 
    if usbDriveName in volumes:
        username = os.getlogin()  # Get the username
        usbPath = f'/media/{username}/{usbDriveName}'
        driveExists = True
        imageFiles, videoFiles = findFiles(usbPath)
        
        if not imageFiles and not videoFiles:
            print(f'No files found on USB - {usbPath}')
    else:
        print('Cannot find USB drive :(')'''
        
        
    # below is for mac         
    if usbDriveName in volumes: 
        usbPath = f'/Volumes/{usbDriveName}'
        driveExists = True 
        imageFiles, videoFiles = findFiles(usbPath)
        if not imageFiles and not videoFiles:
            print(f'No files found on USB - {usbPath}')
    else:
        print(f'cannot find USB drive :(')
    
    return driveExists, imageFiles, videoFiles
    
def displayImages(imageFiles, window, width, height, currentImage):        
        if currentImage >= len(imageFiles):
            currentImage = 0
            return  

        window.fill((0, 0, 0))
        scaledImage = pygame.transform.scale(imageFiles[currentImage], (width, height))
        window.blit(scaledImage, (0, 0))
        pygame.display.flip()
        
        time.sleep(10)

def displayVideos(videoFiles, window, width, height, currentVideo):
    clock = pygame.time.Clock()
    cap = cv2.VideoCapture(videoFiles[currentVideo])

    while True:
        ret, frame = cap.read()
        if not ret:
            cap.release()
            currentVideo += 1
            
            if currentVideo >= len(videoFiles):
                break
             
            cap = cv2.VideoCapture(videoFiles[currentVideo])
        elif ret:  
            frame = cv2.resize(frame, (int(width / 1.2), int(height / 1)))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.transpose(frame)
            
            frame = pygame.surfarray.make_surface(frame)
            window.blit(frame, (0, 0))
            pygame.display.update()
            clock.tick(30)
            
    cap.release()

def findFiles(directory):
    photoFiles = []
    videoFiles = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.jpg', '.png', '.jpeg')):
                photoFiles.append(os.path.join(root, file))
            elif file.endswith(('.gif', '.mov', '.mp4')):
                videoFiles.append(os.path.join(root, file))

    return photoFiles, videoFiles

if __name__ == '__main__':
    main()
