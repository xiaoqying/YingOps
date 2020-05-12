import re, json, os, base64, datetime
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from .models import *

from Django2YingOps.settings import WSSH_IP
from utils.nmap_assets import GetLinuxMethod
from utils.mixin_util import LoginRequiredMixin
from utils.ibmstatus import getIbmList
from utils.ipscan import ScanHosts
import xlwt
from io import BytesIO


# 初始化资产/新增资产
class AssetsInit(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'assets/init.html', locals())

    def post(self, request):
        nets = re.split('\;|\；', request.POST.get('nets', '').strip())
        user_list = re.split('\;|\；', request.POST.get('user_list', '').strip())
        port_list = re.split('\;|\；', request.POST.get('port_list', '').strip())
        passwd_list = re.split('\;|\；', request.POST.get('passwd_list', '').strip())
        # port_list = [int(port) for port in port_list]
        # print(nets, user_list, port_list, passwd_list)
        # nets = '192.168.5.155'
        glm = GetLinuxMethod()
        linux_list = glm.get_linux_list(nets)
        assets_dict = glm.try_ssh_login(linux_list, user_list, port_list, passwd_list)
        if not assets_dict:
            return render(request, 'assets/init.html', {'msg': '{0}密码错误，添加失败！'.format(nets[0])})
        for ip, values in assets_dict.items():
            # print('------>', '进来了呢' )
            try:
                assets_info = AssetsInfo.objects.get(ip=values[3])
                pass
            except Exception as e:
                assets_info = AssetsInfo()
                assets_info.ssh_user = values[0]
                assets_info.ssh_passwd = values[1]
                assets_info.ssh_port = values[2]
                assets_info.ip = values[3]
                assets_info.hostname = values[4]
                assets_info.cpu_cores = values[5]
                assets_info.mem_total = values[6]
                assets_info.disk_total = values[7]
                assets_info.cpu_status = values[8]
                assets_info.mem_status = values[9]
                assets_info.disk_status = values[10]
                assets_info.system_time = values[11]
                assets_info.up_time = values[12]
                assets_info.system_ver = values[13]
                assets_info.mac_address = values[14]
                assets_info.sn = values[15]
                assets_info.manufacturer = values[16]
                assets_info.product = values[17]
                assets_info.cpu_info = values[18]
                assets_info.save()
            # print('新增资产：{0} 成功'.format(ip))
        return redirect('assets:assets_list')


# 资产API
class AssetsListApiView(View):
    def get(self, request):
        obj = AssetsInfo.objects.all()
        assets_info = {}
        for i in obj:
            tmp_dict = {}
            tmp_dict['ip'] = i.ip
            tmp_dict['hostname'] = i.hostname
            tmp_dict['cpu_status'] = i.cpu_status
            tmp_dict['mem_status'] = i.mem_status
            tmp_dict['disk_status'] = i.disk_status
            tmp_dict['sn'] = i.sn
            tmp_dict['up_time'] = i.up_time
            assets_info[i.ip] = tmp_dict
        return HttpResponse(json.dumps(assets_info))


# 资产列表
class AssetsListView(LoginRequiredMixin, View):
    def get(self, request):
        obj = AssetsInfo.objects.filter(is_delete=False).all()
        return render(request, 'assets/linux.html', locals())

    def post(self, request):
        # 删除资产
        ip = request.POST.get('delip').strip()
        AssetsInfo.objects.filter(ip=ip).update(is_delete=True)
        return HttpResponse('delok')


