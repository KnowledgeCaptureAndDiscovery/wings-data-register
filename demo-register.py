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
            cookies=cookies,
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
            cookies=cookies,
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
            cookies=cookies,
            data=payload,
            files=files)
    except requests.exceptions.HTTPError as e:
        logger.exception("HTTP error {}".format(e))
    except requests.exceptions.RequestException as e:
        logger.exception("Connection error {}".format(e))

    response.raise_for_status()
    print(response.text)

    return response


def addUploadNewData(session, user, domain, filepath):
    datatype = "NetCDF"
    filename = getFilename(filepath)
    addDataForType(session, user, domain, datatype, filename)
    setDataLocation(session, user, domain, filepath, filename)
    response = uploadData(session, user, domain, filepath)
    print(response.text)



username = 'mosorio'
domain = 'CompClim'
session = requests.Session()
cookies = {'JSESSIONID': '3053BF7F149BC18B3409D6AF99217D45'}
filepath = "filetest.txt"
addUploadNewData(session, username, domain, filepath)