from pyrsistent import b
from stockfish import Stockfish
import sqlite3
import time
import pyautogui
import random

#pyautogui.click(100, 100)


columnas_blancas = {"a":(76/2)*1, "b":(76/2)*3,"c":(76/2)*5,"d":(76/2)*7, "e":(76/2)*9, "f":(76/2)*11,"g":(76/2)*13,"h":(76/2)*15}
filas_blancas    = {"1":792, "2":716,"3":640,"4":564, "5":488, "6":412,"7":336,"8":260}
columnas_negras = {"h":(76/2)*1, "g":(76/2)*3,"f":(76/2)*5,"e":(76/2)*7, "d":(76/2)*9, "c":(76/2)*11,"b":(76/2)*13,"a":(76/2)*15}
filas_negras    = {"8":792, "7":716,"6":640,"5":564, "4":488, "3":412,"2":336,"1":260}

contador = 1
stockfish = Stockfish(path="./stockfish_15_win_x64_avx2/stockfish_15_x64_avx2.exe", depth=18, parameters={"Threads": 4, "Minimum Thinking Time": 1, "Hash": 256})
stockfish.set_skill_level(5)
color = input("B o N:")
if color == "b":
    best_move = stockfish.get_best_move(1000)
    stockfish.set_position([best_move])
    pyautogui.click(columnas_blancas[best_move[0]],filas_blancas[best_move[1]])
    pyautogui.click(columnas_blancas[best_move[2]],filas_blancas[best_move[3]])
    contador += 1
else:
    con = sqlite3.connect(r"C:\Users\Victor\AppData\Local\Google\Chrome\User Data\Default\databases\https_lichess.org_0\5")
    cur = con.cursor()
    cur.execute('SELECT * FROM Move ORDER BY id DESC')
    last_fetch = cur.fetchone()
    con.close()
    stockfish.set_position([last_fetch[1]])
    best_move = stockfish.get_best_move(1000)
    stockfish.make_moves_from_current_position([best_move])
    pyautogui.click(columnas_negras[best_move[0]],filas_negras[best_move[1]])
    pyautogui.click(columnas_negras[best_move[2]],filas_negras[best_move[3]])

con = sqlite3.connect(r"C:\Users\Victor\AppData\Local\Google\Chrome\User Data\Default\databases\https_lichess.org_0\5")
cur = con.cursor()
cur.execute('SELECT * FROM Move ORDER BY id DESC')
last_fetch = cur.fetchone()
con.close()
print(last_fetch)
while True:
    con = sqlite3.connect(r"C:\Users\Victor\AppData\Local\Google\Chrome\User Data\Default\databases\https_lichess.org_0\5")
    cur = con.cursor()
    cur.execute('SELECT * FROM Move ORDER BY id DESC')
    current_fetch = cur.fetchone()
    con.close()
    if(current_fetch != last_fetch):
        if (color == "b" and int(current_fetch[0]) % 2 == 0) or (color == "n" and int(current_fetch[0]) % 2 == 1):#el jugador negro ha movido
            try:
                stockfish.make_moves_from_current_position([current_fetch[1]])
            except Exception as e:
                print(e)
                if(current_fetch[1]=="e8h8"):
                    stockfish.make_moves_from_current_position(["e8g8"])
                elif current_fetch[1] == "e8a8":
                    stockfish.make_moves_from_current_position(["e8c8"])
                elif current_fetch[1] == "e1h1":
                    stockfish.make_moves_from_current_position(["e1g1"])
                elif current_fetch[1] == "e1a1":
                    stockfish.make_moves_from_current_position(["e1c1"])    
            best_move = stockfish.get_best_move(1000)
            stockfish.make_moves_from_current_position([best_move])
            if color == "b":
                pyautogui.click(columnas_blancas[best_move[0]]+ random.randint(-30, 30),filas_blancas[best_move[1]]+ random.randint(-30, 30))
                time.sleep(random.uniform(0, 4))
                pyautogui.click(columnas_blancas[best_move[2]]+ random.randint(-30, 30),filas_blancas[best_move[3]]+ random.randint(-30, 30))
            else:
                pyautogui.click(columnas_negras[best_move[0]] + random.randint(-30, 30),filas_negras[best_move[1]] + random.randint(-30, 30))
                time.sleep(random.uniform(0, 4))
                pyautogui.click(columnas_negras[best_move[2]] + random.randint(-30, 30) ,filas_negras[best_move[3]]+ random.randint(-30, 30))
            
        
        last_fetch = current_fetch
        current_fetch = ''
    time.sleep(random.uniform(0.4, 0.5))
    
   