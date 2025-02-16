from cte import *

##### CAMBIO DE COLORES #####
color_puerta = rojo_t # (...)_t -> indica transparencia

flecha_izq = gris_t
flecha_der = gris_t
flecha_atr = gris_t
puerta_del = gris_t

flecha_izq_visible = True
flecha_der_visible = True
flecha_atr_visible = True # SIEMPRE SE PODRÁ IR HACIA ATRÁS -> SIEMPRE SERÁ TRUE
puerta_del_visible = True

movimiento = 0 # define el tipo de movimiento del jugador -> N/S/E/O
jdung_tipo = 0 # define el elemento de la lista de sprites del jugador

##### TAMAÑOS SPRITES #####
tam_jugx = 120 * 2
tam_jugy = 60 * 2
tam_enemx = 549 * 2
tam_enemy = 60 * 2

class JugDungeon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = pygame.transform.scale(pygame.image.load('escenario/prueba.png').convert_alpha(),(tam_jugy,tam_jugy))
        self.image.blit(jugador_dung[jdung_tipo] ,(40,0),pygame.Rect(conteo_Msegundo%2 * 167, 0, tam_jugx, tam_jugy))


        self.rect = self.image.get_rect() 
        self.rect.center = (0,0) # Posición Inicial del centro del rectángulo obtenido


    def update(self): 
        global movimiento, posicion_act, tamaño_mapa

    
        if tamaño_mapa[0] == 5 and tamaño_mapa[1] == 5:
            if movimiento == 1:
                self.rect.y -= 120
            if movimiento == 2:
                self.rect.x += 120
            if movimiento == 3:
                self.rect.y += 120
            if movimiento == 4:
                self.rect.x -= 120
        

        self.image = pygame.transform.scale(pygame.image.load('escenario/prueba.png').convert_alpha(),(tam_jugy,tam_jugy)) 
        self.image.blit(jugador_dung[jdung_tipo] ,(40,0),pygame.Rect(conteo_Msegundo%2 * 167, 0, tam_jugx, tam_jugy))
        
        if tamaño_mapa[0] == 5 and tamaño_mapa[1] == 5:
            self.rect = self.image.get_rect()   
            self.rect.center = (posicion_act[2]*120 + 145, posicion_act[1]*120+60)
        
        elif tamaño_mapa[0] == 5 and tamaño_mapa[1] == 7:
            self.rect = self.image.get_rect()
            self.rect.center = (posicion_act[2]*115 + 40 , posicion_act[1]*115+60)
        
        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 5:
            self.rect = self.image.get_rect()
            self.rect.center = (posicion_act[2]*86 + 220 , posicion_act[1]*86+25)

        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 7:
            self.rect = self.image.get_rect()
            self.rect.center = (posicion_act[2]*86 + 120 , posicion_act[1]*86+25)

class EnemDungeon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('escenario/prueba.png').convert_alpha(),(tam_enemy,tam_enemy))
        self.image.blit(enemigo_dung ,(-20,0),pygame.Rect(conteo_Msegundo%6 * 192, 0, tam_enemx, tam_enemy))


        self.rect = self.image.get_rect() 
        self.rect.center = (0,0) # Posición Inicial del centro del rectángulo obtenido


    def update(self): 
        global movimiento, posicion_act

        self.image = pygame.transform.scale(pygame.image.load('escenario/prueba.png').convert_alpha(),(tam_enemy,tam_enemy))
        self.image.blit(enemigo_dung ,(-20,0),pygame.Rect(conteo_animacion%6 * 192, 0, tam_enemx, tam_enemy))
        if tamaño_mapa[0] == 5 and tamaño_mapa[1] == 5:
            self.rect = self.image.get_rect() 
            self.rect.center = (posicion_act[4]*120+140,posicion_act[3]*120+55) # PROBLEMA: X = COLUMNAS, Y = FILAS

        elif tamaño_mapa[0] == 5 and tamaño_mapa[1] == 7:
            self.rect = self.image.get_rect() 
            self.rect.center = (posicion_act[4]*120 + 15,posicion_act[3]*120+55)

        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 5:
            self.rect = self.image.get_rect()
            self.rect.center = (posicion_act[4] * 86 + 220,posicion_act[3]* 83 + 35)

        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 7:
            self.rect = self.image.get_rect()
            self.rect.center = (posicion_act[4] * 86 + 120,posicion_act[3]* 83 + 35)

