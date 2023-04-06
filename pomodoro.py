import json # Permite as configurações serem salvas.
import asyncio as asy # Permite o cronomêtro dos intervalos.
import pygame # Integração de som aos intervalos



pygame.mixer.init() #Inicia o módulo mixer da Biblioteca PyGame

somInicio = pygame.mixer.Sound('sounds/start.mp3') # Som de inicio do pomodoro.
somCurto = pygame.mixer.Sound('sounds/pauses.mp3') # Som da pausa curta.
somLongo = pygame.mixer.Sound('sounds/pausel.mp3') # Som da pausa longa.

somInicio.set_volume(0.1) # Deixa o volume do som em 10%
somLongo.set_volume(0.2) # Deixa o volume do som em 20%



tfinal = 0 # Contar o tempo estudado



async def timer(t): # A função Assíncrona do cronometro 
    await asy.sleep(t*60)   # O cronometro com o tempo em minutos multiplicadado para segundos


def pomodoro(): # Função do pomodoro
    r = open('config.json') # Abre a configuração
    config =  json.load(r) # Armazena os dados no dicionario config
    t_estudo = int(config["tempo_estudo"]) # Armazena o tempo de estudo da configuração
    pcurta = int(config["pausa_curta"]) # Armazena o tempo da pausa curta da configuração
    plonga = int(config["pausa_longa"]) # Armazena o tempo de pausa longa da configuração
    ciclos = int(config["ciclos"]) # Armazena o numero de ciclos da configuração
    print("Tempo de estudo: ",t_estudo,"\nPausa curta: ", pcurta ,"\nPausa longa: ", plonga ,"\n") # Imprime as configurações atuais
    if ciclos == 0: # se os ciclos forem 0
        ciclos = int(input("Numero de ciclos desejado: \n")) # Usuario insere o numero de ciclos desejado
    
    for i in range(ciclos): # Repete o ciclo o numero de vezes desejada
        for i in range(4): # Repete o ciclo de estudo e pausa curta 4 vezes
            print("Iniciando os estudos! Bons estudos.\n") # Imprime que iniciou o tempo de estudo
            somInicio.play() # Toca o som de inicio
            asy.run(timer(t_estudo)) # Cronometro do tempo de estudo
            tfinal = tfinal + t_estudo # Ao fim soma o tempo ao tempo final
            print("Pausa curta! Vá tomar uma agua ou ir no banheiro.\n") # Imprime que a pausa curta iniciou
            somCurto.play() #Toca o som de pausa curta
            asy.run(timer(pcurta)) # Cronometro da pausa curta 
        print("Pausa longa! Descanse um pouco.\n") # Imprime que a pausa longa iniciou
        somLongo.play() # Toca o som de pausa longa
    print("Parabéns você estudou: ",tfinal," Minutos") # Imprime o tempo estudado

    
def entrada(): # Funçao para alterar as configurações
    ntestudo = int(input("Tempo de estudo: \n")) # Lê o novo tempo de estudo
    npcurta = int(input("Tempo de pausa curta: \n")) # Lê o novo tempo de pausa curta
    nplonga = int(input("Tempoa de Pausa longa: \n")) # Lê o novo tempo de pausa longa
    nciclos = int(input("Numero de ciclos padrão(se deseja por ao inicializar digite 0): \n")) # Lê o novo numero de ciclos
    nconfig = { # Dicionario com as novas configurações
        "tempo_estudo" : ntestudo, 
        "pausa_curta" : npcurta,
        "pausa_longa" : nplonga,
        "ciclos": nciclos
    }
    config_obj = json.dumps(nconfig, indent=4) # Gera o objeto com o json e sua identação
    with open("config.json", "w") as outfile: # Abre o arquivo para ser escrito
        outfile.write(config_obj) # Escreve no arquivo
    pomodoro() # Inicia o pomodoro com as novas configurações


print("Deseja usar o tempo padrão ou personalizar?\n1 - Padrão\t 2 - Personalizar \t3 - para encerrar") # Menu das opções
op = int(input("Opção: ")) # Lê a opção desejada


match op: # Match/Switch que alterna entre as opção escolhida
    case 1: # caso digitado 1
        pomodoro() # Inicia o pomodoro
    case 2: # caso digitado 2
        entrada() # Inicia a requisição da nova configuração e posteriormente o pomodoro atualizado
    case _: # caso outro numero
        exit() # encerra