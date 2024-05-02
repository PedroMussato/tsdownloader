import requests
import os
from tkinter import Tk, Label, Entry, Button
import time

"https://cfvod.kaltura.com/scf/hls/p/1612851/sp/161285100/serveFlavor/entryId/0_g4xnlfs7/v/2/ev/7/flavorId/0_a1y5kx98/name/a.mp4/seg-##n##-v1-a1.ts?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9jZnZvZC5rYWx0dXJhLmNvbS9zY2YvaGxzL3AvMTYxMjg1MS9zcC8xNjEyODUxMDAvc2VydmVGbGF2b3IvZW50cnlJZC8wX2c0eG5sZnM3L3YvMi9ldi83L2ZsYXZvcklkLzBfYTF5NWt4OTgvbmFtZS9hLm1wNC8qIiwiQ29uZGl0aW9uIjp7IkRhdGVMZXNzVGhhbiI6eyJBV1M6RXBvY2hUaW1lIjoxNzE0NzU3MTQ0fX19XX0_&Signature=Hl3zEUv7QEwoVN~5ALYy1OEBnN5~wKxeLm6y69p1~R~ya0pilMFFQGcPwflBiFc9wgeTUqMQ44bTLzCxhn6OVyjKsCmZn-Nv4wGqFohIvKZGr3aD9wmWQv0qxdtAe6nzj7LW3LlgxbiIq3IvtT3rBsdOqWjGZooW1ePZkIflfqXliGnB~Qqd4aXF3WwHEzPPK7gfXcNsfl90pykGmoWIt~Cnk5-tkVH9AJRbMHd7wbDD284CU2pNkMCDMvV-kuc7zAT0FUjvmqyzaPvstXbGknF~KSC2h6I72by7AeAdqCH08KVy8qGfLu-2EqWklxF0DxlkSKq7vjvhEDsir-YuKA__&Key-Pair-Id=APKAJT6QIWSKVYK3V34A"


def downloadTsFiles(url, r, referer='https://google.com/', user_agent='Chrome/89.0.4389.90', output_name='output', work_dir=os.path.abspath('.'), output_dir='.'):

    if not referer:
        referer = 'https://google.com/'
    if not user_agent:
        user_agent = 'Chrome/89.0.4389.90'
    if not output_name:
        output_name = 'output'
    else:
        on = ''
        for i in output_name:
            if not i.lower() in 'abcdefghijklmnopqrstuvwxyz':
                on += '_'
            else:
                on += i

    headers = {
        'User-Agent': user_agent,
        'Referer': referer
    }

    input_files = []

    output_file = os.path.join(output_dir, output_name)


    if r == -1:
        c = 0
        while True:
            response = requests.get(url.replace('##n##', str(c)), headers=headers)

            if response.status_code == 404 and c != 0:
                break

            with open(os.path.join(work_dir, f'video{c}.ts'), 'wb') as f:
                f.write(response.content)

            input_files.append(os.path.join(work_dir, f'video{c}.ts'))

            print(f"done {c}")
            c += 1

    else:
        for i in range(r+1):
            response = requests.get(url.replace('##n##', str(i)), headers=headers)
            with open(os.path.join(work_dir, f'video{i}.ts'), 'wb') as f:
                f.write(response.content)

            input_files.append(os.path.join(work_dir, f'video{i}.ts'))

            print(f"done {i}/{r}")

    
    os.popen(f'ffmpeg -i "concat:{"|".join(input_files)}" -c copy {output_file}.mp4')

    for i in range(10,0,-1):
        print(i)
        time.sleep(1)
    
    for i in input_files:
        os.remove(i)

root = Tk()

root.title = "Download *.ts"

l1 = Label(root, text="User agent (não obrigatório)")
e1 = Entry(root, width=50)
e1.insert(0, 'Chrome/89.0.4389.90')

l2 = Label(root, text="Referer (não obrigatório)")
e2 = Entry(root, width=50)
e2.insert(0, 'https://google.com/')

l3 = Label(root, text="Numero do ultimo pacote (não obrigatório)")
e3 = Entry(root, width=50)
e3.insert(0, -1)

l4 = Label(root, text="URL modificada (use '##n##')")
e4 = Entry(root, width=50)

l6 = Label(root, text="Diretorio de trabalho")
e6 = Entry(root, width=50)
e6.insert(0, os.path.abspath('.'))

l7 = Label(root, text="Diretorio de saida")
e7 = Entry(root, width=50)
e7.insert(0, os.path.abspath('.'))

l5 = Label(root, text="Nome de saída")
e5 = Entry(root, width=50)
e5.insert(0, 'output')

b1 = Button(root, text="Ok!", command=lambda : downloadTsFiles(e4.get(), int(e3.get()), e2.get(), e1.get(), e5.get(), e6.get(), e7.get()))

l1.pack()
e1.pack()
l2.pack()
e2.pack()
l3.pack()
e3.pack()
l4.pack()
e4.pack()
l5.pack()
e5.pack()
l6.pack()
e6.pack()
l7.pack()
e7.pack()

b1.pack()

root.mainloop()