######################################## DUNGEONS ########################################
texto_inicio = 'FILAS'
desplazamiento = 0 # nos servirá cuando texto_incio = 'COLUMNAS'

elegir = 0 # define si elige FILAS o COLUMNAS

filas = 0 # cuántas filas jugará
columnas = 0 # cuántas columnas jugará

tamaño_mapa = [] # uso en funciones -> tomará los valores de [filas,columnas]
ver_mapa = 1 # impar -> mapa invisible, par -> mapa visible

mirando = 'norte' # definimos para donde está mirando el jugador
mirando_conf = False # pos_obj[5]. False -> mirando hacia una pared, True -> puede moverse a donde indique

mapa5x5 = pygame.image.load('dungeon/baldosas 5x5.png').convert()
mapa5x7 = pygame.image.load('dungeon/baldosas 5x7.png').convert()
mapa7x5 = pygame.image.load('dungeon/baldosas 7x5.png').convert()
mapa7x7 = pygame.image.load('dungeon/baldosas 7x7.png').convert()
menu_dungeon = pygame.image.load('dungeon/menu_dungeon.png').convert()

jugador_dung = [pygame.transform.scale(pygame.image.load('dungeon/JF.png').convert_alpha(),(tam_jugx,tam_jugy)),
    pygame.transform.scale(pygame.image.load('dungeon/JE.png').convert_alpha(),(tam_jugx,tam_jugy)),
    pygame.transform.scale(pygame.image.load('dungeon/JD.png').convert_alpha(),(tam_jugx,tam_jugy)),
    pygame.transform.scale(pygame.image.load('dungeon/JI.png').convert_alpha(),(tam_jugx,tam_jugy))]

enemigo_dung = pygame.transform.scale(pygame.image.load('dungeon/ED.png').convert_alpha(),(tam_enemx,tam_enemy))

mapa_dungeon = [pygame.image.load('dungeon/mazmorras/c0.png').convert(),
                pygame.image.load('dungeon/mazmorras/c1.png').convert(),
                pygame.image.load('dungeon/mazmorras/c2.png').convert(),
                pygame.image.load('dungeon/mazmorras/c3.png').convert(),
                pygame.image.load('dungeon/mazmorras/c4.png').convert()]
                
ed1 = pygame.image.load('dungeon/mazmorras/ed1.png').convert()
ed2 = pygame.image.load('dungeon/mazmorras/ed2.png').convert()
ei1 = pygame.image.load('dungeon/mazmorras/ei1.png').convert()
ei2 = pygame.image.load('dungeon/mazmorras/ei2.png').convert()

pi1 = pygame.image.load('dungeon/mazmorras/pi1.png').convert()
pd1 = pygame.image.load('dungeon/mazmorras/pd1.png').convert()
pa1 = pygame.image.load('dungeon/mazmorras/pa1.png').convert()
pb1 = pygame.image.load('dungeon/mazmorras/pb1.png').convert()

s1 = pygame.image.load('dungeon/mazmorras/s1.png').convert()

pdf1 = pygame.image.load('dungeon/mazmorras/pdf1.png').convert()

good_ending = pygame.image.load('dungeon/good_ending.png').convert()
bad_ending = pygame.image.load('dungeon/bad_ending.png').convert()

random_dung = random.randint(0,len(mapa_dungeon)-1)
mazmorra = mapa_dungeon[random_dung]

dung_final = good_ending

def animar(sprite):
    global xo, yo, conteo_animar
    if conteo_animar == 0:
        xo += 1.001
        yo += 1.001
        sprite_animado = pg.transform.scale(sprite,(xo,yo))
        pantalla.blit(sprite_animado,((600 * (8/6) - xo)/2,(600-yo)/(7/4)))
    elif conteo_animar == 1:
        xo -= 1
        yo -= 1
        sprite_animado = pg.transform.scale(sprite,(xo,yo))
        pantalla.blit(sprite_animado,((600 * (8/6) - xo)/2,(600-yo)/(7/4)))
    else:
        sprite_animado = pg.transform.scale(sprite,(xo,yo))
        pantalla.blit(sprite_animado,((600 * (8/6) - xo)/2,(600-yo)/(7/4)))
        conteo_animar = 0
            
