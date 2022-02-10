# Extracción datos Censo 2017 Chile

El siguiente script permite obtener distintos datos desde la pagina web 
```
http://resultados.censo2017.cl/
```
generando JSONs para cada región y comuna.

Este JSON puede ser insertado en algún endpoint POST que registre los datos del censo
según sea el metodo y base de datos del usuario (API, conexión a BD (pymysql, etc))

En caso contrario se genera un archivo JSON con los datos requeridos.

el archivo connector.py presenta un ejemplo de conexión a API.

el script utiliza la libreria Selenium para manejar la pagina web, y los componentes para iterar sobre las comunas y regiones.


### Pre-requisitos 📋

Iniciar ambiente virtual (virtualenv, pipenv)

Instalar librerias script

```
pip install -r requirements.txt
```

## Ejecución ⚙️

```
python script.py
```



