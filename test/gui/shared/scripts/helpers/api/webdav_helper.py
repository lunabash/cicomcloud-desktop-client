import urllib.parse
import helpers.api.HttpHelper as request
from helpers.ConfigHelper import get_config
from os import path


def get_webdav_url():
    return path.join(get_config('localBackendUrl'), "remote.php", "dav", 'files')


def get_resource_path(user, resource):
    resource = resource.strip('/')
    encoded_resource_path = [
        urllib.parse.quote(path, safe='') for path in resource.split('/')
    ]
    encoded_resource_path = '/'.join(encoded_resource_path)
    url = path.join(get_webdav_url(), user, encoded_resource_path)
    return url


def resource_exists(user, resource):
    response = request.propfind(get_resource_path(user, resource), user=user)
    if response.status_code == 207:
        return True
    elif response.status_code == 404:
        return False
    else:
        raise Exception(f"Server returned status code: {response.status_code}")


def get_file_content(user, resource):
    response = request.get(get_resource_path(user, resource), user=user)
    return response.text