
#dic_req = {'id-104': '104', 'save-1': 'off', 'date_start-1': '2022-11-22 17:49:00', 'date_stop-1': '2022-11-23 18:39:00', 'description-1': '', 'id-105': '105', 'save-3': 'on', 'date_start-3': '2022-11-22 18:39:00', 'date_stop-3': '2022-11-23 19:29:00', 'description-3': '', 'id-106': '106', 'save-5': 'on', 'date_start-5': '2022-11-22 19:29:00', 'date_stop-5': '2022-11-23 20:19:00', 'description-5': '', 'id-107': '107', 'save-7': 'on', 'date_start-7': '2022-11-22 20:19:00', 'date_stop-7': '2022-11-23 21:09:00', 'description-7': '', 'id-108': '108', 'save-9': 'on', 'date_start-9': '2022-11-22 21:09:00', 'date_stop-9': '2022-11-23 21:59:00', 'description-9': '', 'id-109': '109', 'save-11': 'on', 'date_start-11': '2022-11-22 21:59:00', 'date_stop-11': '2022-11-23 22:49:00', 'description-11': '', 'id-112': '112', 'save-13': 'on', 'date_start-13': '2022-11-22 22:49:00', 'date_stop-13': '2022-11-23 23:39:00', 'description-13': ''}

dic_req = {'id-1': '104', 'save-1': 'on', 'date_start-1': '2022-11-22 17:49:00', 'date_stop-1': '2022-11-23 18:39:00', 'description-1': '', 'id-3': '105', 'save-3': 'off', 'date_start-3': '2022-11-22 18:39:00', 'date_stop-3': '2022-11-23 19:29:00', 'description-3': '', 'id-5': '106', 'save-5': 'on', 'date_start-5': '2022-11-22 19:29:00', 'date_stop-5': '2022-11-23 20:19:00', 'description-5': '', 'id-7': '107', 'save-7': 'on', 'date_start-7': '2022-11-22 20:19:00', 'date_stop-7': '2022-11-23 21:09:00', 'description-7': '', 'id-9': '108', 'save-9': 'on', 'date_start-9': '2022-11-22 21:09:00', 'date_stop-9': '2022-11-23 21:59:00', 'description-9': '', 'id-11': '109', 'save-11': 'on', 'date_start-11': '2022-11-22 21:59:00', 'date_stop-11': '2022-11-23 22:49:00', 'description-11': '', 'id-13': '112', 'save-13': 'on', 'date_start-13': '2022-11-22 22:49:00', 'date_stop-13': '2022-11-23 23:39:00', 'description-13': ''}

len_dic = len(dic_req )
lis_rem = []
for key, value in dic_req.items():
    if value == 'off':
        j = int(key.split("-")[1])
        a = dic_req[f'date_start-{j}']
        s = dic_req[f'date_stop-{j}']
        lis_rem.append(j)
        for i in range(j, len_dic):
            i = i+1
            if dic_req.get(f'date_start-{i}'):
                b = dic_req[f'date_start-{i}']
                c = dic_req[f'date_stop-{j}']
                dic_req[f'date_start-{i}'] = a
                a = b
                s = c

for rm in lis_rem:
    dic_req.pop(f'id-{rm}')
    dic_req.pop(f'save-{rm}')
    dic_req.pop(f'date_start-{rm}')
    dic_req.pop(f'date_stop-{rm}')
    dic_req.pop(f'description-{rm}')



for key, value in dic_req.items():
    if value == 'on':
        j = int(key.split("-")[1])
        print(dic_req[f'id-{j}'])
        print(dic_req[f'save-{j}'])
        print(dic_req[f'date_start-{j}'])
        print(dic_req[f'date_stop-{j}'])
        print(dic_req[f'description-{j}'])





print(dic_req)

