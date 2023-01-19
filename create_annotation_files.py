with open('./train_links.txt', 'r') as f:
    links = f.readlines()
with open('./train_annotations.txt', 'r') as f:
    annotations = f.readlines()

for link, annotation in zip(links, annotations):
    with open('./annotations/' + link.strip().split('/')[-1] + ".txt", 'w') as f:
        for i, a in enumerate(annotation.split(' - ')):
            if i == len(annotation.split(' - ')) - 1:
                continue
            else:
                f.write(a + "\n")