# 资产当前状态获取
class AssetsLiveStatuslView(View):
    # 详情页刷新资产信息
    def get(self, request):
        try:
            ip = request.GET.get('ip', '').strip()
            obj = AssetsInfo.objects.filter(ip=ip).first()
            linux_list = [ip]
            user_list = [obj.ssh_user]
            port_list = [obj.ssh_port]
            passwd_list = [obj.ssh_passwd]
            glm = GetLinuxMethod()
            assets_dict = glm.try_ssh_login(linux_list, user_list, port_list, passwd_list)
            update_dict = {}
            for ip, values in assets_dict.items():
                update_dict['hostname'] = values[4]
                update_dict['cpu_cores'] = values[5]
                update_dict['mem_total'] = values[6]
                update_dict['disk_total'] = values[7]
                update_dict['cpu_status'] = values[8]
                update_dict['mem_status'] = values[9]
                update_dict['disk_status'] = values[10]
                update_dict['system_time'] = values[11]
                update_dict['up_time'] = values[12]
                update_dict['system_ver'] = values[13]
                update_dict['mac_address'] = values[14]
                update_dict['sn'] = values[15]
                update_dict['manufacturer'] = values[16]
                update_dict['product'] = values[17]
                update_dict['cpu_info'] = values[18]
            # print(update_dict)
            AssetsInfo.objects.filter(ip=ip).update(**update_dict)
            return HttpResponse('刷新成功')
        except Exception:
            return HttpResponse('刷新失败')

    # agent定时更新资产信息
    def post(self, request):
        try:
            ip = request.POST.get('ip', '')
            # print('------>',ip)
            if AssetsInfo.objects.get(ip=ip):
                assets_dict = {}
                assets_dict['hostname'] = request.POST.get('hostname', '')
                assets_dict['cpu_cores'] = request.POST.get('cpu_cores', '')
                assets_dict['mem_total'] = request.POST.get('mem_total', '')
                assets_dict['disk_total'] = request.POST.get('disk_total', '')
                assets_dict['cpu_status'] = request.POST.get('cpu_status', '')
                assets_dict['mem_status'] = request.POST.get('mem_status', '')
                assets_dict['disk_status'] = request.POST.get('disk_status', '')
                assets_dict['system_time'] = request.POST.get('system_time', '')
                assets_dict['up_time'] = request.POST.get('up_time', '')
                assets_dict['system_ver'] = request.POST.get('system_ver', '')
                assets_dict['mac_address'] = request.POST.get('mac_address', '')
                assets_dict['sn'] = request.POST.get('sn', '')
                assets_dict['manufacturer'] = request.POST.get('manufacturer', '')
                assets_dict['product'] = request.POST.get('product', '')
                assets_dict['cpu_info'] = request.POST.get('cpu_info', '')
                # print('assets_dict', assets_dict)
                AssetsInfo.objects.filter(ip=ip).update(**assets_dict)
                return HttpResponse('update ok \n')
                # assets_info.hostname = request.POST.get('ip','')
        except Exception:
            return HttpResponse('post error ...\n')
        # except Exception:
        #     assets_info = AssetsInfo()
        #     assets_info.hostname = request.POST.get('ip','')
        #     assets_info.hostname = request.POST.get('hostname','')
        #     assets_info.cpu_cores = request.POST.get('cpu_cores','')
        #     assets_info.mem_total = request.POST.get('mem_total','')
        #     assets_info.disk_total = request.POST.get('disk_total','')
        #     assets_info.cpu_status = request.POST.get('cpu_status','')
        #     assets_info.mem_status = request.POST.get('mem_status','')
        #     assets_info.disk_status = request.POST.get('disk_status','')
        #     assets_info.system_time = request.POST.get('system_time','')
        #     assets_info.up_time = request.POST.get('v','')
        #     assets_info.system_ver = request.POST.get('system_ver','')
        #     assets_info.mac_address = request.POST.get('mac_address','')
        #     assets_info.sn = request.POST.get('sn','')
        #     assets_info.manufacturer = request.POST.get('manufacturer','')
        #     assets_info.product = request.POST.get('product','')
        #     assets_info.cpu_info = request.POST.get('cpu_info','')
        #     assets_info.save()


# 一键更新全部资产信息
class UpdateAllAssetsView(View):
    def post(self, request):
        obj = AssetsInfo.objects.all()
        for i in obj:
            linux_list = [i.ip]
            user_list = [i.ssh_user]
            port_list = [i.ssh_port]
            passwd_list = [i.ssh_passwd]
            glm = GetLinuxMethod()
            assets_dict = glm.try_ssh_login(linux_list, user_list, port_list, passwd_list)
            update_dict = {}
            for ip, values in assets_dict.items():
                update_dict['hostname'] = values[4]
                update_dict['cpu_cores'] = values[5]
                update_dict['mem_total'] = values[6]
                update_dict['disk_total'] = values[7]
                update_dict['cpu_status'] = values[8]
                update_dict['mem_status'] = values[9]
                update_dict['disk_status'] = values[10]
                update_dict['system_time'] = values[11]
                update_dict['up_time'] = values[12]
                update_dict['system_ver'] = values[13]
                update_dict['mac_address'] = values[14]
                update_dict['sn'] = values[15]
                update_dict['manufacturer'] = values[16]
                update_dict['product'] = values[17]
                update_dict['cpu_info'] = values[18]
                # print(update_dict)
            AssetsInfo.objects.filter(ip=i.ip).update(**update_dict)
        return HttpResponse('更新成功')


# 资产详情
class AssetsDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        obj = AssetsInfo.objects.filter(id=id).first()
        return render(request, 'assets/detail.html', locals())

    def post(self, request):
        pass


# webssh远程连接
class AssetsWebSshsView(View):
    def get(self, request):
        url = "http://{0}/?".format(WSSH_IP)
        return render(request, 'assets/webssh.html', locals())

    def post(self, request):
        if 'startwebssh' in request.POST:
            os.system("nohup wssh --address='0.0.0.0' --port=8000 &")
            import time
            time.sleep(1)
            return redirect('/assets/websshs/')
        elif 'stopwebssh' in request.POST:
            os.system("kill -9 `netstat -ntlp|grep 8000|awk -F ' ' '{print $NF}'|awk -F'/' '{print $1}'`")
            return redirect('/assets/websshs/')
        else:
            ip = request.POST.get('ip').strip()
            # print(ip)
            obj = AssetsInfo.objects.filter(ip=ip).first()
            user = obj.ssh_user
            port = obj.ssh_port
            passwd = base64.b64encode(obj.ssh_passwd.encode('utf-8')).decode('utf-8')
            # print(passwd)
            # print user,port,passwd,ip
            url = "http://{4}/?hostname={0}&username={1}&password={2}&port={3}".format(ip, user, passwd, port, WSSH_IP)
            return HttpResponse(url)


