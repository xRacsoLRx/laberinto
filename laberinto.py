import random
import threading
import time
import json

class MapElement:
    def __init__(self):
        pass

    def entrar(self, alguien):
        pass

    def print(self):
        print("MapElement")
    
    def esPuerta(self):
        return False
    
    def esHabitacion(self):
        return False

    def recorrer(self, unBloque):
        pass

    def abrir(self):
        pass

    def cerrar(self):
        pass

    def recorrer(self, unBloque):
        unBloque(self)

class Game:
    def __init__(self):
        self.maze = None
        self.bichos = []
        self.personaje=None
        self.gestorHilos = GestorHilos()

    def createWall(self):
        return Wall()
    
    def lanzarHilos(self):
        print("Los bichos se mueven")
        for bicho in self.bichos:
            self.gestorHilos.agregarHilo(bicho)
        self.gestorHilos.start()
    
    def pararHilos(self):
        print("Los bichos se paran")
        for bicho in self.bichos:
            bicho.vida=0
        self.gestorHilos.start()
      

    def createDoor(self, side1, side2):
        door = Door(side1, side2)
        door.side1 = side1
        door.side2 = side2
        return door

    def createRoom(self, id):
        room = Room(id)
        room.addOrientation(self.makeNorth())
        room.addOrientation(self.makeEast())
        room.addOrientation(self.makeSouth())
        room.addOrientation(self.makeWest())
        room.north=self.createWall()
        room.east=self.createWall()
        room.south=self.createWall()
        room.west=self.createWall()
        return Room(id) 

    def createMaze(self):
        return Maze()
    
    def makeNorth(self):
        return Norte().get_instance()

    def makeEast(self):
        return Este.get_instance()
    
    def makeSouth(self):
        return Sur().get_instance()
    
    def makeWest(self):
        return Oeste().get_instance()
    


    def create4Rooms4BeastsFM(self):
        self.maze = self.createMaze()
        
        room1 = self.createRoom(1)
        room2 = self.createRoom(2) 
        room3 = self.createRoom(3)
        room4 = self.createRoom(4)
        
        door12 = self.createDoor(room1, room2)
        door13 = self.createDoor(room1, room3)
        door24 = self.createDoor(room2, room4)
        door34 = self.createDoor(room3, room4)
        
        room1.south = door12
        room2.north = door12
        
        room1.east = door13 
        room3.west = door13

        room2.east = door24 
        room4.west = door24
        
        room3.south = door34
        room4.north = door34
        
        bicho1 = Bicho(1)
        bicho2 = Bicho(2)
        bicho3 = Bicho(3) 
        bicho4 = Bicho(4)

        bicho1 = self.makeAggressiveBeast(room1)
        bicho2 = self.makeLazyBeast(room2)  
        bicho3 = self.makeAggressiveBeast(room3)
        bicho4 = self.makeLazyBeast(room4)
        
        room1.add(bicho1)
        room2.add(bicho2)
        room3.add(bicho3)
        room4.add(bicho4)
        
        self.maze.addRoom(room1)
        self.maze.addRoom(room2)
        self.maze.addRoom(room3)
        self.maze.addRoom(room4)

        return self.maze

    def agregarPersonaje(self,name):
        self.personaje = Personaje(name)
        self.personaje.game=self
        self.maze.entrar(self.personaje)

    def agregarBicho(self, bicho):
        bicho.num=len(self.bichos)+1
        bicho.game=self
        self.bichos.append(bicho)        

    def eliminarBicho(self, bicho):
        self.bichos.remove(bicho)
    
    def makeAggressiveBeast(self,room):
        bicho= Bicho(Agresivo())
        bicho.poder = 5
        bicho.position=room
        return bicho
    
    def makeLazyBeast(self,room):
        bicho= Bicho(Perezoso())
        bicho.poder = 1
        bicho.position=room
        return bicho
    
    def print(self):
        print("Game")
    
    def encontrarPersonaje(self,unCont):
        if self.personaje.position ==unCont:
            return self.personaje
        else:
            return None
    
    def encontrarBicho(self,unCont):
        for bicho in self.bichos:
            if bicho.position == unCont:
                return bicho
        else:
            return None

    def make2RoomsMazeFM(self):
        self.maze = self.createMaze()
        room1 = self.createRoom(1)
        room2 = self.createRoom(2)
        door = self.createDoor(room1, room2)
        room1.south=door
        room2.north=door
        self.maze.addRoom(room1)
        self.maze.addRoom(room2)
        
        return self.maze
    
    def make2RoomsMaze(self):
        self.maze = Maze()
        room1 = Room(1)
        room2 = Room(2)
        self.maze.addRoom(room1)
        self.maze.addRoom(room2)

        door = Door(room1, room2)
        room1.south=door
        room2.north=door
        return self.maze
    
    def abrirPuertas(self):
        print("Abriendo todas las puertas")
        abrirPuertas=lambda each: each.open()
        self.maze.recorrer(abrirPuertas)

    def cerrarPuertas(self):
        print("Cerrando todas las puertas")
        cerrarPuertas=lambda each: each.close()
        self.maze.recorrer(cerrarPuertas)