def genPos(mapa):
    global mirando_conf
    centro = [0,0]
###### GENERACIÓN DE POSICIÓN DEL JUGADOR ######
    # DEFINIMOS CENTRO SEGÚN EN TAMAÑO DEL MAPA

    centro[0] = (mapa[0] // 2) + 1 - 1 # EL -1 ME FALTÓ EN EL EXAMEN, SE PONE -1 DEBIDO A QUE TRABAJO CON LISTAS
    centro[1] = (mapa[1] // 2) + 1 - 1
    print(centro)
        
    fila_jug = random.randint(0,mapa[0]-1)    # DEBERIA SER DEL 0 A MAPA - 1 - FALLO EXAMEN
    columna_jug = random.randint(0,mapa[1]-1)
    
    # COMO NO PUEDE SPAWNEAR EN EL CENTRO:
    while fila_jug == centro[0] or columna_jug == centro[1] :
        fila_jug = random.randint(0,mapa[0]-1)
        columna_jug = random.randint(0,mapa[1]-1)
        
###### GENERACIÓN DE POSICIÓN DEL MONSTRUO ######
    fila_mon = random.randint(0,mapa[0]-1)
    columna_mon = random.randint(0,mapa[1]-1)
    
    # COMO NO PUEDE SPAWNEAR EN EL CENTRO:
    while fila_mon == centro[0] or columna_mon == centro[1] or fila_mon == fila_jug or columna_mon == columna_jug:    
        fila_mon = random.randint(0,mapa[0]-1)
        columna_mon = random.randint(0,mapa[1]-1)    
     
    posicion_obj = [centro,fila_jug,columna_jug,fila_mon,columna_mon,mirando_conf]    
    # 0: CENTRO, 1:Xjug, 2:Yjug, 3:Xmon, 4:Ymon
    # 0.0 X, 0.1 Y
    return posicion_obj

def comprobar(pos_obj): # ES NECESARIO QUE SE ESTÉ ACTUALIZANDO LA POS
    global locate, dung_final
    if pos_obj[1] == pos_obj[3] and pos_obj[2] == pos_obj[4]: # SI EL JUGADOR SE ENCUENTRA AL ENEMIGO
        dung_final = bad_ending
        locate = 9
    elif pos_obj[1] == pos_obj[0][0] and pos_obj[2] == pos_obj[0][1]:
        dung_final = good_ending
        locate = 9        
        
def mueve(pos_obj,mapa, movimiento):
    global mirando_conf
     ### EN EL EXAMEN DEFINÍ MAL LAS COORDENADAS PARA DÓNDE SE MUEVE ###
    if movimiento == 1:
        if pos_obj[1] == 0:
            print('Fuera de límites')
            pos_obj[5] = False
        else:
            pos_obj[1] -= 1
            movimiento = 0
            pos_obj[5] = True            
    
    elif movimiento == 3:
        if pos_obj[1] == (mapa[0]-1): #mapa[0] = filas
            print('Fuera de límites')
            pos_obj[5] = False
        else:
            pos_obj[1] += 1
            movimiento = 0
            pos_obj[5] = True
    
    elif movimiento == 2: # este = derecha
        if pos_obj[2] == (mapa[1]-1): #mapa[0] = columnas
            print('Fuera de límites')
            pos_obj[5] = False
        else:
            pos_obj[2] += 1
            movimiento = 0
            pos_obj[5] = True
    elif movimiento == 4:
        if pos_obj[2] == 0:
            print('Fuera de límites')
            pos_obj[5] = False
        else:
            pos_obj[2] -=1
            movimiento = 0
            pos_obj[5] = True

    return pos_obj
  
def change_score():
    pass   

        JugDG = pg.sprite.Group()
        EnemDG = pg.sprite.Group()
    
        JD = JugDungeon()
JugDG.add(JD)
ED = EnemDungeon()
EnemDG.add(ED)

        

################################################################################################################
#                                 SPS DUNGEON ------ SELECCIÓN AJUSTES PARTIDA                                 #
################################################################################################################    
    elif locate == 6:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejecutando = False
            if event.type == pg.MOUSEBUTTONDOWN  and event.button==1: # CLICK IZQUIERDO ->
                mouse_pos = pg.mouse.get_pos() # Obtener posición del cursor           
                if elegir == 0: # Elegir = 0 -> elegir filas
                    if 140 < mouse_pos[0] < 280 and 0 < mouse_pos[1] < 520: # Si se presiona el polígono izq(5)
                        texto_inicio = 'COLUMNAS'
                        desplazamiento = 35 # Desplazamiento para centrar el nuevo texto 'COLUMNAS'
                        filas = 5 # Establecemos 5 filas
                        elegir += 1 # Elegir = 1 -> elegir columnas

                    elif 540 < mouse_pos[0] < 680 and 0 < mouse_pos[1] < 520:
                        texto_inicio = 'COLUMNAS'
                        desplazamiento = 35
                        filas = 7 # Establecer 7 filas
                        elegir += 1
                    
                elif elegir == 1:
                    if 140 < mouse_pos[0] < 280 and 0 < mouse_pos[1] < 520:
                        #texto_inicio = '' # ¿necesario?
                        desplazamiento = 0 # Reinicio del desplazamiento
                        columnas = 5
                        tamaño_mapa = [filas,columnas] # Establecemos la variable según las dimensiones elegidas para el mapa

                        posicion_objetos = genPos(tamaño_mapa) # generación posiciones iniciales (posicion_objetos)
                        posicion_act = mueve(posicion_objetos,tamaño_mapa,movimiento) # primera actualización de posiciones (posicion_act)

                        if ver_mapa % 2 == 0: # Ver mapa -> define según el usuario elige si se ejecuta ...
                            locate = 7 # ... el juego con opción de visuallizar la posición de jugador y enemigo o ...                        
                        else:
                            locate = 8 # ... el juego sin conocer las posiciones y viendo tan solo mazmorras.

                    elif 540 < mouse_pos[0] < 680 and 0 < mouse_pos[1] < 520:
                        texto_inicio = ''
                        desplazamiento = 0
                        columnas = 7
                        tamaño_mapa = [filas,columnas]

                        posicion_objetos = genPos(tamaño_mapa) # GENERAMOS LAS POSICIONES INICIALES
                        posicion_act = mueve(posicion_objetos,tamaño_mapa,movimiento)
                        
                        if ver_mapa % 2 == 0:
                            locate = 7
                        else:
                            locate = 8

                if 360 < mouse_pos[0] < 450 and 200 < mouse_pos[1] < 330: # Si se hace click en la puerta de (visualizar_mapa)
                    if ver_mapa % 2 == 0:
                        color_puerta = rojo_t # Rojo indica -> no visualizar mapa
                    else:
                        color_puerta = verde_t # Verde -> visualizar mapa
                    ver_mapa += 1 # Dado que trabajamos con números pares o impares (n + 1)
                    print(ver_mapa)

    ############ OBTENEMOS LA POSICIÓN DEL CURSOR EN CADA MOMENTO ############
        mouse_pos2 = pg.mouse.get_pos()

        ### DETALLE CURSOR SELECCIONANDO FILAS/COLUMNAS, SÍ/NO MOSTRAR MAPA ###
        if 140 < mouse_pos2[0] < 280 and 0 < mouse_pos2[1] < 520:
            pg.draw.polygon(pantalla, BLANCO, ((140, 0), (140, 520), (280, 385), (280, 80)),5) # Polígono izq (5)
        elif 540 < mouse_pos2[0] < 680 and 0 < mouse_pos2[1] < 520:
            pg.draw.polygon(pantalla, BLANCO, ((680, 0), (680, 520), (540, 385), (540, 80)),5) # Polígono der (7)      
        elif 360 < mouse_pos2[0] < 450 and 200 < mouse_pos2[1] < 330:
            pg.draw.rect(pantalla, BLANCO, (360,200,90,130),2) # Puerta (VER MAPA)

        ############### DIBUJO DE FIGURAS Y TEXTOS ###############
        superficie_poligono = pg.Surface((ANCHO, ALTO), pg.SRCALPHA) # CREAMOS UNA SUPERFICIE CON OPACIDAD (SRCALPHA)
        pg.draw.polygon(superficie_poligono, azul_t, ((140, 0), (140, 520), (280, 385), (280, 80))) # DIBUJAMOS SOBRE ESTA SUPERFICIE
        pg.draw.polygon(superficie_poligono, lila_t, ((680, 0), (680, 520), (540, 385), (540, 80)))
        pg.draw.rect(superficie_poligono, color_puerta, (360,200,90,130))        

        # Usamos 'desplazamiento' porque el texto de columnas es más largo que el de filas -> CENTRAR TEXTO
        muestra_texto(pantalla,str(texto_inicio),NEGRO, 373-desplazamiento,170,'fuentes/medieval2.ttf',30) 
        muestra_texto(pantalla,str(texto_inicio),BLANCO, 370-desplazamiento,170,'fuentes/medieval2.ttf',30)
        
        muestra_texto(pantalla,'5',BLANCO,200,210,'fuentes/medieval.ttf',50)
        muestra_texto(pantalla,'7',BLANCO,600,210,'fuentes/medieval.ttf',50)

        temporizador() # Actualiza los sprites sheets de los juegos        
        pg.display.flip()
        pantalla.blit(menu_dungeon,(0,0))
        pantalla.blit(superficie_poligono, (0, 0)) # AÑADIR A LA PANTALLA LA SUPERFICIE CON OPACIDAD

################################################################################################################
#                                    SPS DUNGEON ------ MODO MAPA VISIBLE                                      #
################################################################################################################
    elif locate == 7:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejecutando = False
        ################ MOVIMIENTO SEGÚN LA TECLA PRESIONADA ################
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    movimiento = 4
                    jdung_tipo = 3 # SPRITE PERSONAJE MIRANDO OESTE
                elif event.key == pg.K_d:
                    movimiento = 2
                    jdung_tipo = 2 # SPRITE PERSONAJE MIRANDO ESTE
                elif event.key == pg.K_w:
                    movimiento = 1
                    jdung_tipo = 1 # SPRITE PERSONAJE MIRANDO SUR
                elif event.key == pg.K_s:
                    movimiento = 3
                    jdung_tipo = 0 # SPRITE PERSONAJE MIRANDO NORTE
            
        ################ RETURN DE POSICION ACTUAL DEL JUGADOR EN CADA MOVIMIENTO ################
                posicion_act = mueve(posicion_act,tamaño_mapa,movimiento) # actualiza la posición todo el rato que se mueve
                comprobar(posicion_act)

    ################### CARGA DE FONDO DEPENDIENDO DEL MAPA ELEGIDO ###################    
        if tamaño_mapa[0] == 5 and tamaño_mapa[1] == 5:
            pantalla.blit(pg.image.load('dungeon/fb 5x5.png').convert(),(0,0))
            pantalla.blit(mapa5x5,(100,0))
        elif tamaño_mapa[0] == 5 and tamaño_mapa[1] == 7:
            pantalla.blit(pg.image.load('dungeon/fb 5x7.png').convert(),(0,0))
            pantalla.blit(mapa5x7,(0,15))
        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 5:
            pantalla.blit(pg.image.load('dungeon/fb 7x5.png').convert(),(13,0))
            pantalla.blit(mapa7x5,(200,0))
        elif tamaño_mapa[0] == 7 and tamaño_mapa[1] == 7:
            pantalla.blit(pg.image.load('dungeon/fb 7x7.png').convert(),(0,0))
            pantalla.blit(mapa7x7,(100,0))
    ###################################################################################

        ### DIBUJO Y ACTUALIZACIÓN DE CLASES ###
        JugDG.update()
        JugDG.draw(pantalla)
        EnemDG.update()
        EnemDG.draw(pantalla)     

        temporizador() # ACTUALIZA LOS SPRITES SHEETS DE TODOS LOS JUEGOS
        pg.display.flip()        
        #movimiento = 0 # LA FUNCIÓN MUEVE() YA INCLUYE ESTE REINICIO

################################################################################################################
#                                    SPS DUNGEON ------ MODO MAPA INVISIBLE                                      #
################################################################################################################        
    elif locate == 8:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejecutando = False            
            if event.type == pg.MOUSEBUTTONDOWN  and event.button==1: # CUANDO SE HACE CLICK IZQUIERDO
                mouse_pos = pg.mouse.get_pos()

                ######################### MOVIMIENTO - NORTE #########################
                if 372 < mouse_pos2[0] < 425 and 405 < mouse_pos2[1] < 445:
                    if mirando == 'norte':
                        movimiento = 1 
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]: # pos_act[5] -> comprueba que el movimiento es válido y no hay ninguna pared (VALOR BOOLEANO)
                            mirando = 'norte' # si no hay pared y se permite (True) -> establece mirando y genera un número aleatorio ...   
                            random_dung = random.randint(0,len(mapa_dungeon)-1) # ... este número establece el fondo de la nueva mazmorra

                    elif mirando == 'este':
                        movimiento = 2
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'este'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)
                    elif mirando == 'sur':
                        movimiento = 3
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'sur'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)
                    elif mirando == 'oeste':
                        movimiento = 4
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'oeste'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)            

                ######################### MOVIMIENTO - ESTE #########################
                elif 598 < mouse_pos2[0] < 660 and 510 < mouse_pos2[1] < 540:          
                    if mirando == 'norte':
                        movimiento = 2 
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'este'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)                      
                    elif mirando == 'este':
                        movimiento = 3
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'sur'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'sur':
                        movimiento = 4
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'oeste'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'oeste':
                        movimiento = 1
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'norte'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)                      

                ######################### MOVIMIENTO - SUR #########################
                elif 315 < mouse_pos2[0] < 440 and 545 < mouse_pos2[1] < 580:
                    if mirando == 'norte':
                        movimiento = 3 
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'sur'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'sur':
                        movimiento = 1
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'norte'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'este':
                        movimiento = 4
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'oeste'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'oeste':
                        movimiento = 2
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'este'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  

                ######################### MOVIMIENTO - OESTE #########################
                elif 50 < mouse_pos2[0] < 115 and 475 < mouse_pos2[1] < 505:
                    if mirando == 'norte':
                        movimiento = 4 
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'oeste'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'oeste':
                        movimiento = 3
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'sur'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'sur':
                        movimiento = 2
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'este'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  
                    elif mirando == 'este':
                        movimiento = 1
                        posicion_act = mueve(posicion_act,tamaño_mapa,movimiento)
                        comprobar(posicion_act)
                        if posicion_act[5]:
                            mirando = 'norte'
                            random_dung = random.randint(0,len(mapa_dungeon)-1)  

