Este projeto de computação gráfica foi desenvolvido utilizando diversas bibliotecas para renderização 3D, manipulação de textura, manipulação de vídeo e execução paralela:

**OpenGL (PyOpenGL)**: Usado para renderizar gráficos 3D e 2D, aplicar shaders personalizados e manipular transformações de câmera, luz e objetos na cena.
**PyWavefront**: Para carregar e manipular modelos 3D no formato .obj.
**OpenCV**: Utilizado para carregar e processar vídeos, exibindo frames como texturas dinâmicas dentro da renderização 3D.
**MoviePy**: Manipula arquivos de vídeo para efeitos de reprodução.
**Pygame**: Responsável pela reprodução de sons e trilhas sonoras de fundo.
**PIL (Python Imaging Library)**: Para carregamento e aplicação de texturas.
**Threading (biblioteca padrão do Python)**: Implementa execução paralela, permitindo que o vídeo seja carregado e exibido sem bloquear a renderização principal da cena. Uma fila (queue.Queue) é utilizada para armazenar frames do vídeo e gerenciar o fluxo de dados de forma eficiente.
**GLUT**: Fornece a interface de janela, controle de eventos de teclado e manipulação de entrada do usuário.

# Imagens do Projeto

**Imagem 01**
![image](https://github.com/user-attachments/assets/77c917e3-47db-485b-b56c-1617bef24951)

**Imagem 02**
![image](https://github.com/user-attachments/assets/ec6978c2-b53f-4974-8d7d-7d68ca8371ed)
