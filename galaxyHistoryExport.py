from bioblend.galaxy import GalaxyInstance
import os
import argparse


#########################
# Functions
########################

def print_status(p_username, p_history_id, p_status, p_warnings):
    switch = {
        0: ' ' * 9 + p_username[:18] + ' ' * (20 - len(p_username)) + p_history_id + ' successfully exported',
        1: 'Warning: ' + p_username[:18] + ' ' * (36 - len(p_username)) + ' will be skipped',
        2: 'Error:   ' + p_username[:18] + ' ' * (20 - len(p_username)) + p_history_id + ' unknown error',
        3: 'Warning: ' + p_username[:18] + ' ' * (20 - len(p_username)) + p_history_id +
           ' ' * (17 - len(p_history_id)) + ' does not exist',
        4: 'Warning: ' + p_username[:18] + ' ' * (20 - len(p_username)) + p_history_id + ' is already exported'
    }

    if p_warnings:
        print(switch[p_status])
    else:
        if p_status != 1 and p_status != 4:
            print(switch[p_status])


def export_history(p_gi, p_history, p_user, p_path, p_update, p_warning, p_print_errors):
    export_file = p_path + '/' + p_history['id'] + '.export.tar.gz'
    if p_update and not os.path.isfile(export_file) or not p_update:
        try:
            jeha_id = p_gi.histories.export_history(p_history['id'], gzip=True, include_hidden=False,
                                                    include_deleted=False, wait=True, maxwait=None)
            f = open(export_file, 'wb')
            p_gi.histories.download_history(history_id=p_history['id'], jeha_id=jeha_id, outf=f)
            f.close()
            print_status(p_user['username'], p_history['id'], 0, p_warning)

            error_path = p_user['username'] + "/" + p_history['id'] + '.error.txt'
            if os.path.isfile(error_path):
                os.remove(error_path)
        except Exception as e:
            if p_print_errors:
                print(e)
            f = open(p_path + "/" + p_history['id'] + '.error.txt', 'w')
            dictionary = p_gi.histories.get_histories(p_history['id'])[0]
            f.writelines(''.join(key + str(dictionary[key]) + '\n' for key in dictionary))
            f.writelines(str(e))
            f.close()
            print_status(p_user['username'], p_history['id'], 2, p_warning)
    else:
        print_status(p_user['username'], p_history['id'], 4, p_warning)


#########################
# Main method
########################

def main(arguments):
    args = arguments.__dict__

    gi = GalaxyInstance(url=args['ip'], key=args['key'])
    users = gi.users.get_users(deleted=False)

    for user in users:
        if args['usernames'] is None or user['username'] in args['usernames']:

            if gi.users.get_user_apikey(user['id']) == 'Not available.':
                gi.users.create_user_apikey(user['id'])
            tmp_gi = GalaxyInstance(url=args['ip'], key=gi.users.get_user_apikey(user['id']))

            path = args['outputDirectory'] + '/' + user['username']

            if not os.path.exists(path):
                os.makedirs(path)

            if args['ids'] is not None:

                for history_id in args['ids']:
                    histories = tmp_gi.histories.get_histories(history_id=history_id, deleted=False)

                    if not histories:
                        print_status(user['username'], history_id, 3, args['warning'])
                    else:
                        export_history(tmp_gi, histories[0], user, path, args['error'], args['warning'],
                                       args['printErrors'])
            else:
                histories_list = tmp_gi.histories.get_histories(deleted=False)
                for history in histories_list:
                    export_history(tmp_gi, history, user, path, args['errorCorrection'], args['warning'],
                                   args['printErrors'])
        else:
            print_status(user['username'], '', 1, args['warning'])


##############################
# Commandline arguments definition
##############################

if __name__ == '__main__':
    parser = argparse.ArgumentParser(epilog='Exports histories from galaxy using bioblend.')
    parser.add_argument('ip',
                        help='ip/hostname of your galaxy machine')
    parser.add_argument('key',
                        help='The API key of an admin on the galaxy machine')
    parser.add_argument('-u', '--usernames', type=str, nargs='+', default=None,
                        help='To export only histories of special users')
    parser.add_argument('-i', '--ids', type=str, nargs='+', default=None,
                        help='To export only histories with the id')
    parser.add_argument('-o', '--outputDirectory', type=str, default=os.getcwd(),
                        help='Set the path to the output directory, default it is your working directory')
    parser.add_argument('-e', '--errorCorrection', type=bool, default=False,
                        help='Mode for error correction, if there is a tar.gz file for the history it will skip these')
    parser.add_argument('-w', '--warning', type=bool, default=False,
                        help='Print warnings')
    parser.add_argument('-p', '--printErrors', type=bool, default=False,
                        help='Print error messages, for debugging purposes')

    main(parser.parse_args())
