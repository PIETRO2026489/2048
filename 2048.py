import pygame
import random
import sys

pygame.init()

# -----------------------------
# CONFIGURAÇÕES
# -----------------------------
LARGURA, ALTURA = 560, 700
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("2048 - Cores Novas")

FPS = 60
TAMANHO_TABULEIRO = 4
TAMANHO_CELULA = 115
ESPACO = 10
X_TAB = 45
Y_TAB = 185

# -----------------------------
# CORES
# -----------------------------
FUNDO = (24, 28, 45)
PAINEL = (34, 40, 63)
TABULEIRO = (48, 55, 82)
CELULA_VAZIA = (65, 73, 104)
TEXTO = (245, 247, 255)
TEXTO_ESCURA = (35, 38, 52)
BOTAO = (79, 93, 180)
BOTAO_HOVER = (96, 112, 215)

# Nova paleta dos quadrados
CORES_QUADRADOS = {
    0: CELULA_VAZIA,
    2: (82, 167, 255),
    4: (67, 204, 170),
    8: (255, 193, 92),
    16: (255, 137, 82),
    32: (239, 92, 92),
    64: (210, 76, 145),
    128: (167, 102, 235),
    256: (123, 92, 224),
    512: (91, 110, 230),
    1024: (74, 171, 218),
    2048: (65, 220, 173),
    4096: (247, 214, 77),
}

FONTE_TITULO = pygame.font.SysFont("arial", 60, bold=True)
FONTE_NUMERO = pygame.font.SysFont("arial", 38, bold=True)
FONTE_NUMERO_GRANDE = pygame.font.SysFont("arial", 30, bold=True)
FONTE_SCORE = pygame.font.SysFont("arial", 22, bold=True)
FONTE_PEQUENA = pygame.font.SysFont("arial", 18)
FONTE_FIM = pygame.font.SysFont("arial", 46, bold=True)

# -----------------------------
# ESTADO DO JOGO
# -----------------------------
tabuleiro = []
pontuacao = 0
venceu = False
fim_de_jogo = False


def novo_tabuleiro():
    return [[0 for _ in range(TAMANHO_TABULEIRO)]
            for _ in range(TAMANHO_TABULEIRO)]


def adicionar_numero():
    vazios = [
        (linha, coluna)
        for linha in range(TAMANHO_TABULEIRO)
        for coluna in range(TAMANHO_TABULEIRO)
        if tabuleiro[linha][coluna] == 0
    ]

    if not vazios:
        return

    linha, coluna = random.choice(vazios)
    tabuleiro[linha][coluna] = 2 if random.random() < 0.9 else 4


def reiniciar_jogo():
    global tabuleiro, pontuacao, venceu, fim_de_jogo

    tabuleiro = novo_tabuleiro()
    pontuacao = 0
    venceu = False
    fim_de_jogo = False

    adicionar_numero()
    adicionar_numero()


def mover_linha(linha):
    global pontuacao

    filtrada = [numero for numero in linha if numero != 0]
    resultado = []
    indice = 0

    while indice < len(filtrada):
        if (
            indice + 1 < len(filtrada)
            and filtrada[indice] == filtrada[indice + 1]
        ):
            novo_valor = filtrada[indice] * 2
            resultado.append(novo_valor)
            pontuacao += novo_valor
            indice += 2
        else:
            resultado.append(filtrada[indice])
            indice += 1

    while len(resultado) < TAMANHO_TABULEIRO:
        resultado.append(0)

    return resultado


def mover_esquerda():
    mudou = False

    for linha in range(TAMANHO_TABULEIRO):
        antiga = tabuleiro[linha][:]
        tabuleiro[linha] = mover_linha(tabuleiro[linha])

        if antiga != tabuleiro[linha]:
            mudou = True

    return mudou


def mover_direita():
    mudou = False

    for linha in range(TAMANHO_TABULEIRO):
        antiga = tabuleiro[linha][:]
        tabuleiro[linha] = mover_linha(tabuleiro[linha][::-1])[::-1]

        if antiga != tabuleiro[linha]:
            mudou = True

    return mudou


def mover_cima():
    mudou = False

    for coluna in range(TAMANHO_TABULEIRO):
        antiga = [tabuleiro[linha][coluna] for linha in range(TAMANHO_TABULEIRO)]
        nova = mover_linha(antiga)

        for linha in range(TAMANHO_TABULEIRO):
            tabuleiro[linha][coluna] = nova[linha]

        if antiga != nova:
            mudou = True

    return mudou


def mover_baixo():
    mudou = False

    for coluna in range(TAMANHO_TABULEIRO):
        antiga = [tabuleiro[linha][coluna] for linha in range(TAMANHO_TABULEIRO)]
        nova = mover_linha(antiga[::-1])[::-1]

        for linha in range(TAMANHO_TABULEIRO):
            tabuleiro[linha][coluna] = nova[linha]

        if antiga != nova:
            mudou = True

    return mudou


def pode_mover():
    for linha in range(TAMANHO_TABULEIRO):
        for coluna in range(TAMANHO_TABULEIRO):
            if tabuleiro[linha][coluna] == 0:
                return True

            if coluna + 1 < TAMANHO_TABULEIRO:
                if tabuleiro[linha][coluna] == tabuleiro[linha][coluna + 1]:
                    return True

            if linha + 1 < TAMANHO_TABULEIRO:
                if tabuleiro[linha][coluna] == tabuleiro[linha + 1][coluna]:
                    return True

    return False


def verificar_fim():
    global venceu, fim_de_jogo

    if any(
        2048 in linha
        for linha in tabuleiro
    ):
        venceu = True

    if not pode_mover():
        fim_de_jogo = True


