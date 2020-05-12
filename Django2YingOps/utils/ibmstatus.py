import threading, urllib3, requests

from conf.ibm import return_ibm_list

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_status(ip):
    session = requests.Session()
    url = 'https://{0}/data/login'.format(ip)
    # 请求头信息
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
        'Referer': 'https://{0}/designs/imm/index.php'.format(ip)
    }
    # 表单数据
    formdata = {
        'user': 'USERID',
        'password': 'PASSW0RD',
        'SessionTimeout': '1200',
    }

    response = session.post(url=url, data=formdata, verify=False, headers=headers)
    # 登录成功后返回的数据内容{}
    token = response.json()
    # 第二次请求的头信息
    if 'token2_name' in token:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
            'Referer': 'https://{0}/designs/imm/index-console.php'.format(ip),
            token['token2_name']: token['token2_value']
        }
    else:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
            'Referer': 'https://{0}/designs/imm/index-console.php'.format(ip),
        }
    try:
        # 新url
        geturl = 'https://{0}/designs/imm/dataproviders/imm_status_hardware.php'.format(ip)
        response = session.get(url=geturl, headers=headers)
        res = response.json()
        res[ip] = res.pop('items')[0].pop('hardware_health')
        return res
    except KeyError:
        # 新url
        geturl = 'https://{0}/designs/imm/dataproviders/imm_status.php'.format(ip)
        response = session.get(url=geturl, headers=headers)
        res = response.json()
        return res


def return_res(ip):
    dict1 = {}
    res = get_status(ip=ip)
    dict2 = {}

    # res={'192.168.101.1': [{'id': 1, 'type': 'Cooling Devices', 'status': 'Normal', 'count': 16}, {'id': 2, 'type': 'Power Modules', 'status': 'Normal', 'count': 17}, {'id': 3, 'type': 'Disks', 'status': 'Normal', 'count': 2}, {'id': 4, 'type': 'Processors', 'status': 'Normal', 'count': 6}, {'id': 5, 'type': 'Memory', 'status': 'Normal', 'count': 53}, {'id': 6, 'type': 'System', 'status': 'Normal', 'count': 1}, {'id': 7, 'type': 'Adapters', 'status': 'Normal', 'count': 0}]}
    for i in res[ip]:
        name = i['type']
        status = i['status']
        dict2[name] = status
    dict1[ip] = dict2

    return dict1


class MyThread(threading.Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)
        # print self.result

    def get_result(self):

        try:
            return self.result
        except Exception:
            return None


def getIbmList():
    # import datetime
    # start_time=datetime.datetime.now()
    # #
    ip_list = return_ibm_list()

    t_objs = []
    res_list = []
    for ip in ip_list:
        t = MyThread(return_res, args=(ip,))
        t.start()
        t_objs.append(t)
    for t in t_objs:
        t.join()
        res_list.append(t.result)

    # end_time=datetime.datetime.now()
    #
    # total_time=end_time-start_time
    #
    # print('--------all time-----------',total_time)
    return res_list