class GestorHilos:
    def __init__(self):
        self.hilos = []
    
    def agregarHilo(self, bicho):
        hilo = threading.Thread(target=bicho.start)
        self.hilos.append(hilo)
        
    def start(self):
        for hilo in self.hilos:
            print("Iniciando hilo: ", hilo)
            hilo.start()
    def join(self):
        for hilo in self.hilos:
            print("Esperando a que termine el hilo: ", hilo)
            hilo.join()
    def stop(self):
        for hilo in self.hilos:
            print("Parando hilo: ", hilo)
            hilo.stop()

class Ente:
    def __init__(self):
        self.position = None
        self.game = None
        self.vida = None
        self.poder = None

    def irAlNorte(self):
        self.position.irAlNorte(self)

    def irAlSur(self):
        self.position.irAlSur(self)

    def irAlEste(self):
        self.position.irAlEste(self)

    def irAlOeste(self):
        self.position.irAlOeste(self)

    def findEnemy(self):
        pass

    def attack(self):
        enemy = self.findEnemy()
        if enemy:
            enemy.receiveAttack(self)
    def receiveAttack(self,attacker):
        pass

class Personaje(Ente):
    def __init__(self, name):
        super().__init__()
        self.vida = 20
        self.poder = 1
        self.name = name
    
    def __str__(self):
        return self.name
    def findEnemy(self):
        return self.game.findBicho(self.position)
    
    def isAttackedBy(self,enemy):
        self.vida = self.vida-enemy.poder
        print("Has sido atacado por "+str(enemy)+"\n")
        if self.vida <= 0:
            print("Has muerto")
            self.game.stopThreads()
        else:
            print("Te quedan "+str(self.vida)+" vidas")

class Bicho(Ente):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.poder = 2
        self.vida = 10
        self.num = 0
    def __str__(self):
        template = 'Bicho - {0.mode}{0.num}'
        return template.format(self)
    
    def esAgresivo(self):
        return self.mode.esAgresivo()
    
    def esPerezoso(self):
        return self.mode.esPerezoso()
    
    def actua(self):
        self.mode.actua(self)
    
    def caminaAleatorio(self):
        self.position.caminaAleatorio(self)
    
    def start(self):
        self.actua()

    def stop(self):
        print(self , " está parado")
        exit(0)

    def findEnemy(self):
        return self.game.encontrarPersonaje(self.position)
          
class Mode:
    def __init__(self):
        pass
    def esAgresivo(self):
        return False
    
    def esPerezoso(self):
        return False
    
    def act(self, bicho):
        while bicho.life > 0:
            self.duerme(bicho)
            self.camina(bicho)
            self.ataca(bicho)

    def camina(self, bicho):
        bicho.caminaAleatorio()

    def duerme(self, bicho):
        print(bicho," está durmiendo")
        time.sleep(5)
    def ataca(self,bicho):
        bicho.ataca()

