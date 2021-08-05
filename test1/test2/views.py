from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import requests as r
import os
from pathlib import Path
import cv2
import sqlite3

BASE_DIR = Path(__file__).resolve().parent.parent
media = os.path.join(BASE_DIR, 'media/')


def index(request):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM images''')
    images = cursor.fetchall()
    img = []
    try:
        for i in images:
            for n in i:
                img.append(n)
        count_images = len(images)
    except:
        count_images = 0
    return render(request, 'index.html', {'count': count_images, 'images': img})


def add(request):
    if request.POST.get('url_img') and request.FILES:
        return render(request, 'add.html', {'error': 0})
    if request.POST.get('url_img'):
        img = r.get(request.POST.get('url_img'))
        names = str(request.POST.get('url_img')).split('/')[-1]
        img_name = os.path.join(media, str(request.POST.get('url_img')).split('/')[-1])
        img_file = open(img_name, 'wb')
        img_file.write(img.content)
        img_file.close()
        save_db(names)
        return redirect(f'preview?fileName={names}')
    elif request.method == 'POST' and request.FILES:
        file = request.FILES['myfile1']
        fs = FileSystemStorage()
        fs.save(file.name, file)
        save_db(file.name)
        return redirect(f'preview?fileName={file.name}')
    return render(request, 'add.html')


def preview(request):
    filename = request.GET.get('fileName')
    image = cv2.imread(media+filename)
    if request.GET.get('width') and request.GET.get('height'):
        cv2.imwrite(f"{media}test.png", resizing(img=image, new_width=int(request.GET.get('width')), new_height=int(request.GET.get('height'))))
        return render(request, 'preview.html', {'image.shape': image.shape, 'imgName': filename, 'img': 'test.png'})
    elif request.GET.get('width'):
        cv2.imwrite(f"{media}test.png", resizing(img=image, new_width=int(request.GET.get('width'))))
        return render(request, 'preview.html', {'image.shape': image.shape, 'imgName': filename, 'img': 'test.png'})
    elif request.GET.get('height'):
        cv2.imwrite(f"{media}test.png", resizing(img=image, new_height=int(request.GET.get('height'))))
        return render(request, 'preview.html', {'image.shape': image.shape, 'imgName': filename, 'img': 'test.png'})
    return render(request, 'preview.html', {'image.shape': image.shape, 'imgName': filename, 'img': filename})


def resizing(img, new_width=None, new_height=None, interp=cv2.INTER_LINEAR):
    h, w = img.shape[:2]
    if new_width is None and new_height is None:
        return img
    if new_width is None:
        ratio = new_height / h
        dimension = (int(w * ratio), new_height)
    else:
        ratio = new_width / w
        dimension = (new_width, int(h * ratio))
    return cv2.resize(img, dimension, interpolation=interp)


def save_db(file_name):
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO images (name) VALUES ("{file_name}")')
    conn.commit()
    conn.close()
