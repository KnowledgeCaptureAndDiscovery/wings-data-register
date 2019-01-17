import cgi
import requests
import os
import logging

WINGS_API_URL = "http://datascience4all.org/wings-portal"
logger = logging.getLogger('demo')

def getFilename(filepath):
    return os.path.basename(filepath).split('.')[0]

def getDataTypeJSON(session, user, domain):
    data = 'data/getDataTypeJSON?data_type=\
        http%://www.wings-workflows.org/ontology/\
        data.owl%23DataObject&_dc=1547668799874'
    url = '{}/users/{}/{}/{}'.format(WINGS_API_URL, user, domain, data)
    response = session.get(url, cookies=cookies)

'''
Add data in DataType
'''
def addDataForType(session, user, domain, datatype, filename):
    url = '{}/users/{}/{}/data/addDataForType'.format(
        WINGS_API_URL, user, domain)
    payload = {
        'data_type': 
            "http://ontosoft.isi.edu:8080/wings-portal/export/users/{}/{}/data/ontology.owl#{}".\
                format(user, domain, datatype),
        'data_id': 
            'http://ontosoft.isi.edu:8080/wings-portal/export/users/{}/{}/data/library.owl#{}'\
            .format(user, domain, filename)
    }
    headers = {'X-Requested-With': 'XMLHttpRequest'}

    try:
        response = session.post(
            url,
            data=payload,
            headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.exception("HTTP error {}".format(e))
    except requests.exceptions.RequestException as e:
        logger.exception("Connection error {}".format(e))

    response.raise_for_status()
    print(response.text)

    return response

'''
Set the location for the datafile
'''
def setDataLocation(session, user, domain, filepath, filename):
    url = '{}/users/{}/{}/data/setDataLocation'.format(
        WINGS_API_URL, user, domain)
    payload = {
        'location':
            '/opt/wings/storage/default/users/{}/{}/data/{}'.\
                format(user, domain, filepath),
        'data_id':
            'http://ontosoft.isi.edu:8080/wings-portal/export/users/{}/{}/data/library.owl#{}'.\
            format(user, domain, filename)
    }
    headers = {'X-Requested-With': 'XMLHttpRequest'}

    try:
        response = session.post(
            url,
            data=payload,
            headers=headers)
    except requests.exceptions.HTTPError as e:
        logger.exception("HTTP error {}".format(e))
    except requests.exceptions.RequestException as e:
        logger.exception("Connection error {}".format(e))

    response.raise_for_status()
    print(response.text)

    return response

'''
Upload the data
'''

def uploadData(session, user, domain, filepath):
    files = {'file': open(filepath, 'rb')}
    url = '{}/users/{}/{}/upload'.format(WINGS_API_URL, user, domain)
    payload = {
        'type': 'data'
    }
    try:
        response = session.post(
            url,
            data=payload,
            files=files)
    except requests.exceptions.HTTPError as e:
        logger.exception("HTTP error {}".format(e))
    except requests.exceptions.RequestException as e:
        logger.exception("Connection error {}".format(e))

    response.raise_for_status()
    print(response.text)

    return response


'''
Upload the data
'''
def login(session, username, password):
    url_login = '{}/login'.format(WINGS_API_URL)
    try:
        response = session.get(url_login)
    except requests.exceptions.HTTPError as e:
        logger.exception("HTTP error {}".format(e))
    except requests.exceptions.RequestException as e:
        logger.exception("Connection error {}".format(e))

    url_security = '{}/j_security_check'.format(WINGS_API_URL)
    payload = {
        'j_username': username,
        'j_password': password
    }
    try:
        response = session.post(url_security,data=payload)
    except requests.exceptions.HTTPError as e:
        logger.exception("HTTP error {}".format(e))
    except requests.exceptions.RequestException as e:
        logger.exception("Connection error {}".format(e))
    return response


def addUploadNewData(session, username, domain, filepath):
    datatype = "NetCDF"
    filename = getFilename(filepath)
    addDataForType(session, username, domain, datatype, filename)
    setDataLocation(session, username, domain, filepath, filename)
    response = uploadData(session, username, domain, filepath)


username = os.environ.get('WINGS_USERNAME')
password = os.environ.get('WINGS_PASSWORD')
domain = 'CompClim'
session = requests.Session()
filepath = "filetest.txt"
login(session, username, password)
addUploadNewData(session, username, domain, filepath)