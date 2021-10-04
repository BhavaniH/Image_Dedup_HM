import base64
import hashlib
import io
import os
import cv2
import Crypto
import sys
import numpy as np
import rehash

sys.modules['Crypto'] = Crypto
from PIL import Image
from starlette.responses import FileResponse
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Database.base import engine
import pandas as pd
from Database.Models import img_keys, img_tags, img_images, img_cloud_tags, img_cloud_cipher, img_enc_tags
from starlette.responses import StreamingResponse
import json
from dedup.integrityBlocks import Block, Blockchain

img_no = 1
conn = engine.connect()
blockchain = Blockchain()


def getKey(image_block_byte):
    hasher = SHA256.new(image_block_byte)
    return hasher.digest()


def encrypt(key, image):
    """ Encryption function"""
    iv = b'\xfa\xb6.4\xe8\xa6B\xe4\xef\xf7?x4\x16\x8e\x0c'
    cipher = AES.new(key, AES.MODE_CFB, iv)
    #print("Key Value of cipher text:",key , len(key))
    cipher_text = cipher.encrypt(image)
    #print("Image Cipher_text: ", cipher_text, type(cipher_text), len(cipher_text))
    return cipher_text


def decrypt(key, cipher_text):
    iv = b'\xfa\xb6.4\xe8\xa6B\xe4\xef\xf7?x4\x16\x8e\x0c'
    #print("Key Value of De-cipher text:", key, len(key))
    cipher = AES.new(key, AES.MODE_CFB, iv)
    plain_text = cipher.decrypt(cipher_text.encode('utf8'))
    #print("Image plain_text: ", plain_text, type(plain_text), len(plain_text))
    plain_array = np.ndarray((20,20,3),np.int,plain_text)
    #print("Plain_array of image:", plain_array, type(plain_array), plain_array.shape)
    return plain_text


