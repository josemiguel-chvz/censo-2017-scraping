import requests


def get_token(email,password):

	try:
		global GLOBAL_API_URL
		url = GLOBAL_API_URL+'auth/login/'
		
		data_login = {
			'email': email,
			'password': password
		}

		response = requests.post(url,data=data_login)
		status = response.status_code
		if status == 200:
			data = response.json()
			user_type = data['user_type']
			if user_type == "staff":
				token = data['tokens']['access']
			else:
				print('No tiene permiso.')
				token = None
		else:
			token = None

		return token

	except requests.exceptions.HTTPError as error:
		print(error)

def insert_data(API_URL_INSERT,data_insert):

    try:
    	global header, API_URL
    	url = API_URL+API_URL_INSERT
    	response = requests.post(url,data=data_insert,headers=header)
    	status = response.status_code
    	
    	if(status == 201):
    		print('dato insertado')
    	else:
    		print('error '+str(status)+' \n')
    		print(data_insert)

    except requests.exceptions.HTTPError as error:
        print(error)


def get_data_comuna(codigo_comuna):

	try:
		global header, API_URL
		url = API_URL+f'comunas/?codigo={codigo_comuna}'
		
		response = requests.get(url,headers = header)
		status = response.status_code
		if status  == 200:
		
			data = response.json()
			if( data['count'] > 0 ):
				data_result = data['results'][0]
			elif( data['count'] == 0 ):
				data_result = {}

		return data_result

	except requests.exceptions.HTTPError as error:
		print(error)


def get_data_region(numero_region):

	try:
		global header, API_URL

		url = API_URL+f'regiones/?numero_region={numero_region}'
		response = requests.get(url,headers = header)
		status = response.status_code
		if status  == 200:
		
			data = response.json()
			if( data['count'] > 0 ):
				data_result = data['results'][0]
			elif( data['count'] == 0 ):
				data_result = {}

		return data_result

	except requests.exceptions.HTTPError as error:
		print(error)



#Generar API URL para obtencion e inserción de datos
#Ejemplo: http://api.example.com/api-v1/
#URL_API = http://api.example.com/
#URL_UBICACION_DATOS = api-v1/
GLOBAL_API_URL = 'URL_API/'
url = 'URL_UBICACION_DATOS/'
API_URL = GLOBAL_API_URL+url


#Token se obtiene desde API. 
#No necesario si usa una API sin autenticación
token = get_token('EMAIL','PASSWORD')
header = {'Authorization': f'Token {token}'}