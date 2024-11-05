import subprocess


#Using_Mount = subprocess.run("docker ps --format \"{{.Mounts}}\"")
Using_Mount_string = subprocess.run(['docker' , 'ps' ,'--format','{{.Mounts}}'] , capture_output=True, text=True)
# 顯示命令的標準輸出
# print(Using_Mount_string.stdout)

Using_Mount_List = Using_Mount_string.stdout.split('\n')
Using_Mount_List = [ v.replace('…','').strip().split(',')[0]  for v in Using_Mount_List if not (v.startswith('/')) ]
Using_Mount_List.remove('')
print('[Using_Mount_List]('+ str(len(Using_Mount_List))+ ')' ) 
print(Using_Mount_List)


Docker_Volumns_string = subprocess.run(['docker' , 'volume' ,'list'] , capture_output=True, text=True)
# print(Docker_Volumns_string.stdout)

Docker_Volumns_List = Docker_Volumns_string.stdout.split('\n')
Docker_Volumns_List.remove('DRIVER    VOLUME NAME')
Docker_Volumns_List.remove('')
Docker_Volumns_List =[v.replace("local","").strip()  for v in Docker_Volumns_List]
print('[Docker_Volumns_List]('+ str(len(Docker_Volumns_List))+ ')' ) 
print(Docker_Volumns_List)

print('===================================================')
NoUse_Volumes = [b for b in Docker_Volumns_List if not any(b.startswith(a) for a in Using_Mount_List)]

print('[NoUse_Volumes]('+ str(len(NoUse_Volumes))+ ')' ) 
print(NoUse_Volumes)  

print('===================================================')
print('[Volume Ls Show & Delete]')

for i , vol in enumerate(NoUse_Volumes):
   
    print('[' ,i , ']' ,vol)
    subprocess.run(
    ['docker', 'run', '--rm', '-v', vol + ':/vdata',
     '-v', './vresult:/vresult', 
     'ubuntu', 'sh', '-c', 'ls /vdata > /vresult/ls.txt'],
    capture_output=True, text=True
    )
    

    f = open("vresult/ls.txt", "r")
    lines = f.readlines()
    f.close()
    for line in lines:
        print(line, end="")


    print("Delete this Volume?(Y/N) ")
    Delete_Volumn = input('Y')

    if Delete_Volumn == 'Y' :
        Process_Del_Vol = subprocess.run(    ['docker', 'volume', 'rm', vol ],    capture_output=True, text=True)