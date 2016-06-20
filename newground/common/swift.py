# coding=utf-8
import swiftclient
from config import swift_endpoint, FDBInfo_rediskeyname, \
    SwiftAccountInfo_rediskeyname
import redis_cli as redis
import json
from swiftclient.exceptions import ClientException


# create new connection
def get_conn(fdbname):

    fdbinfo = json.loads(redis.get_value(FDBInfo_rediskeyname))
    swiftaccountinfo = json.loads(
        redis.get_value(SwiftAccountInfo_rediskeyname))
    swift_user = ''
    try:
        swift_user = fdbinfo[fdbname]
    except:
        return {'error': 'fdb not exists'}
    swift_key = swiftaccountinfo[swift_user]

    conn = swiftclient.Connection(
        user=swift_user,
        key=swift_key,
        authurl='http://' + swift_endpoint + '/auth/v1.0',
    )
    return conn


# def show_account_detail(conn):
#     try:
#         #get_conn(fdbname).
#         return True
#     except:
#         import traceback
#         traceback.print_exc()
#         return False


def create_container(conn, container_name):
    """
    create container
    :param container_name: container name to create
    :return: success return:True else:False
    """
    try:
        conn.put_container(container_name)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False


def create_object(conn, container_name, sw_file_name, local_file_content):
    """
    create an object
    :param local_file_content:file content to upload
    :param container_name: container name to put object
    :param sw_file_name: file name to store on swift
    :param content_type: content type to write
    :return: success return:True else:False
    """
    try:
        conn.put_object(container_name, sw_file_name,
                        contents=local_file_content)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False


def get_container_names(conn):
    """
    list owned containers
    :return: containers name list; [] when error occurs
    """
    namelist = []
    try:
        for container in conn.get_account()[1]:
            namelist.append(container['name'])
        return namelist
    except:
        import traceback
        traceback.print_exc()
        return []


def get_containerinfo(conn, container_name):
    """
    """
    info = ()
    try:
        info = conn.get_container(container_name)
        return info
    except ClientException as ce:
        print ce.message
        return None


def get_file_list(conn, container_name):
    """
    list a container's content
    :param container_name: in which container to list
    :return: file info list; [] when error occurs
    """
    filelist = []
    try:
        for data in conn.get_container(container_name)[1]:
            filelist.append((data['name'], data['bytes'],
                             data['last_modified']))
        return filelist
    except:
        import traceback
        traceback.print_exc()
        return []


def get_object(conn, container_name, file_name, local_file_name):
    """
    retrieve an object
    :param container_name: in which container
    :param file_name: which file on swift
    :param local_file_name: file name to store in local system (including path)
    :return: success return:True else:False
    """
    try:
        obj_tuple = conn.get_object(container_name, file_name)
        with open(local_file_name, 'w') as file:
            file.write(obj_tuple[1])
        return True
    except:
        import traceback
        traceback.print_exc()
        return False


def delete_object(conn, container_name, file_name):
    """
    delete an object
    :param container_name: in which container
    :param file_name: of which file to delete
    :return: success return:True else:False
    """
    try:
        conn.delete_object(container_name, file_name)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False


def delete_container(conn, container_name):
    """
    delete an container
    :param container_name: of which container to delete
    :return: success return:True else:False
    """
    try:
        conn.delete_container(container_name)
        return True
    except:
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    pass
    # print create_container('leixun')
    # print create_object('hello.txt', 'leixun', 'hello.txt', 'text/plain')
    # print get_container_names()
    # print get_file_list('leixun')
    # print get_object('leixun', 'hello.txt', 'hello1.txt')
    # print delete_object('leixun', 'hello.txt')
    # print delete_container('leixun')
