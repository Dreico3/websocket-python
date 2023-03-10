#!/usr/bin/env python
import json
import asyncio
import websockets

puerto = 8765
data = []
# esto es un lista


def traerJson():
    with open("/home/erick/Escritorio/prueva/python/webSockets/src/datos.json") as archivoJson:
        # print(type(archivoJson))
        # .load(archivo)  lo convierte en una lista
        data = json.load(archivoJson)
        return data


def agregar(pokemon):
    # retorna retorna lista de pokemones
    print(f'agregando a {pokemon["name"]} a la lista')
    pokemon.pop('orden')
    data.append(pokemon)
    # return data


def mostrar():
    return data


def eliminar(elemento):
    cont = -1
    for ele in data:
        cont += 1
        if ele['name'] == elemento['name']:
            data.pop(cont)
            return {'mensaje': 'eliminado'}

    return {'mensaje': 'elemento no existente'}


def modificar(element):
    element.pop('orden')
    print(f'modificando {element}')

    cont = -1
    for ele in data:
        cont += 1
        if ele['id'] == element['id']:
            # data.pop(cont)
            ele['name'] = element['name']
            ele['base_experience'] = element['base_experience']
            ele['image'] = element['image']
            return {'mensaje': 'elemento modificado'}

    return {'mensaje': f'elemento no encontrado {element}'}


def control(dato):
    print('controlando esto')
    print(dato['orden'])
    print('-----------------------------')

    if dato['orden'] == 'agregar':
        print(dato['orden'], '<--orden recibido')
        agregar(dato)
        return {'mensaje': f'item agregado ->{dato}'}
    elif dato['orden'] == 'mostrar':
        return mostrar()
    elif dato['orden'] == 'eliminar':
        return eliminar(dato)
    elif dato['orden'] == 'modificar':
        return modificar(dato)
    return {'mensaje': 'orden no encontrado'}
    # else if papa


async def hello(websocket):
    # aqui es donde agaramos lo q nos envia el front
    while True:
        name = await websocket.recv()
        print(f"<<< nos llega esto -> {name}")
        # transformano el elemento en un diccionario
        elementoTrans = json.loads(json.loads(name))

        # controlador
        jsonObject = json.dumps(control(elementoTrans))

        # interesante forma de mandar lo que sea
        # mensaje=json.dumps({'mensaje':'hola'})
        # solo tiene que estar en formanto json para q pueda funcionar
        await websocket.send(jsonObject)
        #print(f"le respondimos esto >>> {json_lista}")


async def main():
    async with websockets.serve(hello, "localhost", puerto):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    data = traerJson()
    print('servidor running in PORT ' + str(puerto))
    asyncio.run(main())
