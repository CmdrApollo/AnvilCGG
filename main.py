import pygame
import asyncio
import random
from skimage import color as c_space

pygame.init()

width, height = 1280, 720

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Anvil Color Guessing Game")

font = pygame.font.Font("CourierNew.ttf", 20)

async def main():
    clock = pygame.time.Clock()
    delta: float = 0.0
    
    banned_colors: list[str] = [
        "aliceblue",
        "antiquewhite",
        "blanchedalmond",
        "burlywood",
        "cornflowerblue",
        "cornsilk",
        "darkkhaki",
        "dimgray",
        "dimgrey",
        "dodgerblue",
        "floralwhite",
        "gainsboro",
        "ghostwhite",
        "ivory",
        "khaki",
        "lavenderblush",
        "lawngreen",
        "lemonchiffon",
        "lightsteelblue",
        "linen",
        "limegreen",
        "mintcream",
        "mistyrose",
        "moccasin",
        "navajowhite",
        "navyblue",
        "oldlace",
        "olivedrab",
        "papayawhip",
        "peachpuff",
        "peru",
        "rosybrown",
        "seashell",
        "snow",
        "springgreen",
        "wheat",
        "whitesmoke",
    ]

    all_colors = []
    
    for c in pygame.color.THECOLORS:
        if c[-1].isdigit() or c in banned_colors or "medium" in c:
            continue
        all_colors.append(c)

    final_color = random.choice(all_colors)

    final_tup = c_space.rgb2lab([a / 255 for a in pygame.Color(final_color).rbg])

    current_guess = ""
    guesses = []

    current_color = None

    pygame.key.set_repeat(250, 100)

    running: bool = True
    while running:
        delta = clock.tick_busy_loop(60.0) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.TEXTINPUT:
                current_guess += event.text

                current_color = None

                for color in all_colors:
                    if current_guess.strip().replace(' ', '').lower() == color:
                        current_color = color
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    current_guess = current_guess[:-1]

                    current_color = None

                    for color in all_colors:
                        if current_guess.strip().replace(' ', '').lower() == color:
                            current_color = color
                elif event.key == pygame.K_RETURN:
                    if current_color != None:
                        guesses.append(current_color)
                        current_color = None
                        current_guess = ""
                    if current_guess.lower().strip() == "!reveal":
                        guesses.append(final_color)
                        current_color = None
                        current_guess = ""
                    if current_guess.lower().strip() == "!again":
                        final_color = random.choice(all_colors)
                        final_tup = c_space.rgb2lab([a / 255 for a in pygame.Color(final_color).rbg])

                        current_guess = ""
                        guesses = []

                        current_color = None

        screen.fill('#202040')

        s = 40
        t = (pygame.time.get_ticks() / 100) % s

        for x in range(width // s + 1):
            for y in range(height // s + 1):
                if (x + y) & 1:
                    pygame.draw.rect(screen, '#303050', (x * s - t, y * s - t, s, s))

        if current_color != None:
            pygame.draw.circle(screen, current_color, (width // 2, height // 6), 32)
        else:
            screen.blit(s := font.render("???", True, 'antiquewhite'), (width // 2 - s.get_width() // 2, height // 6 - s.get_height() // 2))
        pygame.draw.circle(screen, 'black', (width // 2, height // 6), 32, 1)

        screen.blit(s := font.render("---How to Play---\nIn order to play ACGG, use the keyboard to type out your guess before hitting enter/return to lock in your guess. The game will then tell you how close you are on a scale from 0.0(furthest) to 100.0(closest). On an 100, you win! Type \"!reveal\" to give up and reveal the answer. Type \"!again\" to play again.", True, 'antiquewhite', wraplength=(width//5-10)), (width - s.get_width() - 5, height - s.get_height() - 5))
        s = font.render(current_guess + ("|" if (pygame.time.get_ticks() // 350) & 1 else " "), True, 'antiquewhite')
        pygame.draw.rect(screen, 'black', (width // 2 - s.get_width() // 2 - 5, height // 4 - s.get_height() // 2 - 5, s.get_width() + 10, s.get_height() + 10), 0, 8)
        screen.blit(s, (width // 2 - s.get_width() // 2, height // 4 - s.get_height() // 2))

        size = 32
        x_positions = [width // 7, (width * 2) // 7, (width * 3) // 7, (width * 4) // 7,  (width * 5) // 7]

        has_won = False

        for i, guess in enumerate(guesses):
            tup = c_space.rgb2lab([a / 255 for a in pygame.Color(guess).rbg])


            p = 0
            p += abs(final_tup[0] - tup[0]) / 100
            p += abs(final_tup[1] - tup[1]) / 100
            p += abs(final_tup[2] - tup[2]) / 100
            p /= 3

            if p == 0.0:
                has_won = True
            
            x, y = i % len(x_positions), i // len(x_positions)

            pygame.draw.rect(screen, guess, (x_positions[x] - size // 2, height // 3 + (size + 60) * y, size, size), 0, 8)
            pygame.draw.rect(screen, 'black', (x_positions[x] - size // 2, height // 3 + (size + 60) * y, size, size), 1, 8)
            screen.blit(s := font.render(f"{guess}\n{((1.0 - p) * 100.0):.1f}%", True, "antiquewhite"), (x_positions[x] - s.get_width() // 2, height // 3 + (size + 60) * y + size + 5))

        if has_won:
            screen.blit(s := font.render(f"You have won! The color was \"{final_color}\".", True, "antiquewhite"), (width // 2 - s.get_width() // 2, height - s.get_height() - 5))

        pygame.display.flip()

        await asyncio.sleep(0)
    
    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())