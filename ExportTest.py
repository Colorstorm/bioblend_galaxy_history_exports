from bioblend.galaxy import GalaxyInstance

ip = '172.XXX.XXX.XXX.XXX'
api_key = 'XXXXXXXX'

gi = GalaxyInstance(url=ip, key=api_key)
histories_list = gi.histories.get_histories(deleted=False)
for history in histories_list:
    jeha_id = gi.histories.export_history(history['id'], gzip=True, include_hidden=False, include_deleted=False,
                                          wait=True, maxwait=None)
    f = open("test/" + history['id'] + '.tar.gz', 'wb')
    gi.histories.download_history(history_id=history['id'], jeha_id=jeha_id, outf=f)
    f.close()