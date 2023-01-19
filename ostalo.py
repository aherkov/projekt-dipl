import os

ostalo_links = []
with open("train_links.txt", 'r') as f:
    for line in f.readlines():
        if line.split('/')[5].strip() not in os.listdir('images'):
            ostalo_links.append(line)

with open("ostalo.txt", 'w') as f:
    [f.write(photo_url + '\n') for photo_url in set(ostalo_links)]
