# Importação das bibliotecas necessárias para o projeto
import cv2  # OpenCV para captura de vídeo, manipulação de imagens e exibição
import mediapipe as mp  # MediaPipe para detecção de mãos em tempo real
import numpy as np  # NumPy para manipulação de arrays, usado no contorno personalizado
import time  # Para controle de FPS e monitoramento de desempenho

# Inicialização dos módulos do MediaPipe
# mp_hands: Módulo para detecção de mãos, fornecendo 21 landmarks por mão
# mp_drawing: Utilitário para desenhar landmarks e conexões na imagem
# mp_drawing_styles: Estilos visuais pré-definidos para landmarks e conexões
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


def detect_hands_realtime():
    """
    Detecta mãos em tempo real usando a webcam e desenha o contorno do exoesqueleto.

    Funcionalidade:
        - Inicializa a webcam e processa cada frame para detectar mãos.
        - Desenha landmarks e um contorno personalizado do exoesqueleto.
        - Exibe o vídeo processado em uma janela com informações de FPS.
        - Sai ao pressionar a tecla 'q'.

    Returns:
        None: A função exibe o vídeo em tempo real e não retorna valores.

    Note:
        - Requer uma webcam funcional (índice 0 por padrão).
        - A detecção pode falhar em condições de baixa iluminação ou fundo complexo.
    """

    # Inicialização da captura de vídeo
    # cv2.VideoCapture(0) acessa a webcam padrão (índice 0)
    # Alternativas: índice 1 ou caminho de vídeo para outros dispositivos/fontes
    cap = cv2.VideoCapture(0)

    # Verificação se a captura foi inicializada corretamente
    if not cap.isOpened():
        print("Erro: Não foi possível inicializar a webcam.")
        return

    # Configuração do detector de mãos do MediaPipe
    # static_image_mode=False: Otimizado para vídeo, priorizando continuidade entre frames
    # max_num_hands=2: Limita a duas mãos para equilibrar desempenho e casos comuns
    # min_detection_confidence=0.5: Threshold moderado para evitar falsos positivos
    # min_tracking_confidence=0.5: Confiança mínima para rastreamento entre frames
    # O uso de 'with' garante liberação de recursos do MediaPipe
    with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

        # Variável para cálculo de FPS
        prev_time = time.time()

        # Loop principal para captura e processamento de frames
        while cap.isOpened():
            # Leitura de um frame da webcam
            # success: Booleano indicando se a leitura foi bem-sucedida
            # frame: Imagem capturada (BGR por padrão no OpenCV)
            success, frame = cap.read()
            if not success:
                print("Erro: Falha ao capturar frame da webcam.")
                break

            # Conversão do frame de BGR para RGB
            # MediaPipe requer imagens em RGB, enquanto OpenCV usa BGR
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Processamento do frame para detectar mãos
            # O método process retorna landmarks normalizados (x, y, z) para cada mão
            results = hands.process(frame_rgb)

            # Criação de uma cópia do frame para desenhar resultados
            # Evita modificar o frame original, garantindo segurança
            annotated_frame = frame.copy()

            # Verificação se mãos foram detectadas
            if results.multi_hand_landmarks:
                # Passagem por cada mão detectada
                for hand_landmarks in results.multi_hand_landmarks:
                    # Desenho dos landmarks e conexões usando utilitários do MediaPipe
                    # Isso inclui círculos nos pontos-chave e linhas entre eles
                    mp_drawing.draw_landmarks(
                        annotated_frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

                    # Extração das dimensões do frame
                    # Necessário para converter coordenadas normalizadas em pixels
                    h, w, _ = annotated_frame.shape

                    # Lista para armazenar coordenadas dos landmarks em pixels
                    points = []
                    # Percorrer cada landmark para conversão de coordenadas
                    for landmark in hand_landmarks.landmark:
                        # Conversão de coordenadas normalizadas (0 a 1) para pixels
                        cx, cy = int(landmark.x * w), int(landmark.y * h)
                        points.append((cx, cy))

                    # Definição do contorno do exoesqueleto
                    # Conecta landmarks na ordem: pulso → dedos → pulso
                    # A ordem reflete a estrutura externa da mão para destacar o exoesqueleto
                    contour_points = [
                        points[0],  # Pulso
                        points[1], points[2], points[3], points[4],  # Indicador
                        points[5], points[6], points[7], points[8],  # Médio
                        points[9], points[10], points[11], points[12],  # Anelar
                        points[13], points[14], points[15], points[16],  # Mindinho
                        points[17], points[18], points[19], points[20],  # Polegar
                        points[0]  # Volta ao pulso
                    ]

                    # Conversão para array NumPy
                    # cv2.polylines requer um array de pontos no formato correto
                    contour = np.array(contour_points, dtype=np.int32)

                    # Desenho do contorno no frame
                    # Verde (0, 255, 0) para visibilidade, espessura 2 para destaque
                    cv2.polylines(annotated_frame, [contour], isClosed=True, color=(0, 255, 0), thickness=2)

            # Cálculo do FPS
            # Diferença de tempo entre frames para estimar a taxa de quadros
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time

            # Adição do FPS ao frame
            # cv2.putText exibe o FPS no canto superior esquerdo
            cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Exibição do frame processado
            # 'Hand Detection' é o nome da janela
            cv2.imshow("Hand Detection", annotated_frame)

            # Verificação para saída do loop
            # Sai ao pressionar 'q' (tecla ASCII 113)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Liberação de recursos
    # Garante que a webcam e janelas sejam fechadas adequadamente
    cap.release()
    cv2.destroyAllWindows()


# Ponto de entrada do script
if __name__ == "__main__":
    """
    Bloco principal para execução do detector de mãos em tempo real.
    - Inicializa a webcam e começa a detecção.
    - Facilita testes diretos sem parâmetros adicionais.
    """
    try:
        detect_hands_realtime()
    except Exception as e:
        # Tratamento genérico de erros para depuração
        print(f"Erro durante a execução: {e}")