################# OBTENER POSICIÓN DEL RATÓN EN CADA MOMENTO #################
        mouse_pos2 = pg.mouse.get_pos()


##########################################################################################
#          ESTABLECER MAZMORRA Y FLECHAS VISIBLES DEPENDIENDO DE 'MIRANDAO'              #
##########################################################################################
        
        if mirando == 'norte':
            if posicion_act[2] == 0 and posicion_act[1] == 0: # ESQUINA IZQ SUP
                mazmorra = ed2
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == 0: # PASILLO IZQUIERDO
                mazmorra = pi1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == tamaño_mapa[0] - 1 and posicion_act[1] == 0: #ESQUINA DER SUP
                mazmorra = ei1
                puerta_del_visible = False
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == tamaño_mapa[0] - 1: # PASILLO DERECHO
                mazmorra = pd1
                puerta_del_visible = True
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[1] == 0:
                mazmorra = pa1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = True
            elif posicion_act[2] == posicion_act[0][0] and posicion_act[1] == posicion_act[0][1] + 1 :
                mazmorra = s1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
            else:
                mazmorra = mapa_dungeon[random_dung]
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True

        elif mirando == 'sur':
            if posicion_act[2] == 0 and posicion_act[1] == tamaño_mapa[1] - 1: # ESQUINA IZQ INF
                mazmorra = ei1
                puerta_del_visible = False
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == 0: #PASILLO IZQUIERDO
                mazmorra = pd1
                puerta_del_visible = True
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == tamaño_mapa[0] - 1 and posicion_act[1] == tamaño_mapa[1] - 1: #ESQUINA DER INF
                mazmorra = ed1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == tamaño_mapa[0] - 1: # PASILLO DERECHO
                mazmorra = pi1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[1] == tamaño_mapa[1] - 1: # PASILLO INFERIOR
                mazmorra = pb1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = True
            elif posicion_act[2] == posicion_act[0][0] and posicion_act[1] == posicion_act[0][1] - 1:
                mazmorra = s1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
            else:
                mazmorra = mapa_dungeon[random_dung]
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
        
        elif mirando == 'este':
            if posicion_act[2] == tamaño_mapa[0] - 1 and posicion_act[1] == 0: #ESQUINA DER SUP
                mazmorra = ed2
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == tamaño_mapa[0] - 1 and posicion_act[1] == tamaño_mapa[1] - 1: #ESQUINA DER INF
                mazmorra = ei2
                puerta_del_visible = False
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == tamaño_mapa[0] - 1: # PASILLO DERECHO
                mazmorra = pdf1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = True
            elif posicion_act[1] == 0: # PASILLO SUPERIOR
                mazmorra = pi1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[1] == tamaño_mapa[1] - 1: # PASILLO INFERIOR
                mazmorra = pd1
                puerta_del_visible = True
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == posicion_act[0][0] - 1 and posicion_act[1] == posicion_act[0][1]: #PUERTA
                mazmorra = s1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
            else:
                mazmorra = mapa_dungeon[random_dung]
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
            
        elif mirando == 'oeste':
            if posicion_act[2] == 0 and posicion_act[1] == 0: # ESQUINA IZQ SUP
                mazmorra = ei2
                puerta_del_visible = False
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[2] == 0 and posicion_act[1] == tamaño_mapa[1] - 1: # ESQUINA IZQ INF
                mazmorra = ed1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == 0: #PASILLO IZQUIERDO
                mazmorra = pdf1
                puerta_del_visible = False
                flecha_der_visible = True
                flecha_izq_visible = True
            elif posicion_act[1] == 0: # PASILLO SUPERIOR
                mazmorra = pd1
                puerta_del_visible = True
                flecha_der_visible = False
                flecha_izq_visible = True
            elif posicion_act[1] == tamaño_mapa[1] - 1: # PASILLO INFERIOR
                mazmorra = pi1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = False
            elif posicion_act[2] == posicion_act[0][0] + 1 and posicion_act[1] == posicion_act[0][1]:
                mazmorra = s1
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True
            else:
                mazmorra = mapa_dungeon[random_dung]
                puerta_del_visible = True
                flecha_der_visible = True
                flecha_izq_visible = True