class Agresivo(Mode):
    def __init__(self):
        super().__init__()
    
    def __str__(self):
        return "Agresivo"
    
    def esAgresivo(self):
        return True

    def print(self):
        print("bicho agresivo")

class Perezoso(Mode):
    def __init__(self):
        super().__init__()
    
    def __str__(self):    
        return "Perezoso"
    
    def print(self):
        print("bicho perezoso")

    def esPerezoso(self):
        return True

class Door(MapElement):
    def __init__(self, side1, side2):
        self.side1 = side1
        self.side2 = side2
        self.opened = False
    def entrar(self, alguien):
        if self.opened:
            if alguien.position == self.side1:
                self.side2.entrar(alguien)
            else:
                self.side1.entrar(alguien)
        else:
            print("La puerta "+str(self)+" está cerrada"+"\n")
    def __str__(self):
     return "Puerta-"+str(self.side1)+"-"+str(self.side2)
    
    def open(self):
        print("Abriendo la puerta "+str(self))
        self.opened = True
        
    def close(self):
        print("Cerrando la puerta "+str(self))
        self.opened = False

    def esPuerta(self):
        return True
        
class Wall(MapElement):
    def __init__(self):
        pass 
    def print(self):
        print("Wall")
    def entrar(self):
        print("No puedes atravesar paredes")

class BombedWall(Wall):
    def __init__(self):
        super().__init__()
        self.active = False

    def entrar(self):
        if self.active:
            print("La bomba ha explotado")
        else:
            return super().entrar()

class BombedGame(Game):
    def create_wall(self):
        return BombedWall()
    
    def print(self):
        print("BombedGame")

class Contenedor(MapElement):

    def __init__(self):
        super().__init__()
        self.Hijos = []
        self.num = None    
        self.forma = None 
        
    def agregarHijo(self, hijo):
        self.Hijos.append(hijo)
        
    def eliminarHijo(self, hijo):
        self.Hijos.remove(hijo)

    def caminarAleatorio(self,alguien):
        pass

    def agregarOrientacion(self, orientacion):
        #self.orientations.append(orientation)
        self.forma.agregarOrientacion(orientacion)
    
    def eliminarOrientacion(self, orientacion):
        #self.orientations.remove(orientation)
        self.forma.eliminarOrientacion(orientacion)

    def caminarAleatorio(self, ente):        
        orientacion = self.forma.getRandomOrientation()
        orientacion.caminarAleatorio(ente)
   
    def irAlNorte(self, alguien):
        self.forma.irAlNorte(alguien)
    def irAlEste(self, alguien):
        self.forma.irAlEste(alguien)
    def irAlSur(self, alguien):
        self.forma.irAlSur(alguien)
    def irAlOeste(self, alguien):
        self.forma.irAlOeste(alguien)
    def ponerElementoEn(self, em, orientacion):
        self.forma.ponerElementoEn(em, orientacion)
    
    def recorrer(self, unBloque):
        unBloque(self)
        for child in self.children:
            child.recorrer(unBloque)
        self.forma.recorrer(unBloque)

class Orientacion:
    def __init__(self) -> None:
        pass
    def caminarAleatorio(self, alguien):
        pass
    def ponerElementoEn(self, elemento, contenedor):
        pass
    def recorrerEn(self, unBloque, contenedor):
        pass

class Norte(Orientacion):
    _instance = None
    def __init__(self):
        if not Norte._instance:
            super().__init__()
            Norte._instance = self
    def ponerElementoEn(self, elemento, contenedor):
        contenedor.norte = elemento

    def get_instance(cls):
        if not cls._instance:
            cls._instance = Norte()
        return cls._instance

    def print(self):
        print("Norte")
    
    def caminarAleatorio(self, alguien):
        alguien.irAlNorte()

    def recorrerEn(self, unBloque, contenedor):
        contenedor.norte.recorrer(unBloque)
          

