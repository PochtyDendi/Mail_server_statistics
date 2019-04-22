import random
import re


def main_func():
    list_of_data = open_file('maillog/maillog')
    list_of_users = get_list_of_users(list_of_data)
    result = get_result(list_of_users)
    return result, list_of_users


def open_file(path_to_file):
    list_of_line = []
    file_data = open(path_to_file, 'r')
    for line in file_data:
        list_of_line.append(line)
    return list_of_line


def get_list_of_users(list_of_data):
    dict_of_users = {'users': {}}
    ids = []
    for i in list_of_data:
        if 'sasl_username' in i:
            message_id = re.search(r'\w{11}', i)
            message_id = message_id.group(0)
            ids.append(message_id)
            if message_id not in dict_of_users['users']:
                dict_of_users['users'].update({message_id: {}})
            else:
                dict_of_users['users'].update({message_id+random.randint(1, 1000): {}})
        for j in ids:
            if j in i and 'from=<' in i:
                # find email 'from'
                email_str = re.search(r'<(.*?)>', i)
                email = email_str.group(0)
                email_from = email[1:-1]
                if email_from not in dict_of_users['users']:
                    dict_of_users['users'][j].update({email_from: {}})
                    break
            elif j in i and 'to=<' in i:
                # find email 'to'
                email_to_str = re.search(r'<(.*?)>', i)
                email_to = email_to_str.group(0)
                email_to = email_to[1:-1]
                # find status
                status_str = re.search(r'status=([a-z]{1,10})', i)
                status = status_str.group(0)
                status = re.sub(r"status=", "", status)
                # add to dict
                email_from_key = dict_of_users['users'][j].keys()
                email_from = []
                for i in email_from_key:
                    email_from.append(i)
                dict_of_users['users'][j][email_from[0]].update({email_to: status})
                break
            elif j in i and 'removed' in i:
                ids.remove(j)
    return dict_of_users


def get_result(list_of_users):
    result = {}
    for i in list_of_users['users']:
        for j in list_of_users['users'][i]:
            s_count = 0
            f_count = 0
            if '@' not in j:
                continue
            else:
                for k in list_of_users['users'][i][j]:
                    if list_of_users['users'][i][j][k] == 'sent':
                        s_count = s_count + 1
                    else:
                        f_count = f_count + 1
                if j in result:
                    s_count = result[j]['sent'] + s_count
                    f_count = result[j]['not_sent'] + f_count
            result.update({j: {'sent': s_count, 'not_sent': f_count}})
    return result


print(main_func())