def imgcrop(input, xPieces, yPieces, filename):
    """ Function for Image Blocks creation"""
    global img_no
    im = Image.open(io.BytesIO(input))
    #print("Im value:", im, type(im), im.tobytes)
    with io.BytesIO() as buf:
        im.save(buf, 'jpeg')
        #im.save(buf, 'tiff')
        #im.save(buf, 'png')
        image_bytes = buf.getvalue()
    imgwidth, imgheight = im.size
    height = imgheight // yPieces
    width = imgwidth // xPieces
    file_name = filename.split(".")[0]
    file_extension = filename.split(".")[-1]
    blocks = []
    keys = []
    ciphers = []
    tags = []
    chain_data = []
    query1 = img_images.insert().values(imagename=filename,image=image_bytes)
    conn.execute(query1)
    #print("img_images:",type(img_images))
    query2 = img_enc_tags.insert().values(filename=filename)
    conn.execute(query2)
    df1 = pd.read_sql('SELECT * FROM img_enc_tags', con=conn)
    print("Dataframe object:", df1)
    query = img_cloud_tags.insert().values(filename=filename)
    conn.execute(query)
    df = pd.read_sql('SELECT * FROM img_cloud_tags', con=conn)
    #print("Dataframe object:", df)

    try:
        block_no = 1
        for i in range(0, yPieces):
            for j in range(0, xPieces):
                box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
                a = im.crop(box)
                file_path = "images/blocks/" + file_name + "." + str(img_no) + "-" + str(
                    block_no) + "." + file_extension
                a.save(file_path)
                blocks.append(a)
                block_no = block_no + 1
        img_no = img_no + 1
        for file in os.listdir("images/blocks/"):
            if file.split(".")[0] == file_name:
                img = cv2.imread(os.path.join(f"images/blocks/", file))
                #print("IMG:",img,type(img),img.shape)
                if img is not None:
                    bytesarray = Image.fromarray(img).tobytes()
                    #print("bytesarray:", bytesarray, type(bytesarray))
                    key = getKey(bytesarray)
                    #print("key:", key, len(key), type(key))
                    keys.append(key)
                    c_text = encrypt(key, bytesarray)
                    #print("c_text: ",c_text, len(c_text),type(c_text))
                    ciphers.append(str(c_text))
                    tag = getKey(c_text)
                    #print("tag: ",tag, len(tag),type(tag))
                    tags.append(str(tag))

        for i in tags:
            blockchain.add_new_transaction(i)
            blockchain.mine()

        for block in blockchain.chain:
            chain_data.append(block.__dict__)
        #data1 = json.dumps({"length": len(chain_data), "chain": chain_data})
        print("Data1:", chain_data)

        result_keys = img_keys.insert().values(
            filename=filename,
            block_1=keys[0],
            block_2=keys[1],
            block_3=keys[2],
            block_4=keys[3],
            block_5=keys[4],
            block_6=keys[5],
            block_7=keys[6],
            block_8=keys[7],
            block_9=keys[8],
            block_10=keys[9],
            block_11=keys[10],
            block_12=keys[11],
            block_13=keys[12],
            block_14=keys[13],
            block_15=keys[14],
            block_16=keys[15]
        )
        conn.execute(result_keys)
        result_tags = img_tags.insert().values(
            filename=filename,
            block_1=tags[0],
            block_2=tags[1],
            block_3=tags[2],
            block_4=tags[3],
            block_5=tags[4],
            block_6=tags[5],
            block_7=tags[6],
            block_8=tags[7],
            block_9=tags[8],
            block_10=tags[9],
            block_11=tags[10],
            block_12=tags[11],
            block_13=tags[12],
            block_14=tags[13],
            block_15=tags[14],
            block_16=tags[15]
        )
        conn.execute(result_tags)
        result_img_cipher = img_cloud_cipher.insert().values(
            filename=filename,
            block_1=ciphers[0],
            block_2=ciphers[1],
            block_3=ciphers[2],
            block_4=ciphers[3],
            block_5=ciphers[4],
            block_6=ciphers[5],
            block_7=ciphers[6],
            block_8=ciphers[7],
            block_9=ciphers[8],
            block_10=ciphers[9],
            block_11=ciphers[10],
            block_12=ciphers[11],
            block_13=ciphers[12],
            block_14=ciphers[13],
            block_15=ciphers[14],
            block_16=ciphers[15]
        )
        conn.execute(result_img_cipher)

        filenames = list(df['filename'])
        # print("filename", filenames)
        b1 = list(df['block_1'])
        # print("block b1", b1)
        for i in b1:
            if i == chain_data[1].get('hash'):
                ind = b1.index(i)
                df.loc[df['filename'] == filename, 'block_1'] = filenames[ind] + "#" + "block_1"
                break
            else:
                df.loc[df['filename'] == filename, 'block_1'] = chain_data[1].get('hash')
                print("value of i :", i, chain_data[1].get('hash'))

        b2 = list(df['block_2'])
        for i in b2:
            if i == chain_data[2].get('hash'):
                ind = b2.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_2'] = filenames[ind] + "#" + "block_2"
                break
            else:
                df.loc[df['filename'] == filename, 'block_2'] = chain_data[2].get('hash')

        b3 = list(df['block_3'])
        for i in b3:
            if i == chain_data[3].get('hash'):
                ind = b3.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_3'] = filenames[ind] + "#" + "block_3"
                break
            else:
                df.loc[df['filename'] == filename, 'block_3'] = chain_data[3].get('hash')

        b4 = list(df['block_4'])
        for i in b4:
            if i == chain_data[4].get('hash'):
                ind = b4.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_4'] = filenames[ind] + "#" + "block_4"
                break
            else:
                df.loc[df['filename'] == filename, 'block_4'] = chain_data[4].get('hash')

        b5 = list(df['block_5'])
        for i in b5:
            if i == chain_data[5].get('hash'):
                ind = b5.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_5'] = filenames[ind] + "#" + "block_5"
                break
            else:
                df.loc[df['filename'] == filename, 'block_5'] = chain_data[5].get('hash')

        b6 = list(df['block_6'])
        for i in b6:
            if i == chain_data[6].get('hash'):
                ind = b6.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_6'] = filenames[ind] + "#" + "block_6"
                break
            else:
                df.loc[df['filename'] == filename, 'block_6'] = chain_data[6].get('hash')

        b7 = list(df['block_7'])
        for i in b7:
            if i == chain_data[7].get('hash'):
                ind = b7.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_7'] = filenames[ind] + "#" + "block_7"
                break
            else:
                df.loc[df['filename'] == filename, 'block_7'] = chain_data[7].get('hash')

        b8 = list(df['block_8'])
        for i in b8:
            if i == chain_data[8].get('hash'):
                ind = b8.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_8'] = filenames[ind] + "#" + "block_8"
                break
            else:
                df.loc[df['filename'] == filename, 'block_8'] = chain_data[8].get('hash')

        b9 = list(df['block_9'])
        for i in b9:
            if i == chain_data[9].get('hash'):
                ind = b9.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_9'] = filenames[ind] + "#" + "block_9"
                break
            else:
                df.loc[df['filename'] == filename, 'block_9'] = chain_data[9].get('hash')

        b10 = list(df['block_10'])
        for i in b10:
            if i == chain_data[10].get('hash'):
                ind = b10.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_10'] = filenames[ind] + "#" + "block_10"
                break
            else:
                df.loc[df['filename'] == filename, 'block_10'] = chain_data[10].get('hash')

        b11 = list(df['block_11'])
        for i in b11:
            if i == chain_data[11].get('hash'):
                ind = b11.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_11'] = filenames[ind] + "#" + "block_11"
                break
            else:
                df.loc[df['filename'] == filename, 'block_11'] = chain_data[11].get('hash')

        b12 = list(df['block_12'])
        for i in b12:
            if i == chain_data[12].get('hash'):
                ind = b12.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_12'] = filenames[ind] + "#" + "block_12"
                break
            else:
                df.loc[df['filename'] == filename, 'block_12'] = chain_data[12].get('hash')

        b13 = list(df['block_13'])
        for i in b13:
            if i == chain_data[13].get('hash'):
                ind = b13.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_13'] = filenames[ind] + "#" + "block_13"
                break
            else:
                df.loc[df['filename'] == filename, 'block_13'] = chain_data[13].get('hash')

        b14 = list(df['block_14'])
        for i in b14:
            if i == chain_data[14].get('hash'):
                ind = b14.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_14'] = filenames[ind] + "#" + "block_14"
                break
            else:
                df.loc[df['filename'] == filename, 'block_14'] = chain_data[14].get('hash')

        b15 = list(df['block_15'])
        for i in b15:
            if i == chain_data[15].get('hash'):
                ind = b15.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_15'] = filenames[ind] + "#" + "block_15"
                break
            else:
                df.loc[df['filename'] == filename, 'block_15'] = chain_data[15].get('hash')

        b16 = list(df['block_16'])
        for i in b16:
            if i == chain_data[16].get('hash'):
                ind = b16.index(i)
                # print("index of i", ind, filenames[ind])
                df.loc[df['filename'] == filename, 'block_16'] = filenames[ind] + "#" + "block_16"
                break
            else:
                df.loc[df['filename'] == filename, 'block_16'] = chain_data[16].get('hash')
        print("after loading df:", df)
        df.to_sql('img_cloud_tags', conn, if_exists='replace', index=False)

        filenames = list(df1['filename'])
        # print("filename", filenames)
        b1 = list(df1['block_1'])
        # print("block b1", b1)
        for i in b1:
            if i == tags[0]:
                ind = b1.index(i)
                df1.loc[df1['filename'] == filename, 'block_1'] = filenames[ind] + "#" + "block_1"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_1'] = tags[0]

        b2 = list(df1['block_2'])
        for i in b2:
            if i == tags[1]:
                ind = b2.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_2'] = filenames[ind] + "#" + "block_2"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_2'] = tags[1]

        b3 = list(df1['block_3'])
        for i in b3:
            if i == tags[2]:
                ind = b3.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_3'] = filenames[ind] + "#" + "block_3"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_3'] = tags[2]

        b4 = list(df1['block_4'])
        for i in b4:
            if i == tags[3]:
                ind = b4.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_4'] = filenames[ind] + "#" + "block_4"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_4'] = tags[3]

        b5 = list(df1['block_5'])
        for i in b5:
            if i == tags[4]:
                ind = b5.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_5'] = filenames[ind] + "#" + "block_5"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_5'] = tags[4]

        b6 = list(df1['block_6'])
        for i in b6:
            if i == tags[5]:
                ind = b6.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_6'] = filenames[ind] + "#" + "block_6"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_6'] = tags[5]

        b7 = list(df1['block_7'])
        for i in b7:
            if i == tags[6]:
                ind = b7.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_7'] = filenames[ind] + "#" + "block_7"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_7'] = tags[6]

        b8 = list(df1['block_8'])
        for i in b8:
            if i == tags[7]:
                ind = b8.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_8'] = filenames[ind] + "#" + "block_8"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_8'] = tags[7]

        b9 = list(df1['block_9'])
        for i in b9:
            if i == tags[8]:
                ind = b9.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_9'] = filenames[ind] + "#" + "block_9"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_9'] = tags[8]

        b10 = list(df1['block_10'])
        for i in b10:
            if i == tags[9]:
                ind = b10.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_10'] = filenames[ind] + "#" + "block_10"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_10'] = tags[9]

        b11 = list(df1['block_11'])
        for i in b11:
            if i == tags[10]:
                ind = b11.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_11'] = filenames[ind] + "#" + "block_11"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_11'] = tags[10]

        b12 = list(df1['block_12'])
        for i in b12:
            if i == tags[11]:
                ind = b12.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_12'] = filenames[ind] + "#" + "block_12"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_12'] = tags[11]

        b13 = list(df1['block_13'])
        for i in b13:
            if i == tags[12]:
                ind = b13.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_13'] = filenames[ind] + "#" + "block_13"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_13'] = tags[12]

        b14 = list(df1['block_14'])
        for i in b14:
            if i == tags[13]:
                ind = b14.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_14'] = filenames[ind] + "#" + "block_14"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_14'] = tags[13]

        b15 = list(df1['block_15'])
        for i in b15:
            if i == tags[14]:
                ind = b15.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_15'] = filenames[ind] + "#" + "block_15"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_15'] = tags[14]

        b16 = list(df1['block_16'])
        for i in b16:
            if i == tags[15]:
                ind = b16.index(i)
                # print("index of i", ind, filenames[ind])
                df1.loc[df1['filename'] == filename, 'block_16'] = filenames[ind] + "#" + "block_16"
                break
            else:
                df1.loc[df1['filename'] == filename, 'block_16'] = tags[15]
        print("after loading df1:", df1)
        df1.to_sql('img_enc_tags', conn, if_exists='replace', index=False)


    except Exception as e:
        print(e)


def split_blocks(image, filename):
    """ Image blocks creation as per client requirement like 4x4 or 8x8..."""
    imgcrop(image, 4, 4, filename)
    return "Blocks Created successfully"


def download(img_name):
    print("img_name from download:", img_name)
    query = img_images.select().where(img_images.c.imagename == img_name)
    result = conn.execute(query)
    img_d = result.fetchall()[0][2]
    store_path = "ImageDownload/"+img_name
    print("download image:", img_d)
    with open(store_path, "wb") as file:
        file.write(img_d)
        file.close()

