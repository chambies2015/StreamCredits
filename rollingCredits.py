import Credentials
import pygame
import sys
from datetime import datetime

def read_credits(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def rolling_credits(file_path, subList, followerList):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Rolling Credits")
    clock = pygame.time.Clock()

    # Define fonts
    big_font = pygame.font.Font(None, 72)
    medium_font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)

    # Define colors (RGB)
    header_color = (255, 255, 0)  # Yellow
    subheader_color = (0, 255, 0)  # Green
    text_color = (255, 255, 255)  # White

    # Get current date
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Read credits and insert dynamic header
    credits = read_credits(file_path)
    credits.insert(0, f"#HEADER# {Credentials.channelName}\n")
    credits.insert(1, f"#HEADER# {current_date} Stream Credits\n")
    credits.insert(2, f"##SUBHEADER## Producer\n")
    credits.insert(3, f'{Credentials.channelName}\n')
    credits.insert(4, f"##SUBHEADER## Subscribers\n")

    subCount = 5
    for sub in subList:
        credits.insert(subCount, f"{sub}\n")
        subCount += 1

    credits.insert(subCount, f"##SUBHEADER## Followers\n")
    followCount = subCount + 1
    for follower in followerList:
        credits.insert(followCount, f"{follower}\n")
        followCount += 1
    credits.insert(followCount, "\n")
    credits.insert(followCount+1, f"#HEADER# Thanks for watching!")

    # Load scrolling image
    try:
        scrolling_image = pygame.image.load(Credentials.imagePath)
    except pygame.error as e:
        print(f"Failed to load scrolling image: {e}")
        pygame.quit()
        sys.exit()

    scrolling_image_rect = scrolling_image.get_rect(center=(screen.get_width() // 2, screen.get_height()))  # Start below the screen

    # Load static image
    try:
        static_image = pygame.image.load(Credentials.staticImagePath)
    except pygame.error as e:
        print(f"Failed to load static image: {e}")
        pygame.quit()
        sys.exit()

    static_image_rect = static_image.get_rect(bottomright=(screen.get_width(), screen.get_height()))  # Bottom right corner

    text_y = screen.get_height()

    # Calculate the total height of all credits
    total_height = 0
    for line in credits:
        if line.startswith('#HEADER#'):
            text = big_font.render(line.strip('#HEADER#').strip(), True, header_color)
        elif line.startswith('##SUBHEADER##'):
            text = medium_font.render(line.strip('##SUBHEADER##').strip(), True, subheader_color)
        else:
            text = small_font.render(line.strip(), True, text_color)

        total_height += text.get_rect().height + 10

    # Adjust scrolling image position to start after the credits
    image_start_y = text_y + total_height
    scrolling_image_rect.y = image_start_y  # Place the scrolling image right after the credits

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen with black color (you can change this to any color)
        screen.fill((0, 0, 0))

        y_offset = text_y
        for line in credits:
            if line.startswith('#HEADER#'):
                text = big_font.render(line.strip('#HEADER#').strip(), True, header_color)
            elif line.startswith('##SUBHEADER##'):
                text = medium_font.render(line.strip('##SUBHEADER##').strip(), True, subheader_color)
            else:
                text = small_font.render(line.strip(), True, text_color)

            text_rect = text.get_rect(center=(screen.get_width() // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += text_rect.height + 10

        # Update scrolling image position
        scrolling_image_rect.y -= 1  # Scroll the image up
        if scrolling_image_rect.y + scrolling_image.get_height() < 0:  # Stop scrolling when the image is fully off the screen
            break

        # Blit the scrolling image after text
        screen.blit(scrolling_image, scrolling_image_rect)

        # Blit the static image
        screen.blit(static_image, static_image_rect)

        text_y -= 1

        # Stop scrolling once the credits and image have moved off the screen
        if y_offset < 0 and text_y + total_height < 0:
            break

        pygame.display.flip()
        clock.tick(60)

    print('done')

if __name__ == "__main__":
    rolling_credits('credits.txt', ['Alice', 'Bob', 'Charlie'], ['Follower1', 'Follower2'])
