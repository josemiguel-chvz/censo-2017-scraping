# Extracción datos Censo 2017 Chile

El siguiente script permite obtener distintos datos desde la pagina web
```
http://resultados.censo2017.cl/
```

Utilizando selenium y python, se busca probar la tecnica de web scraping a traves de la automatización
en la navegación del sitio web del Censo 2017 utilizando los selectores de región y comuna provistos por el sitio.
La obtención de la data se realiza usando xPath.
Finalmente se genera un archivo JSON con los datos respectivos sobre la región y sus comunas.

### Pre-requisitos 📋

Iniciar ambiente virtual (virtualenv, pipenv)

Instalar librerias
```
pip install -r requirements.txt
```

Selenium Driver Browser
```
Chrome
```
Debe contar con google chrome instalado

## Ejecución ⚙️

```
python script.py
```



