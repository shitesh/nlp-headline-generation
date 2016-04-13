# -*- coding: utf-8 -*-
import gzip,os
import codecs


n=0
for root, dirs, files in os.walk('S:\\thirdsem\NLP\\format_corpus\in_files', topdown=False):
    for name in files:
        file = os.path.join(root, name)

        with gzip.open(file, 'rb') as f:
            length = sum(1 for line in gzip.open('C:\Users\Surabhi\Desktop\hindi\ext_test\\00002.htm.gz'))
            file_name = "out200711,12\out"+str(n)+".txt"
            n+=1
            f1=codecs.open(file_name,"w+")
            for i in range(0,30):
                #print i
                file_content = f.readline()
                if(i==4):
                    #print file_content
                    head = "<Headline>"+file_content+"</Headline>\n<text>"
                    f1.write(head)
                if i>4 :
                    if "Shop Gifts Online" not in file_content:
                        f1.write(file_content)
                    else:
                        break
            f1.write("</text>")
            f.close()
