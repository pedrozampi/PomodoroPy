import json # Permite as configurações serem salvas.
import asyncio as asy # Permite o cronomêtro dos intervalos.
import pygame # Integração de som aos intervalos


pygame.mixer.init() #Inicia o módulo mixer da Biblioteca PyGame

somInicio = pygame.mixer.Sound('sounds/start.mp3') # Som de inicio do pomodoro.
somCurto = pygame.mixer.Sound('sounds/pauses.mp3') # Som da pausa curta.
somLongo = pygame.mixer.Sound('sounds/pausel.mp3') # Som da pausa longa.

somInicio.set_volume(0.1) # Deixa o volume do som em 10%
somCurto.set_volume(0.2) # Deixa o volume do som em 20%
somLongo.set_volume(0.2) # Deixa o volume do som em 20%


def carregar():
    r = open('config.json') # Abre a configuração
    global config
    config =  json.load(r) # Armazena os dados no dicionario config



async def timer(t): # A função Assíncrona do cronometro 
    await asy.sleep(t*60)   # O cronometro com o tempo em minutos multiplicadado para segundos

def tempototal(t):
    carregar()
    tempot = int(config["tempo_total"])
    ntestudo = int(config["tempo_estudo"])
    npcurta = int(config["pausa_curta"])
    nplonga = int(config["pausa_longa"])
    nciclos = int(config["tempo_total"])
    ntempo = { # Dicionario com as novas configurações
        "tempo_estudo" : ntestudo, 
        "pausa_curta" : npcurta,
        "pausa_longa" : nplonga,
        "ciclos": nciclos,
        "tempo_total" : tempot+t 
    }
    config_obj = json.dumps(ntempo, indent=4) # Gera o objeto com o json e sua identação
    with open("config.json", "w") as outfile: # Abre o arquivo para ser escrito
        outfile.write(config_obj)

def limpart():
    carregar()
    ntestudo = int(config["tempo_estudo"])
    npcurta = int(config["pausa_curta"])
    nplonga = int(config["pausa_longa"])
    nciclos = int(config["tempo_total"])
    ntempo = { # Dicionario com as novas configurações
        "tempo_estudo" : ntestudo, 
        "pausa_curta" : npcurta,
        "pausa_longa" : nplonga,
        "ciclos": nciclos,
        "tempo_total" : 0 
    }
    config_obj = json.dumps(ntempo, indent=4) # Gera o objeto com o json e sua identação
    with open("config.json", "w") as outfile: # Abre o arquivo para ser escrito
        outfile.write(config_obj)
    print("Tempo zerado.\n")


tfinal = 1 # Contar o tempo estudado

def pomodoro(): # Função do pomodoro
    carregar()
    global tfinal
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
    tempototal(tfinal)

    
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

carregar()
print("Você já estudou ",config["tempo_total"],"minutos no total\n")
print("Deseja usar o tempo padrão ou personalizar?\n1 - Padrão\t2 - Personalizar \t3 - Zerar tempo total\t4 - para encerrar") # Menu das opções
op = int(input("Opção: ")) # Lê a opção desejada


match op: # Match/Switch que alterna entre as opção escolhida
    case 1: # caso digitado 1
        pomodoro() # Inicia o pomodoro
    case 2: # caso digitado 2
        entrada() # Inicia a requisição da nova configuração e posteriormente o pomodoro atualizado
    case 3:
        limpart()
    case _: # caso outro numero
        exit() # encerra