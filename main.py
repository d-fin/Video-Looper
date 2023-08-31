import pygame 
import os 
import numpy 
import cv2 


def main():

    pygame.init()
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h
    window = pygame.display.set_mode((width, height))

    font = pygame.font.Font(None, 74)
    text = font.render('Insert a USB Drive!', True, (255, 255, 255))


    usbPath = ["E"]
    currentImage = 0
    startTime = pygame.time.get_ticks()
    images = []

    while True:
        driveExists = False

        # Check for USB drives
        for driveLetter in usbPath:
            if os.path.exists(driveLetter + ":\\"):
                driveExists = True
                files = findFiles(driveLetter + ":\\")
                if files:
                    images = [pygame.image.load(path) for path in files]
                else:
                    print(f"No media files were found in {driveLetter}")
                break

        if not driveExists:
            # Display static color with text
            window.fill((0, 0, 255))
            window.blit(text, (250, 250))
            pygame.display.flip()
            print(f"Error finding USB drive - {usbPath}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # Display image logic here
        if driveExists and images:
            if (pygame.time.get_ticks() - startTime) > 10000:
                currentImage += 1
                if currentImage >= len(images):
                    currentImage = 0

                startTime = pygame.time.get_ticks()

            window.fill((0, 0, 0))
            scaledImage = pygame.transform.scale(images[currentImage], (width, height))
            window.blit(scaledImage, (0, 0))
            pygame.display.flip()

        pygame.time.delay(100)

def findFiles(directory):
    mediaFiles = []
    try:
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.jpg') or file.endswith('.png') or file.endswith('.jpeg') or file.endswith('gif') or file.endswith('.png') or file.endswith('.mov') or file.endswith('.mp4'):
                    mediaFiles.append(os.path.join(root, file))
    except:
        return False
    else:
        return mediaFiles

if __name__ == '__main__':
    main()