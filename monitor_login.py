docfile_log = open("/var/log/auth.log").readlines()
ghidulieu = open("/root/login_monitor.txt", 'a')
docfile_dl_f_ssh = open("/root/login_monitor.txt").readlines()

f_ssh_line = []
list_so_sanh = []

dl_f_ssh_date_list = []

tukhoa1 = ": Failed password"
tukhoa11 = "invalid"

tukhoa2 = ": FAILED LOGIN"
tukhoa22 = "UNKNOWN"

tukhoa3 = "pam_unix(login:session): session opened"

tukhoa4 = ": Accepted password"

check1 = False
check2 = False
check3 = False
check4 =False

for i in range(0,len(docfile_log)):
    if tukhoa1 in docfile_log[i] or tukhoa2 in docfile_log[i] or tukhoa3 in docfile_log[i] or tukhoa4 in docfile_log[i]:
        f_ssh_line.append(docfile_log[i])


for i in range(0,len(docfile_dl_f_ssh)):
    k = docfile_dl_f_ssh[i].split(" ")
    sosanh1 = k[0]+" "+k[2]+" "+k[3]
    list_so_sanh.append(sosanh1)
#    print sosanh1
#    dl_f_ssh_date_list.append(docfile_dl_f_ssh[i].split(" ")[0])


#ghidulieu.truncate()
for i in f_ssh_line:
    a= True
    ngaythang = i.split(" ")
    sosanh2 = ngaythang[0]+" "+ngaythang[2]+" "+ngaythang[3]
#    print sosanh2

    for j in range(0,len(list_so_sanh)):
        if sosanh2 == list_so_sanh[j]:
            a= False
            break;
    if a:
        ghidulieu.write(i)


#    ghidulieu.write(i)
ghidulieu.close()



txt = open("/root/login_monitor.txt")

fail_ssh_last = []
cut_fail_ssh_last = []

fail_direct_login_last = []
cut_fail_direct_login_last = []

success_ssh_last = []
cut_success_ssh_last = []

success_direct_login_last = []
cut_success_direct_login_last = []

docfile = txt.readlines()




for i in range(0,len(docfile)):
    if tukhoa1 in docfile[i]:
        fail_ssh_last.append(docfile[i])

print "{\n"
print '\t"data":[\n\n'
if fail_ssh_last:
    cut_fail_ssh_last=fail_ssh_last[len(fail_ssh_last)-1].split(" ")
    if tukhoa11 in cut_fail_ssh_last:
        print "\t{\n"
        print '\t\t"{#LOGIN1}":"FAIL SSH",' +   '\t\t"{#USER}":\"Khong ton tai user '+str(cut_fail_ssh_last[11])+"\","+'\t\t"{#IP}":\"from '+str(cut_fail_ssh_last[13])+" port "+str(cut_fail_ssh_last[15])+"\""
        print "\t},\n"

    else:

        print "\t{\n"
        print '\t\t"{#LOGIN1}":"FAIL SSH",' +  '\t\t"{#USER}":\"'+"User "+str(cut_fail_ssh_last[9])+"\","+ '\t\t"{#IP}":\" from'+str(cut_fail_ssh_last[11])+" port "+str(cut_fail_ssh_last[13])+"\""
        print "\t},\n"





for i in range(0,len(docfile)):
    if tukhoa2 in docfile[i]:
        fail_direct_login_last.append(docfile[i])

if fail_direct_login_last:
    cut_fail_direct_login_last=fail_direct_login_last[len(fail_direct_login_last)-1].split(" ")
    if tukhoa22 in cut_fail_direct_login_last:
        print "\t{\n"
    
        print '\t\t"{#LOGIN2}":"FAIL DIRECT LOGIN",' +   '\t\t"{#USER}":\"Khong ton tai user '+"\","+'\t\t"{#IP}":\"'+" Authentication failure "+"\""
        print "\t},\n"

    else:
        print "\t{\n"
        print '\t\t"{#LOGIN2}":"FAIL DIRECT LOGIN",' +  '\t\t"{#USER}":\"'+"User "+str(cut_fail_direct_login_last[12])+"\","+ '\t\t"{#IP}":\"'+" Authentication failure "+"\""
        print "\t},\n"



for i in range(0,len(docfile)):
    if tukhoa3 in docfile[i]:
        success_direct_login_last.append(docfile[i])
if success_direct_login_last:
    cut_success_direct_login_last = success_direct_login_last[len(success_direct_login_last)-1].split(" ")

    print "\t{\n"
    
    print '\t\t"{#LOGIN3}":"SUCCESS DIRECT LOGIN",' +  '\t\t"{#USER}":\"'+"User "+str(cut_success_direct_login_last[11])+"\","+ '\t\t"{#IP}":\"'+" by "+str(cut_success_direct_login_last[12])+"\""
    print "\t},\n"



for i in range(0,len(docfile)):
    if tukhoa4 in docfile[i]:
        success_ssh_last.append(docfile[i])

if success_ssh_last:        
    cut_success_ssh_last=success_ssh_last[len(success_ssh_last)-1].split(" ")

    print "\t{\n"
    print '\t\t"{#LOGIN4}":"SUCCESS SSH",' +  '\t\t"{#USER}":\"'+"User "+str(cut_success_ssh_last[9])+"\","+ '\t\t"{#IP}":\"from '+str(cut_success_ssh_last[10])+" port "+str(cut_success_ssh_last[12])+"\""
    print "\t}\n"
    print "\n\t]\n"
    print "}\n"
