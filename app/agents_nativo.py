import json, asyncio
from app import ai_wrappers
from app.models import internals
from app.prompts import principal, acciones
from app.config.settings import logger
from dotenv import load_dotenv
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

load_dotenv()

async def recursion_arbol(tools:list,messages:list,funciones:list,api_state:internals.Usuario,depth:int,sistema:str,temperatura:float,tipo_funciones:str):

    if(depth==12): raise Exception("Error de recursion, la IA entro en loop depth en 12")

    try:
        response_claude=await ai_wrappers.call_claude(sistema,messages,tools,"claude-sonnet-4-5",temperatura,tipo_funciones,45)
    except:
        logger.info("CAMBIO DE MODELO")
        response_claude=await ai_wrappers.call_claude(sistema,messages,tools,"claude-haiku-4-5",temperatura,tipo_funciones,150)

    tipo_funciones="auto"

    logger.info("Cabecera: %s", response_claude)
    
    if(response_claude.stop_reason == "tool_use"): 

        try:
            tool_use=next(block for block in response_claude.content if block.type == "tool_use")
        except:
            logger.error("Error en tool_use pero sin content")
            return await recursion_arbol(tools=tools,messages=messages,funciones=funciones,api_state=api_state,depth=depth+1,sistema=sistema,temperatura=temperatura,tipo_funciones="any") #Forzar la tool

        logger.info("Function call -> %s", tool_use)

        tool_name = tool_use.name
        function_args = tool_use.input

        response=await acciones.acciones(tool_name,function_args,api_state)
        
        logger.info("%s° DEGREE llamada -> %s", depth, response)

        messages.append({"role": "assistant", "content": response_claude.content})
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": response,
                    }
                ],
            }
        )

        funciones.append({
            "input": str(function_args),
            "name": tool_name,
            "output": str(response)
        })

        return await recursion_arbol(tools=tools,messages=messages,funciones=funciones,api_state=api_state,depth=depth+1,sistema=sistema,temperatura=temperatura,tipo_funciones=tipo_funciones)

    else:

        if(response_claude.content==[]):
            
            logger.info("Devuelve el content en []")
            nombre_ultima=funciones[-1]["name"]
            messages.append({"role": "user", "content": f"Ya tienes la informacion de la ultima funcion llamada {nombre_ultima}. Dale forma y da una respuesta que englobe a todo esto"})
            return await recursion_arbol(tools=tools,messages=messages,funciones=funciones,api_state=api_state,depth=depth+1,sistema=sistema,temperatura=temperatura,tipo_funciones=tipo_funciones)
            
        else:

            respuesta_usuario = response_claude.content[0].text

        detectar_nocall_verificare="Todo bien"

        #detectar_nocall_verificare=generales.detectar_nocall_verificare(dic_claude,funciones)

        if (detectar_nocall_verificare!="Todo bien"):
            
            messages.append({"role": "user", "content": f"Le comentaste al usuario que verificarias o realizarias alguna accion, pero NO USASTE ninguna funcion, llama a las tools correspondientes."})
            
            return await recursion_arbol(tools=tools,messages=messages,funciones=funciones,api_state=api_state,depth=depth+1,sistema=sistema,temperatura=temperatura,tipo_funciones="any")
        
        elif (respuesta_usuario==None or respuesta_usuario==""):
        
            messages.append({"role": "user", "content": f"Hey! No generaste ninguna respuesta al usuario. Formula una respuesta."})
            return await recursion_arbol(tools=tools,messages=messages,funciones=funciones,api_state=api_state,depth=depth+1,sistema=sistema,temperatura=temperatura,tipo_funciones="auto")

        logger.info("Respuesta -> %s",respuesta_usuario)

        return respuesta_usuario

async def margot(usuario:internals.Usuario):


    messages=[{}]
    funciones=[]
    temperatura=0.25
    tipo_funciones="auto"

    tools=principal.tools
    sistema=principal.sistema_prompt(usuario)

    usuario_prompt,dinamico_prompt=principal.usuario_prompt(usuario)

    messages[0]={"role": "user", "content": [{"type":"text","text":usuario_prompt,"cache_control": {"type": "ephemeral"}}]}
    messages.append({"role": "user", "content": dinamico_prompt})

    respuesta=await recursion_arbol(tools,messages,funciones,usuario,1,sistema,temperatura,tipo_funciones)

    return respuesta