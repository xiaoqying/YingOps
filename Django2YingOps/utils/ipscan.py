import nmap, json


class ScanHosts(object):

    def __init__(self):
        self.nm = nmap.PortScanner()

    def scanHost(self, nets):
        self.nm.scan(nets, arguments='-n -sP -PE')
        all_host = self.nm.all_hosts()
        return all_host

    def allHost(self, nets):
        all_host = self.scanHost(nets)
        # print(all_host)
        nums = []
        for ip in all_host:
            num = int(ip.split('.')[-1])
            nums.append(num)
        nums.sort()
        range_num=[i for i in range(1,255)]
        host_list=[]
        for i in range_num:
            if i in nums:
                host_list.append(str(i)+' Online ')
            else:
                host_list.append(str(i)+' Offline ')
                # range_num.remove(i)
        net = nets.rsplit('.', 1)[0]
        status=[net + '.' + str(i) for i in host_list]

        return status
    def oneHost(self,nets):
        statu=self.scanHost(nets)
        if statu:
            statu=statu[0] + ' Online '
        else:
            statu=nets+' Offline '
        status=[]
        status.append(statu)
        # print(status)
        return status