# 资产导出Excle
class AssetsExportView(LoginRequiredMixin, View):
    def post(self, request):
        # new一个文件
        wb = xlwt.Workbook(encoding='utf-8')
        # new一个sheet
        sheet = wb.add_sheet(u'资产信息', cell_overwrite_ok=True)
        for i in range(1, 13):
            sheet.col(i).width = 256 * 15
        tall_style = xlwt.easyxf('font:height 600')  # 36pt
        first_row = sheet.row(0)
        first_row.set_style(tall_style)

        # 维护一些样式， style_heading, style_body, style_red, style_green
        style_heading = xlwt.easyxf("""
        font:
          name Arial,
          colour_index white,
          bold on,
          height 200;
        align:
          wrap off,
          vert center,
          horiz center;
        pattern:
          pattern solid,
          fore-colour 0x19;
        borders:
          left THIN,
          right THIN,
          top THIN,
          bottom THIN;
        """
                                    )
        style_body = xlwt.easyxf("""
        font:
          name Arial,
          bold off,
          height 0XA0;
        align:
          wrap on,
          vert center,
          horiz left;
        borders:
          left THIN,
          right THIN,
          top THIN,
          bottom THIN;
        """
                                 )
        # 写标题栏
        sheet.write(0, 0, '序号', style_heading)
        sheet.write(0, 1, 'IP地址', style_heading)
        sheet.write(0, 2, '操作系统主机名', style_heading)
        sheet.write(0, 3, '操作系统版本', style_heading)
        sheet.write(0, 4, 'ssh登录的端口', style_heading)
        sheet.write(0, 5, 'ssh登录的用户', style_heading)
        sheet.write(0, 6, 'ssh登录的用户', style_heading)
        sheet.write(0, 7, 'mac地址列表', style_heading)
        sheet.write(0, 8, 'SN－主机的唯一标示', style_heading)
        sheet.write(0, 9, '制造商', style_heading)
        sheet.write(0, 10, 'cpu核数', style_heading)
        sheet.write(0, 11, '内存总大小', style_heading)
        sheet.write(0, 12, '磁盘总大小', style_heading)
        row = 1
        obj = AssetsInfo.objects.all()
        for usa in obj:
            sheet.write(row, 0, row, style_body)
            sheet.write(row, 1, usa.ip, style_body)
            sheet.write(row, 2, usa.hostname, style_body)
            sheet.write(row, 3, usa.system_ver, style_body)
            sheet.write(row, 4, usa.ssh_port, style_body)
            sheet.write(row, 5, usa.ssh_user, style_body)
            sheet.write(row, 6, usa.ssh_passwd, style_body)
            sheet.write(row, 7, usa.mac_address, style_body)
            sheet.write(row, 8, usa.sn, style_body)
            sheet.write(row, 9, usa.manufacturer, style_body)
            sheet.write(row, 10, usa.cpu_cores, style_body)
            sheet.write(row, 11, usa.mem_total, style_body)
            sheet.write(row, 12, usa.disk_total, style_body)
            row += 1

        # 设置HttpResponse的类型
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename=assets.xls'

        # 写出到IO
        output = BytesIO()
        wb.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
        return response


# ibmstatus，该功能基于爬虫，且只针对IBM服务器
class IbmStatusView(LoginRequiredMixin, View):

    def get(self, request):
        obj = IbmStatus.objects.all()
        return render(request, 'assets/ibmstatus.html', locals())

    def post(self, request):
        if 'localpost' in request.POST:
            ibm_list = getIbmList()
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for res_dict in ibm_list:
                for ip, j in res_dict.items():
                    IbmStatus.objects.filter(ip=ip).update(
                        Processors=j['Processors'],
                        Disks=j['Disks'],
                        System=j['System'],
                        Memory=j['Memory'],
                        Power_Modules=j['Power Modules'],
                        Cooling_Devices=j['Cooling Devices'],
                        Adapters=j['Adapters'],
                        date_time=date_time,
                    )
            return HttpResponse('updateok')
        else:
            pass


# 扫描IP
class IpScanView(View):
    def get(self, request):
        return render(request, 'assets/ipscan.html', locals())

    def post(self, request):
        if 'networks' in request.POST:
            ip = request.POST.get('ip')
            if '/24' in ip:
                ipscan = ScanHosts()
                status = ipscan.allHost(ip)
                return render(request, 'assets/ipscan.html', locals())
            else:
                status = ['请输入正确的格式，如 192.168.5.0/24']
                return render(request, 'assets/ipscan.html', locals())
        elif 'network' in request.POST:
            ip = request.POST.get('ip1')
            ipscan = ScanHosts()
            status = ipscan.oneHost(ip)
            return render(request, 'assets/ipscan.html', locals())
