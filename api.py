from fastapi import FastAPI
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()

# Ruta raíz.
@app.get("/")
def raiz():
    return {"Mensaje": "La API está funcionando. Visite /docs para obtener la documentación de la API"}

# Api 1.
@app.get("/developer")
def developer(desarrollador:str):
    """Input: Nombre de un desarrollador dentro de steam.
    Retorno: Cantidad de los juegos lanzados por año y su porcentaje de juegos que fueron gratis."""
    
    # Cargo el archivo.
    df_steam_games = pd.read_parquet("output_steam_games_ETL.parquet")
    
    # Nombres únicos de los desarrolladores.
    nombres_desarrolladores = set(df_steam_games["developer"].dropna())
    nombres_desarrolladores = {nombre.lower().strip() for nombre in nombres_desarrolladores}
    
    # Aplico strip() para eliminar espacios vacíos y lower() para comparar con el set de desarrolladores.
    desarrollador = desarrollador.lower().strip()
    
    # Compruebo si el desarrollador está dentro del dataset.
    if desarrollador not in nombres_desarrolladores:
        return {"Desarrollador": f"No existe el desarrollador {desarrollador}"}
    
    del nombres_desarrolladores # Libero memoria que no vuelve a ser usada.
    
    # Variable para guardar los datos del desarrollador.
    datos_desarrollador = []
    
    # Busco todas las apariciones del desarrollador y guardo el precio del producto y su fecha.
    for i in range(len(df_steam_games["developer"])):
        if desarrollador.lower() == str(df_steam_games.loc[i, "developer"]).lower():
            datos_desarrollador.append(df_steam_games.loc[i, ["release_date", "price"]])

    # Obtengo los años en el mismo orden de la lista para ser recorridos
    años = [str(año[0])[:4] for año in datos_desarrollador]
    
    # Variable donde serán almacenados la cantidad de juegos lanzados por año.
    diccionario_objetos = dict()
    # Variable donde serán almacenados la cantidad de juegos gratis almacenados por año.
    diccionario_objetos_gratis = dict() 
    
    # Itero con enumerate para obtener el índice y el año que es el nombre de la variable.
    for i, año in enumerate(años):
        
        # Compruebo si el año ya es clave del diccionario.
        if año in diccionario_objetos:
            # Compruebo que el juego sea gratis.
            if datos_desarrollador[i][1] == 0:
                
                diccionario_objetos[año] += 1
                diccionario_objetos_gratis[año] += 1
                
            diccionario_objetos[año] += 1
        
        # Si año no es clave del diccionario, lo inicializo.
        else:
            # Compruebo que el primer juego sea gratis.
            if datos_desarrollador[i][1] == 0:
                
                diccionario_objetos[año] = 1
                diccionario_objetos_gratis[año] = 1
                
            diccionario_objetos[año] = 1
            diccionario_objetos_gratis[año] = 0
    
    del desarrollador # Libero memoria que no vuelve a ser usada.
    
    # Uno los diccionarios para obtener las fechas y la cantidad de juegos de pago y gratuitos.
    año_cant_objetos_porcentaje_gratis = list(zip(diccionario_objetos.keys(), diccionario_objetos.values(), diccionario_objetos_gratis.values()))
    
    del diccionario_objetos # Libero memoria que no vuelve a ser usada.
    del diccionario_objetos_gratis # Libero memoria que no vuelve a ser usada.
    
    # Obtengo el porcentaje de los juego gratuitos.
    for i in range(len(año_cant_objetos_porcentaje_gratis)):
        año_cant_objetos_porcentaje_gratis[i] = list(año_cant_objetos_porcentaje_gratis[i])
        año_cant_objetos_porcentaje_gratis[i][2] = round((año_cant_objetos_porcentaje_gratis[i][2] / año_cant_objetos_porcentaje_gratis[i][1]) * 100, 2)
    
    # Ordeno la lista para presentar por año de forma ascendente.
    año_cant_objetos_porcentaje_gratis.sort()
    
    def iterador():
        for i in año_cant_objetos_porcentaje_gratis:
            yield {f"Año:": i[0],
                   "Cantidad de juegos lanzados:": i[1],
                   "porcentaje de juegos gratis lanzados": f"{i[2]}%"}
    
    return iterador()



# Api 2.
@app.get("/userdata")
def userdata(user_id: str):
    """Input: Nombre de un usuario dentro de steam.
    Retorno: Nombre del usuario, cantidad de los juegos del usuario y
    su porcentaje de juegos que fueron comprados por recomendación."""
    
    # Cargo el primer archivo.
    df_users_reviews = pd.read_parquet("australian_user_reviews_ETL.parquet")
    
    users = set(df_users_reviews["user_id"].dropna())
    users = {str(user) for user in users}
    
    user_id = user_id.strip()
    
    if user_id not in users:
        return f"No existe el usuario {user_id} en la base de datos."
    
    del users
    
    recomendaciones_si_no = df_users_reviews[df_users_reviews["user_id"] == user_id]["recommend"].tolist()
    juegos = []
    total_juegos = 0
    recomendaciones_total = 0
    precio_total = 0.0
    
    # Libero memoria.
    del df_users_reviews
    
    # Cargo el segundo archivo.
    df_users_items = pd.read_parquet("australian_users_items_ETL.parquet")
            
    for i, user in enumerate(df_users_items["user_id"]):
        if user_id == user:
            juegos.append(df_users_items.loc[i, "item_id"])
            total_juegos = df_users_items.loc[i, "items_count"]
    
    # Libero memoria.
    del df_users_items
    
    # Cargo el tercer archivo.
    df_steam_games = pd.read_parquet("output_steam_games_ETL.parquet")
     
    for i in df_steam_games.index:
        
        if str(df_steam_games.loc[i, "id"]) in juegos:
            precio_total += df_steam_games.loc[i, "price"]
            
    # Libero memoria.
    del df_steam_games
            
    recomendaciones_total = sum(recomendaciones_si_no)  # Sumar booleanos para contar True

    if int(total_juegos) == 0 or recomendaciones_total == 0:
        porcentaje_recomendaciones = 0.0
    else:
        porcentaje_recomendaciones = round((recomendaciones_total / total_juegos) * 100, 2)
        
    print(type(precio_total), type(user_id), type(total_juegos), type(porcentaje_recomendaciones))
            
    return {"Usuario": user_id,
            "Dinero gastado": f"{round(float(precio_total), 2)}$",
            "Total de juegos": int(total_juegos),
            "Porcentaje de juegos comprados recomendados": f"{float(porcentaje_recomendaciones)}%"}
    


# Sistema de recomendación.
@app.get("/recomendacion_juego")
def recomendacion_juego(id_producto: int):
    """Input: El id de un juego.
    Ouput: 5 juegos recomendados en base a la entrada."""
    
    #Cargo las recomendaciones.
    df_recomendaciones = pd.read_csv("recomendaciones_de_juegos.csv")
    
    # Compruebo que la entrada no este vacía.
    if not id_producto:
        return f"Por favor, escriba el id del juego el que desea obtener recomendaciones."
    
    # Compruebo que el id exista en el df.
    if not df_recomendaciones["id_game"].isin([id_producto]).any():
        return {"error": f"No existe el juego con el id: {id_producto}"}
    
    # Obtengo las recomendaciones del juego.
    recomendaciones = df_recomendaciones[df_recomendaciones["id_game"] == id_producto]["recomendaciones"].tolist()
    
    # Retorno el id y sus recomendaciones.
    return {"Juego": id_producto,
            "Recomendaciones": recomendaciones}
