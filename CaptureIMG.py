#!/usr/bin/python3

import cv2
import pygame
import os

def main():

    # Codigo para abrir o video capturado e salvar uma imagem ao carregar numa tecla

    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    # Abrir camera e mostrar video em tempo real
    # camera = cv2.VideoCapture(2)

    # Abrir video previamente gravado
    # video_path = '/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/Capture/Videos/cam_video_measure.avi'
    video_path = '/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/Capture/Videos/cam2_sf_video5.avi'
    camera = cv2.VideoCapture(video_path)

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('/DigiAqua/FastSAM/Capture/capturado.avi', fourcc, 10.0, (640, 480))

    output_folder = "/home/vinicius/catkin_ws/src/DigiAqua/FastSAM/Capture"

    while camera.isOpened():
        ret, frame = camera.read()

        # Verifique se o quadro foi lido corretamente
        if not ret:
            print("Não foi possível ler o próximo quadro. O vídeo pode ter chegado ao fim.")
            break

        # Inverte horizontalmente o quadro se necessário
        frame = cv2.flip(frame, 1)  # 1 para espelhamento horizontal

        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pygame_frame = pygame.surfarray.make_surface(frame_rgb)

        # Exibe o frame na janela do Pygame
        screen.blit(pygame_frame, (0, 0))
        pygame.display.flip()

        # Gravar o frame no vídeo
        out.write(frame)

        # Aguarde a tecla r ser pressionada
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    frame_rotated = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                    frame_rotated = cv2.flip(frame_rotated, 1)
                    frame_filename = os.path.join(output_folder, f"frame_{len(os.listdir(output_folder)) + 1}.png")
                    cv2.imwrite(frame_filename, frame_rotated)
                    print(f"Frame salvo como '{frame_filename}'.")

                if event.key == pygame.K_q:
                    camera.release()
                    cv2.destroyAllWindows()
                    pygame.quit()
                    quit()

if __name__ == '__main__':
    main()
