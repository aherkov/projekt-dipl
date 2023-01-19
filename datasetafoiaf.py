# import os
#
# train = ["./images/train/" + x.replace('txt', 'png\n') for x in os.listdir('train') if x[-3:] == "txt"]
# val = ["./images/val/" + x.replace('txt', 'png\n') for x in os.listdir('val') if x[-3:] == "txt"]
# test = ["./images/test/" + x.replace('txt', 'png\n') for x in os.listdir('test') if x[-3:] == "txt"]
#util
# with open('../split_txt/train.txt', 'w') as f:
#     f.writelines(train)
#
# with open('../split_txt/test.txt', 'w') as f:
#     f.writelines(test)
#
# with open('../split_txt/val.txt', 'w') as f:
#     f.writelines(val)

sh = """
for i in $( ls )
do mv $i $i.png
done
"""

for i in ["train", "test", "val"]:
    with open('./dataset/images/' + i + '/script.sh', 'w') as file:
        file.write(sh)