class Sur(Orientacion):
    _instance = None
    def __init__(self):
        if not Sur._instance:
            super().__init__()
            Sur._instance = self
    def ponerElementoEn(self, elemento, contenedor):
        contenedor.sur = elemento

    def get_instance(cls):
        if not cls._instance:
            cls._instance = Sur()
        return cls._instance

    def print(self):
        print("Sur")
    
    def caminarAleatorio(self, alguien):
        alguien.irAlSur()

    def recorrerEn(self, unBloque, contenedor):
        contenedor.norte.recorrer(unBloque)
          

class Este(Orientacion):
    _instance = None
    def __init__(self):
        if not Este._instance:
            super().__init__()
            Este._instance = self
    def ponerElementoEn(self, elemento, contenedor):
        contenedor.este = elemento

    def get_instance(cls):
        if not cls._instance:
            cls._instance = Este()
        return cls._instance

    def print(self):
        print("Este")
    
    def caminarAleatorio(self, alguien):
        alguien.irAlEste()

    def recorrerEn(self, unBloque, contenedor):
        contenedor.este.recorrer(unBloque)
          

class Oeste(Orientacion):
    _instance = None
    def __init__(self):
        if not Oeste._instance:
            super().__init__()
            Oeste._instance = self
    def ponerElementoEn(self, elemento, contenedor):
        contenedor.este = elemento

    def get_instance(cls):
        if not cls._instance:
            cls._instance = Oeste()
        return cls._instance

    def print(self):
        print("Oeste")
    
    def caminarAleatorio(self, alguien):
        alguien.irAlOeste()

    def recorrerEn(self, unBloque, contenedor):
        contenedor.oeste.recorrer(unBloque)

class Hoja(MapElement):
    def __init__(self):
        super().__init__()
    
    def print(self):
        print("Leaf")

class Decorator(Hoja):
    def __init__(self):
        super().__init__()
        self.component = None
    
    def print(self):
        print("Decorator")

class Bomba(Decorator):
    def __init__(self):
        super().__init__()
        self.activa = False
    
    def print(self):
        print("Bomba")
    
    def entrar(self, alguien):
        print(alguien + "caminó hacia la bomba")

class Maze(Contenedor):
    def __init__(self):
        super().__init__()
    def addRoom(self, room):
        self.agregarHijo(room)
    def entrar(self, alguien):
        self.Hijos[0].entrar(alguien)
    def print(self):
        print("Maze") 
    def obtenerHabitaciones(self, num):
        for room in self.Hijos:
            if room.num == num:
                return room
        return None
    def recorrer(self, unBloque):
        unBloque(self)
        for hijo in self.Hijos:
            hijo.recorrer(unBloque)

class Room(Contenedor):
    def __init__(self, num):
        super().__init__()
        self.num = num

    def entrar(self, alguien):
        print(str(alguien) + " entra a la habitación " 
              + str(self.num)+"\n")
        alguien.position=self
    def esHabitacion(self):
        return True
    def print(self):
        print("Room")

    def __str__(self):
        return "Hab -" + str(self.num)+"\n"
    def obtenerOrientaciones(self):
        return self.forma.orientaciones
    
class Forma:
    def __init__(self):
        self.orientaciones = []
    
    def agregarOrientacion(self, orientacion):
        self.orientaciones.append(orientacion)
    
    def eliminarOrientacion(self, orientacion):
        self.orientaciones.remove(orientacion)
    
    def obtenerDireccionAleatoria(self):
        return random.choice(self.orientaciones)
    
    def ponerElementoEn(self, elemento, orientacion):
        orientacion.ponerElementoEn(elemento, self)
    
    def recorrer(self, bloque):
        for orientacion in self.orientaciones:
            orientacion.recorrerEn(bloque, self)

class Rectangle(Forma):
    def __init__(self):
        super().__init__()
        self.norte = None
        self.sur = None
        self.este = None
        self.oeste = None
    def irAlNorte(self, alguien):
        self.norte.entrar(alguien)
    def irAlEste(self, alguien):
        self.este.entrar(alguien)
    def irAlSur(self, alguien):
        self.sur.entrar(alguien)
    def irAlOeste(self, alguien):
        self.oeste.entrar(alguien)