###################################################################################################################
#                                    CONFIGURACION DE COLORES DE FLECHAS                                          #
###################################################################################################################

        ################### RATÓN EN FLECHA DELANTERA ###################
        if 372 < mouse_pos2[0] < 425 and 405 < mouse_pos2[1] < 445:
            if puerta_del_visible:
                puerta_del = BLANCO # Si el ratón está en la flecha delantera y esta es visible, colorear de BLANCO
        else:
            if puerta_del_visible: # Si es visible pero el ratón no está en la flecha, colorear de gris_t
                puerta_del = gris_t    
        ################### RATÓN EN FLECHA IZQUIERDA ###################
        if 50 < mouse_pos2[0] < 115 and 475 < mouse_pos2[1] < 505: 
            if flecha_izq_visible:
                flecha_izq = BLANCO
        else:
            if flecha_izq_visible:
                flecha_izq = gris_t
        ################### RATÓN EN FLECHA DERECHA ###################
        if 598 < mouse_pos2[0] < 660 and 510 < mouse_pos2[1] < 540: 
            if flecha_der_visible:
                flecha_der = BLANCO
        else:
            if flecha_der_visible:
                flecha_der = gris_t
        ################### RATÓN EN FLECHA TRASERA ###################
        if 315 < mouse_pos2[0] < 440 and 545 < mouse_pos2[1] < 580: 
            flecha_atr = BLANCO
        else:
            flecha_atr = gris_t # No necesita else, siempre está visible

        ################### FLECHA NO VISIBLE = NO MOSTRAR (colorear de trans) ###################
        if not flecha_izq_visible:
            flecha_izq = trans
        if not flecha_der_visible:
            flecha_der = trans
        if not puerta_del_visible:
            puerta_del = trans