def fazer_movimento(direcao):
    if venceu or fim_de_jogo:
        return

    if direcao == "esquerda":
        mudou = mover_esquerda()
    elif direcao == "direita":
        mudou = mover_direita()
    elif direcao == "cima":
        mudou = mover_cima()
    else:
        mudou = mover_baixo()

    if mudou:
        adicionar_numero()
        verificar_fim()


def desenhar_texto_central(texto, fonte, cor, retangulo):
    superficie = fonte.render(str(texto), True, cor)
    x = retangulo.centerx - superficie.get_width() // 2
    y = retangulo.centery - superficie.get_height() // 2
    TELA.blit(superficie, (x, y))


def desenhar():
    TELA.fill(FUNDO)

    # Título
    titulo = FONTE_TITULO.render("2048", True, TEXTO)
    TELA.blit(titulo, (45, 35))

    # Pontuação
    caixa_score = pygame.Rect(365, 38, 150, 70)
    pygame.draw.rect(TELA, PAINEL, caixa_score, border_radius=10)

    texto_score = FONTE_SCORE.render("PONTOS", True, (175, 182, 210))
    TELA.blit(texto_score, (caixa_score.centerx - texto_score.get_width() // 2, 46))

    valor_score = FONTE_NUMERO_GRANDE.render(str(pontuacao), True, TEXTO)
    TELA.blit(valor_score, (caixa_score.centerx - valor_score.get_width() // 2, 69))

    # Instrução
    instrucao = FONTE_PEQUENA.render(
        "Use as setas ou WASD para mover os quadrados",
        True,
        (190, 197, 220)
    )
    TELA.blit(instrucao, (45, 125))

    # Tabuleiro
    area = pygame.Rect(
        X_TAB - 10,
        Y_TAB - 10,
        4 * TAMANHO_CELULA + 5 * ESPACO,
        4 * TAMANHO_CELULA + 5 * ESPACO
    )
    pygame.draw.rect(TELA, TABULEIRO, area, border_radius=12)

    for linha in range(TAMANHO_TABULEIRO):
        for coluna in range(TAMANHO_TABULEIRO):
            valor = tabuleiro[linha][coluna]

            x = X_TAB + coluna * (TAMANHO_CELULA + ESPACO)
            y = Y_TAB + linha * (TAMANHO_CELULA + ESPACO)

            retangulo = pygame.Rect(x, y, TAMANHO_CELULA, TAMANHO_CELULA)
            cor = CORES_QUADRADOS.get(
                valor,
                (60, 60, 60)
            )

            pygame.draw.rect(TELA, cor, retangulo, border_radius=10)

            if valor != 0:
                cor_texto = TEXTO_ESCURA if valor <= 4 else TEXTO

                if valor >= 1024:
                    fonte = FONTE_NUMERO_GRANDE
                else:
                    fonte = FONTE_NUMERO

                desenhar_texto_central(
                    valor,
                    fonte,
                    cor_texto,
                    retangulo
                )

    # Botão reiniciar
    botao = pygame.Rect(190, 650, 180, 40)
    cor_botao = BOTAO

    if botao.collidepoint(pygame.mouse.get_pos()):
        cor_botao = BOTAO_HOVER

    pygame.draw.rect(TELA, cor_botao, botao, border_radius=8)

    texto_botao = FONTE_PEQUENA.render("NOVO JOGO", True, TEXTO)
    TELA.blit(
        texto_botao,
        (
            botao.centerx - texto_botao.get_width() // 2,
            botao.centery - texto_botao.get_height() // 2
        )
    )

    # Tela de vitória/fim
    if venceu or fim_de_jogo:
        camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        camada.fill((16, 20, 34, 205))
        TELA.blit(camada, (0, 0))

        mensagem = "VOCÊ CHEGOU AO 2048!" if venceu else "FIM DE JOGO!"
        texto = FONTE_FIM.render(mensagem, True, TEXTO)
        TELA.blit(
            texto,
            (
                LARGURA // 2 - texto.get_width() // 2,
                270
            )
        )

        texto_pontos = FONTE_SCORE.render(
            f"Pontuação: {pontuacao}",
            True,
            (205, 211, 235)
        )
        TELA.blit(
            texto_pontos,
            (
                LARGURA // 2 - texto_pontos.get_width() // 2,
                330
            )
        )

        dica = FONTE_PEQUENA.render(
            "Clique em NOVO JOGO para jogar novamente",
            True,
            (190, 197, 220)
        )
        TELA.blit(
            dica,
            (
                LARGURA // 2 - dica.get_width() // 2,
                365
            )
        )

    pygame.display.flip()


def tratar_movimento_teclado(tecla):
    movimentos = {
        pygame.K_LEFT: "esquerda",
        pygame.K_RIGHT: "direita",
        pygame.K_UP: "cima",
        pygame.K_DOWN: "baixo",
        pygame.K_a: "esquerda",
        pygame.K_d: "direita",
        pygame.K_w: "cima",
        pygame.K_s: "baixo",
    }

    if tecla in movimentos:
        fazer_movimento(movimentos[tecla])


# -----------------------------
# INÍCIO
# -----------------------------
reiniciar_jogo()
relogio = pygame.time.Clock()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            tratar_movimento_teclado(evento.key)

            if evento.key == pygame.K_r:
                reiniciar_jogo()

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            botao = pygame.Rect(190, 650, 180, 40)

            if botao.collidepoint(evento.pos):
                reiniciar_jogo()

    desenhar()
    relogio.tick(FPS)