class Director:
    def __init__(self):
        self.dict=None
        self.builder=LaberintoBuilder()
    
    def procesar(self, filename):
        self.leer_archivo(filename)
        self.crear_laberinto()
        self.crear_juego()
        self.crear_bichos()

    def leer_archivo(self, filename):
        try:
            with open(filename) as f:
                data = json.load(f)
                self.dict= data
        except FileNotFoundError:
            print(f"Archivo {filename} no existe")
            return None
        
    def crear_laberinto(self):
       self.builder.makeMaze(self)

    def crear_juego(self):
       self.builder.makeGame(self)
       
       for each in self.dict['maze']:
           self.crear_laberinto_recursivo(each, 'root')
       for each in self.dict['doors']:
           n1 = each[0]
           or1 = each[1]
           n2 = each[2]
           or2 = each[3]
           self.builder.makeDoor(n1, or1, n2, or2)

    def crear_laberinto_recursivo(self, un_dic, padre):
    
        if un_dic['tipo'] == 'room':
            con = self.builder.makeRoom(un_dic['num'])
            
        if un_dic['tipo'] == 'bomb':
            self.builder.makeBombIn(padre)
            
        if 'hijos' in un_dic:
            for each in un_dic['hijos']:
                self.crear_laberinto_recursivo(each, con)

    def obtenerJuego(self):
        return self.builder.obtenerJuego()
    
    def crear_beasts(self):
        for each in self.dict['bichos']:
            modo = each['modo']
            if modo == 'Agresivo':
                self.builder.makeAggressiveBeastPosition(each['posicion'])
            elif modo == 'Perezoso':
                self.builder.makeLazyBeastPosition(each['posicion'])

class LaberintoBuilder:
    def __init__(self):
        self.game = None
        self.maze = None
    
    def obtenerJuego(self):
        return self.game
    
    def makeGame(self):
        self.game = Game()
        self.game.maze = self.maze

    def makeForm(self):
        return Rectangle()
     
    def makeMaze(self):
        self.maze= Maze()
    
    def makeWall(self):
        return Wall()
    
    def makeDoor(self,room1, room2):
        door=Door(room1, room2)
        return door

    def makeBombIn(self, room):
        bomb=Bomba()
        room.agregarHijo(bomb)
        return bomb

    def makeRoom(self, num):
        room=Room(num)
        room.forma=self.makeForm()
        room.agregarOrientacion(self.makeNorth())
        room.agregarOrientacion(self.makeEast())
        room.agregarOrientacion(self.makeSouth())
        room.agregarOrientacion(self.makeWest())
        for each in room.getOrientations():
            each.setEMinOr(self.makeWall(), room.form)
        self.maze.addRoom(room)
        return room

    def makeNorth(self):
        return Norte().get_instance()

    def makeEast(self):
        return Este.get_instance()
    
    def makeSouth(self):
        return Sur().get_instance()
    
    def makeWest(self):
        return Oeste().get_instance()
    
    def makeDoor(self, un_num, una_or_string, otro_num, otra_or_string):
        lado1 = self.maze.obtenerHabitaciones(un_num)
        lado2 = self.maze.obtenerHabitaciones(otro_num)
        
        or1 = getattr(self, 'make'+una_or_string)()
        or2 = getattr(self, 'make'+otra_or_string)()
        
        pt = Door(lado1, lado2)
        
        lado1.ponerElementoEn(pt,or1) 
        lado2.ponerElementoEn(pt,or2)

    def makeAggressiveBeast(self):
        return Bicho(Agresivo())
    def makeLazyBeast(self):
        return Bicho(Perezoso())
    def makeAggressiveBeastPosition(self, num):
        room=self.maze.obtenerHabitaciones(num)
        bicho=self.makeAggressiveBeast()
        bicho.position=room
        self.game.agregarBicho(bicho)
    def makeLazyBeastPosition(self, num):
        room=self.maze.obtenerHabitaciones(num)
        bicho=self.makeLazyBeast()
        bicho.position=room
        self.game.agregarBicho(bicho)