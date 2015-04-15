#I.Đặt vấn đề

Một server public ra ngoài mạng internet đứng trước nguy cơ mất dữ liệu khi có nhiều cuộc tấn công cố gắng truy cập vào hệ thống với tài khoản quản trị nhằm chiếm quyền sử dụng, thao tác với hệ thống. Vì vậy cần có biện pháp phòng ngừa, cảnh báo khi có sự kiện đăng nhập trực tiếp hoặc SSH.

#II. Giải pháp


Khi có sự kiện đăng nhập trực tiếp hay từ xa hệ thống sẽ ghi lại nhật ký trong file log

```sh 
tail /var/log/auth.log
```

<img src=http://i.imgur.com/ycnoVaF.png width="80%" height="80%" border="1">

Giải pháp được đưa ra là viết chương trình lấy thông tin trong file log này, thông tin cần lấy gồm có

- Số lần đăng nhập ssh thành công bao gồm user đăng nhập và ip máy đăng nhập từ xa

- Số lần đăng nhập bằng ssh thất bại, bao gồm cả thông tin user, user không tồn tại, IP của máy đăng nhập từ xa, port

- Số lần đăng nhập trực tiếp thành công, bao gồm user đăng nhập, và đăng nhập trên tty của user nào

- Số lần đăng nhập trực tiếp thất bại, gồm có cả user đăng nhập

Tất cả thông tin này chương trình sẽ chuyển sang định sang json và đẩy lên server, server sẽ dựa vào số biến động những số liệu này để gửi cảnh báo về cho người quản trị

Tuy nhiên hệ thống sẽ xóa file log định kỳ nên để số lần đăng nhập đúng chương trình sẽ ghi dữ liệu sang file text

# III. Triển khai

## 3.1 Trên máy Zabbix Agent

Tải script và tạo thư mục chứa file script:

```sh
wget https://raw.githubusercontent.com/thanhha123/zabbix_monitor_login/master/monitor_login.py

mkdir -p /var/tools/zabbix/monitor/

cp login_monitor.py /var/tools/zabbix/monitor/login_monitor.py
chmod +x /var/tools/zabbix/monitor/login_monitor.py
```

Chạy script dữ liệu sẽ dưới dạng file JSON


<img src=http://i.imgur.com/gRAAgAM.png width="80%" height="80%" border="1">

Sau khi chạy script xong tại thư mục /var/zabbix/monitor/ sẽ sinh ra file login_monitor.txt chứa các dòng dữ liệu trong file log để lưu dữ liệu khi file log bị xóa

Thêm các UserParameter vào file cấu hình /etc/zabbix/zabbix_agentd.conf

```sh 
echo " UserParameter=direct.log.fail[*],cat /var/tools/zabbix/monitor/login_monitor.txt |grep \": FAILED LOGIN\"|wc -l" >> /etc/zabbix/zabbix_agentd.conf

echo "UserParameter=ssh.log.success[*],cat /var/tools/zabbix/monitor/login_monitor.txt |grep \": Accepted password\"|wc -l">>/etc/zabbix/zabbix_agentd.conf

echo "UserParameter=direct.log.success[*],cat /var/tools/zabbix/monitor/login_monitor.txt |grep \"pam_unix(login:session): session opened\"|wc -l" >> /etc/zabbix/zabbix_agentd.conf


echo "UserParameter=direct.log.fail[*],cat /var/tools/zabbix/monitor/login_monitor.txt |grep \": Failed password\"|wc -l" >> /etc/zabbix/zabbix_agentd.conf

echo "UserParameter=login.monitor,/usr/bin/python /var/tools/zabbix/monitor/login_monitor.py" >> /etc/zabbix/zabbix_agentd.conf

```


Khởi động lại Zabbix Agent:

```sh
service zabbix_agent restart
```

## 3.2 Trên Zabbix Server

Bước 1: Tạo host với IP máy cần giám sát

<img src=http://i.imgur.com/JJVfJKb.png width="80%" height="80%" border="1">

Bước 2: Tạo Discovery rules trong host vừa khởi tạo với MACRO LOGIN

<img src=http://i.imgur.com/xTaLfKz.png width="80%" height="80%" border="1">

Bước 3: Khởi tạo các item

<img src=http://i.imgur.com/XObgWOc.png width="80%" height="80%" border="1">


Kết quả:

<img src=http://i.imgur.com/mbousuT.png width="80%" height="80%" border="1">

