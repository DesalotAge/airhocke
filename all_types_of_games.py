from constants import *
from player import *
from puck import *
from random import randint
from utils import *
from serv import network
import threading
import concurrent.futures
from multiprocessing.pool import ThreadPool
from serv.network import Networking

def two_in_one(pygame):
    pygame.display.set_caption('Hockey')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    running = True
    v = 100
    fps = 120
    clock = pygame.time.Clock()
    w = pygame.Color("white")
    first_coef, second_coef = 1, 1
    first = Player([width / 4, height / 2], 50, 1, height, width)
    second = Player([3 * width / 4, height / 2], 50, 0, height, width)
    puck = Puck([width / 2 + 95, height / 2] if randint(0, 1) else [width / 2 - 95, height / 2], [first, second], 25, height, width)
    first_score, second_score = 0, 0
    main_font = pygame.font.Font(None, 36)
    is_animated = 1
    animation_color = [55, 55, 55, 255]
    puck_radius = 50
    animation_radius = 50


    return_to_menu = Button(465, 540, 65, 50)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 1000
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    first.change_movement().change_y(-NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_a:
                    first.change_movement().change_x(-NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_s:
                    first.change_movement().change_y(NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_d:
                    first.change_movement().change_x(NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_UP:
                    second.change_movement().change_y(-NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_LEFT:
                    second.change_movement().change_x(-NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_DOWN:
                    second.change_movement().change_y(NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_RIGHT:
                    second.change_movement().change_x(NORMAL_MOVEMENT * second_coef)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    first.change_movement().change_y(NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_a:
                    first.change_movement().change_x(NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_s:
                    first.change_movement().change_y(-NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_d:
                    first.change_movement().change_x(-NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_UP:
                    second.change_movement().change_y(NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_LEFT:
                    second.change_movement().change_x(NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_DOWN:
                    second.change_movement().change_y(-NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_RIGHT:
                    second.change_movement().change_x(-NORMAL_MOVEMENT * second_coef)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if return_to_menu.is_clicked(mouse_pos):
                    return 0

        screen.fill((0, 0, 0))

        
        '''
            draw field
        '''
        pygame.draw.line(screen, WHITE, [0, 0], [width, 0], BORDERS)
        pygame.draw.line(screen, WHITE, [0, height - 1], [width , height - 1], BORDERS)
        pygame.draw.line(screen, WHITE, [0, 0], [0, height / 2 - GATES_SIZE / 2], BORDERS)
        pygame.draw.line(screen, WHITE, [0, height/ 2 + GATES_SIZE / 2], [0, height], BORDERS)
        pygame.draw.line(screen, WHITE, [width - 1, 0], [width - 1, height / 2 - GATES_SIZE / 2], BORDERS)
        pygame.draw.line(screen, WHITE, [width - 1, height/ 2 + GATES_SIZE / 2], [width - 1, height], BORDERS)
        pygame.draw.line(screen, WHITE, [width / 2, 0], [width / 2, height], BORDERS - 1)
        pygame.draw.circle(screen, WHITE, [width / 2, height / 2], 95, 1)
        '''
            render goals
        '''
        rez = puck.check_goal()
        if rez:
            if rez == 1:
                puck.coords = width / 2, height / 2
                puck.movement.set(0, 0)
                first_score += 1
                puck.coords = [width / 2 + 95, height / 2]

            if rez == 2:
                puck.coords = width / 2, height / 2
                puck.movement.set(0, 0)
                second_score += 1

                puck.coords = [width / 2 - 95, height / 2]

            is_animated = 1
            animation_color = [55, 55, 55, 255]
            animation_radius = 50
            first.coords = [width / 4, height / 2]
            second.coords = [3 * width / 4, height / 2]
        if max(first_score, second_score) >= 11:
            if first_score > second_score:
                return result(pygame, "Red player won")
            else:
                return result(pygame, "Blue player won")

        if animation_color != [255, 255, 255, 255]:
            for i in range(3):
                animation_color[i] += 5
            animation_radius += (25 - puck_radius) / (200 / 5)
            clock.tick(100)
        else:
            is_animated = 0

        '''
            rewriting objects
        '''
        if is_animated:
            pygame.draw.circle(*puck.remove_collision().change_coords().draw_info(screen, pygame.Color(*animation_color), animation_radius))
            pygame.draw.circle(*first.draw_info(screen))
            pygame.draw.circle(*second.draw_info(screen))
        else:
            pygame.draw.circle(*puck.remove_collision().change_coords().draw_info(screen))
            pygame.draw.circle(*first.change_coords().draw_info(screen))
            pygame.draw.circle(*second.change_coords().draw_info(screen))

        first_score_object = main_font.render(str(first_score), True, BLUE)
        second_score_object = main_font.render(str(second_score), True, RED)
        screen.blit(first_score_object, (width / 2 - 40, 10))
        screen.blit(second_score_object, (width / 2 + 30, 10))
        return_to_menu.draw("Menu", 20, pygame=pygame, screen=screen)
        clock.tick(fps)
        pygame.display.flip()
    return 0


def game_intro(pygame):
    pygame.display.set_caption('Air hockey')
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    running = True
    v = 100
    fps = 120
    clock = pygame.time.Clock()
    w = pygame.Color("white")
    running = True
    two_players_button = Button(200, 250, 150, 50)
    online_players_button = Button(450, 250, 90, 50)
    ai_plaing = Button(650, 250, 160, 50)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 1000

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos 

                if two_players_button.is_clicked(mouse_pos):
                    return 1

                if online_players_button.is_clicked(mouse_pos):
                    return 2

                if ai_plaing.is_clicked(mouse_pos):
                    return 3

        screen.fill((0, 0, 0))
        two_players_button.draw("Two players", 20, pygame=pygame, screen=screen)
        online_players_button.draw('Online', 20, pygame=pygame, screen = screen)
        ai_plaing.draw("Play with ai", 20, pygame=pygame, screen=screen)

        pygame.display.update()
        clock.tick(fps)


def result(pygame, rez):

    pygame.display.set_caption('Hockey')
    size = 1000, 600
    screen = pygame.display.set_mode(size)
    running = True
    fps = 120
    clock = pygame.time.Clock()
    return_to_menu = Button(465, 540, 65, 50)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 1000

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos 
                if return_to_menu.is_clicked(mouse_pos):
                    return 0

        screen.fill((0, 0, 0))
        write_text(rez, (355, 250), 30, pygame, screen, color=WHITE)
        return_to_menu.draw("Menu", 20, pygame, screen)
        pygame.display.update()
        clock.tick(fps)


def online(pygame):
    result = [None]
    thread = threading.Thread(target=connect, args=(result, 0))
    thread.start()
    pygame.display.set_caption('Hockey')
    text = "Looking for opponent"
    size = width, height = 1000, 600
    screen = pygame.display.set_mode(size)
    running = True
    fps = 120
    opponent = None
    clock = pygame.time.Clock()
    return_to_menu = Button(465, 540, 65, 50)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 1000

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos 
                if return_to_menu.is_clicked(mouse_pos):
                    return 0
        if result[0]:
            opponent = result[0]
            break
        screen.fill((0, 0, 0))
        
        write_text(text, (330, 250), 30, pygame, screen, color=WHITE)
        return_to_menu.draw("Menu", 20, pygame, screen)
        
        pygame.display.update()
        clock.tick(fps)
    
    print(opponent)
    make_rules = (opponent['my'] > opponent['enemy'][1])
    opponent_ip = opponent['enemy'][0][0]

    ######################################################################################
    ######################################################################################
    ######################################################################################
    ######################################################################################
    ######################################################################################

    running = True
    fps = 120
    clock = pygame.time.Clock()
    first_coef, second_coef = 1, 1
    my_player = Player([width / 4, height / 2], 50, 1, height, width)
    opponent_player = Player([3 * width / 4, height / 2], 50, 0, height, width)
    puck = Puck([width / 2 + 95, height / 2] if randint(0, 1) else [width / 2 - 95, height / 2], [my_player, opponent_player], 25, height, width)
    my_score, opponent_score = 0, 0
    main_font = pygame.font.Font(None, 36)
    is_animated = 1
    animation_color = [55, 55, 55, 255]
    puck_radius = 50
    animation_radius = 50


    return_to_menu = Button(465, 540, 65, 50)


    connected = Networking(37020)
    print(opponent_ip)
    connected.bind(opponent_ip)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return 1000
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    my_player.change_movement().change_y(-NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_a:
                    my_player.change_movement().change_x(-NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_s:
                    my_player.change_movement().change_y(NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_d:
                    my_player.change_movement().change_x(NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_UP:
                    my_player.change_movement().change_y(-NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_LEFT:
                    my_player.change_movement().change_x(-NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_DOWN:
                    my_player.change_movement().change_y(NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_RIGHT:
                    my_player.change_movement().change_x(NORMAL_MOVEMENT * second_coef)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    my_player.change_movement().change_y(NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_a:
                    my_player.change_movement().change_x(NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_s:
                    my_player.change_movement().change_y(-NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_d:
                    my_player.change_movement().change_x(-NORMAL_MOVEMENT * first_coef)
                if event.key == pygame.K_UP:
                    my_player.change_movement().change_y(NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_LEFT:
                    my_player.change_movement().change_x(NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_DOWN:
                    my_player.change_movement().change_y(-NORMAL_MOVEMENT * second_coef)
                if event.key == pygame.K_RIGHT:
                    my_player.change_movement().change_x(-NORMAL_MOVEMENT * second_coef)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if return_to_menu.is_clicked(mouse_pos):
                    return 0

        screen.fill((0, 0, 0))

        
        '''
            draw field
        '''
        pygame.draw.line(screen, WHITE, [0, 0], [width, 0], BORDERS)
        pygame.draw.line(screen, WHITE, [0, height - 1], [width , height - 1], BORDERS)
        pygame.draw.line(screen, WHITE, [0, 0], [0, height / 2 - GATES_SIZE / 2], BORDERS)
        pygame.draw.line(screen, WHITE, [0, height/ 2 + GATES_SIZE / 2], [0, height], BORDERS)
        pygame.draw.line(screen, WHITE, [width - 1, 0], [width - 1, height / 2 - GATES_SIZE / 2], BORDERS)
        pygame.draw.line(screen, WHITE, [width - 1, height/ 2 + GATES_SIZE / 2], [width - 1, height], BORDERS)
        pygame.draw.line(screen, WHITE, [width / 2, 0], [width / 2, height], BORDERS - 1)
        pygame.draw.circle(screen, WHITE, [width / 2, height / 2], 95, 1)
        '''
            render goals
        '''
        if make_rules:
            connected.send_json({
                'your_coords': opponent_player.get_coords(),
                'my_coords': my_player.get_coords(),
                'puck_coords': puck.coords,
                "score": (my_score, opponent_score),
            }, opponent_ip)
        else:
            connected.send_json({
                'my_vector': my_player.movement.get(),
            }, opponent_ip)
        data = connected.recv_json()
        print(data)
        # if make_rules:
        #     opponent_player.movement = tuple(data['my_vector'])
        # else:

        


        # rez = puck.check_goal()
        # if rez:
        #     if rez == 1:
        #         puck.coords = width / 2, height / 2
        #         puck.movement.set(0, 0)
        #         first_score += 1
        #         puck.coords = [width / 2 + 95, height / 2]

        #     if rez == 2:
        #         puck.coords = width / 2, height / 2
        #         puck.movement.set(0, 0)
        #         second_score += 1

        #         puck.coords = [width / 2 - 95, height / 2]

        #     is_animated = 1
        #     animation_color = [55, 55, 55, 255]
        #     animation_radius = 50
        #     first.coords = [width / 4, height / 2]
        #     second.coords = [3 * width / 4, height / 2]
        # if max(first_score, second_score) >= 11:
        #     if first_score > second_score:
        #         return result(pygame, "Red player won")
        #     else:
        #         return result(pygame, "Blue player won")

        # if animation_color != [255, 255, 255, 255]:
        #     for i in range(3):
        #         animation_color[i] += 5
        #     animation_radius += (25 - puck_radius) / (200 / 5)
        #     clock.tick(100)
        # else:
        #     is_animated = 0

        # '''
        #     rewriting objects
        # '''
        # if is_animated:
        #     pygame.draw.circle(*puck.remove_collision().change_coords().draw_info(screen, pygame.Color(*animation_color), animation_radius))
        #     pygame.draw.circle(*first.draw_info(screen))
        #     pygame.draw.circle(*second.draw_info(screen))
        # else:
        #     pygame.draw.circle(*puck.remove_collision().change_coords().draw_info(screen))
        #     pygame.draw.circle(*first.change_coords().draw_info(screen))
        #     pygame.draw.circle(*second.change_coords().draw_info(screen))

        # first_score_object = main_font.render(str(first_score), True, WHITE)
        # second_score_object = main_font.render(str(second_score), True, WHITE)
        # screen.blit(first_score_object, (width / 2 - 40, 10))
        # screen.blit(second_score_object, (width / 2 + 30, 10))
        # return_to_menu.draw("Menu", 20, pygame=pygame, screen=screen)
        # clock.tick(fps)
        # pygame.display.flip()
    return 0
    ######################################################################################
    ######################################################################################
    ######################################################################################
    ######################################################################################


def ai(pygame):
    pass