#################################################################################################
#                         FIN COORDENADAS Y FLECHAS DEL MODO MAZMORRAS                          #
#                                                                                               #
#-----------------------------------------------------------------------------------------------#
#                                                                                               #
#                                DIBUJO DE FLECHAS Y MÁS FIGURAS                                #
#################################################################################################

        superficie_poligono = pg.Surface((ANCHO, ALTO), pg.SRCALPHA) # SUPERFICIE CON TRANSPARENCIA
        
        #### DIBUJO DE FLECHS ####
        muestra_texto(superficie_poligono, 'Volver atras',flecha_atr,320,550,'fuentes/medieval2.ttf', 30 )
        pg.draw.polygon(superficie_poligono, flecha_izq, ((50,490), (93,477), (77,489),(114,489),(108,495),(73,495),(60,505)))
        pg.draw.polygon(superficie_poligono, flecha_der,  ((596,522),(628,522),(620,510),(658,523),(638,539),(630,529),(600,528)))
        pg.draw.polygon(superficie_poligono, puerta_del,  ((410,405),(425,420),(410,420),(396,445),(372,445),(389,420),(373,420)))

        ### DIBUJO Y ACTUALIZACIÓN DE CLASES ###
        JugDG.update()
        JugDG.draw(pantalla)
        EnemDG.update()
        EnemDG.draw(pantalla) 

        pg.display.flip() # ACTUALIZACIÓN DE PANTALLA
        
        pantalla.blit(mazmorra,(0,0)) # MOSTRAMOS EL FONDO ...
        pantalla.blit(superficie_poligono, (0, 0)) # ... Y ENCIMA LA SUPERFICIE TRANSPARENTE

###################################################################################################################
#                                  FIN DE PARTIDA - VOLVER A JUGAR / SALIR                                        #
###################################################################################################################
    elif locate == 9:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ejecutando = False
            if event.type == pg.MOUSEBUTTONDOWN  and event.button==1:
                mouse_pos = pg.mouse.get_pos()
                if 200 < mouse_pos2[0] < 350 and 280 < mouse_pos2[1] < 350: #BOTÓN JUGAR
                    locate = 6 # VOLVER A LA CONFIGURACIÓN DE LA PARTIDA
                    elegir = 0
                    filas = 0
                    columnas = 0
                    texto_inicio = 'FILAS'
                    jdung_tipo = 0
                elif 450 < mouse_pos2[0] < 600 and 280 < mouse_pos2[1] < 350: #BOTÓN SALIR
                    locate = 0 # VOLVER AL MENÚ SPS CLOUD
                    elegir = 0
                    filas = 0
                    columnas = 0
                    texto_inicio = 'FILAS'
                    jdung_tipo = 0

        superficie_poligono = pg.Surface((ANCHO, ALTO), pg.SRCALPHA) # SUPERFICIE CON TRANSPARENCIA

        puerta_del = gris_t # Tiene que ir antes del if // Uso 'puerta_del' para reutilizar variables...
        flecha_atr = gris_t # ...debido a que puerta_del' no se está usando.
        flecha_der = gris_t
        flecha_izq = gris_t
        
        mouse_pos2 = pg.mouse.get_pos()

        if 200 < mouse_pos2[0] < 350 and 280 < mouse_pos2[1] < 350: # BOTÓN JUGAR
            puerta_del = BLANCO
            flecha_atr = AMARILLO
        if 450 < mouse_pos2[0] < 600 and 280 < mouse_pos2[1] < 350: #BOTOÓN SALIR
            flecha_izq = BLANCO
            flecha_der = BLANCO
           
        pg.draw.rect(superficie_poligono,puerta_del,(200,280,150,70),1) # BOTÓN JUGAR        
        muestra_texto(superficie_poligono,'JUGAR',flecha_atr,226,302,'fuentes/medieval2.ttf',35)

        muestra_texto(superficie_poligono,'SALIR',flecha_der,480,302,'fuentes/medieval2.ttf',33) # BOTÓN SALIR
        pg.draw.rect(superficie_poligono,flecha_izq,(450,280,150,70),1)

        pg.display.flip()
        pantalla.blit(dung_final,(0,0))
        pantalla.blit(superficie_poligono,(0,0))
