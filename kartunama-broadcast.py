import os
import requests
import boto3
import json
import time
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
def post_json(url, data):
    payload = data
    headers = {
        'Content-Type': 'application/json',
        'token': '3cf910c2cb021f11871705689f7457ff2da2004c5d9c3d6d3a175fa24f325557fa540f44a605769f'
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)

    return response.json()
    # if response.status_code == 201:
    #     return response.json()
    #     pass
    # else:
    #     print(f'REPONSE ERROR: {response.status_code}')
    #     print('==================')
    #     print(data)
    #     print('------------------')
    #     print(response.text)
    #     print('==================')
def send_image_wassenger(destination, image_id, image_caption):
    phone = destination
    json_data = {
        "phone": destination,
        "message": image_caption,
        "media": {
            "file": image_id
        }
    }
    url = "https://api.wassenger.com/v1/messages"
    resp = post_json(url, json_data)
    print(resp)
def send_text_wassenger(destination, message):
    phone = destination
    json_data = {
        "phone": destination,
        "message": message,
    }
    url = "https://api.wassenger.com/v1/messages"
    resp = post_json(url, json_data)
    print(resp)
def upload_to_s3(filename, s3_parameter):
    neo_bucket = s3_parameter['s3_bucket']
    head, base_filename = os.path.split(filename)

    # neo_session = boto3.Session(aws_access_key_id='0097e53172ab6efac13c', aws_secret_access_key='/TBmQkkIx6dMYNvkbx9Z44Wrth26/+t0FdKcf+pN')
    # neo_s3 = neo_session.client('s3', endpoint_url='https://nos.jkt-1.neo.id')

    session = boto3.Session(aws_access_key_id=s3_parameter['access_key_id'],
                                aws_secret_access_key=s3_parameter['secret_access_key'])
    s3 = session.client('s3', endpoint_url=s3_parameter['endpoint_url'])

    # s3 = boto3.client('s3')
    # s3r = boto3.resource('s3')
    s3_fullname = '%s/%s' % (s3_parameter['s3_path'], base_filename)
    # s3_base64_fullname = '%s/%s' % (s3_path, output_base64)

    # send image S3
    # print('Copying file %s to S3:%s/%s' % (image_output, s3_bucket, s3_fullname))
    # s3.upload_file(image_output, s3_bucket, s3_fullname, ExtraArgs={'ACL': 'public-read', 'ContentType':'image/png'})
    # url = '{}/{}/{}'.format(s3.meta.endpoint_url, s3_bucket, s3_fullname)

    # send image
    # print('Copying file %s to neo_s3:%s/%s' % (filename, neo_bucket, s3_fullname))
    s3.upload_file(filename, neo_bucket, s3_fullname,
                       ExtraArgs={'ACL': 'public-read', 'ContentType': 'image/png'})
    url = '{}/{}/{}'.format(s3.meta.endpoint_url, neo_bucket, s3_fullname)

    return url
def current_dir_to_list():
    path = './wa_blast'
    files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(path) for f in filenames if
                 os.path.splitext(f)[1] == '.jpg']
    return files
# def upload_to_wa(url):
def send_mesage(msisdn, image_id):
    msg = "Halo kak,aku Lisa dari Kartunama.net dan ini adalah Kartu Nama Digital kakak yang aku ambil dari data kita.\n\n"
    send_image_wassenger(msisdn, image_id, msg)
    time.sleep(5)
    msg = "Untuk mendukung aktifitas bisnis kakak di era New Normal, kakak bisa forward Kartu Nama Digital ini saat meeting online. Tukar kartu nama itu kesannya lebih professional dan lebih melekat.\n\n"
    send_text_wassenger(msisdn, msg)
    time.sleep(2)
    msg = "Btw mohon maaf kalau kartu namanya nggak update dengan pekerjaan kakak sekarang. Tapi Lisa bisa buatin yang baru koq, cukup balas pesan ini dengan foto dari kartu nama terbaru kakak. Nanti yang versi digital terbaru akan Lisa kirim lagi.\n\n"
    send_text_wassenger(msisdn, msg)
    time.sleep(5)
    msg = "Terima kasih ya sudah jadi pelanggan di kartunama.net, sehat dan sukses selalu :)\n\n"
    msg = msg + "Salam, \nLisa 🙍‍♀️"
    send_text_wassenger(msisdn, msg)
    time.sleep(25)
    msg = "O iya, kalau kakak mau cetak kasih tahu Lisa aja kak. Nanti di bantu juga kirim pakai Gojek atau Grab. Makasi yah kak.\n\n"
    send_text_wassenger(msisdn, msg)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.

    files = current_dir_to_list()
    path = './files'
    s3 = {
        "access_key_id": '18P61SPZYGA3H71VE5LY',
        'secret_access_key': '6pajOovWQOBhOSF1Wd50XPdEGP519zlObFLB93qT',
        'endpoint_url': 'https://ewr1.vultrobjects.com',
        's3_path': 'images',
        's3_bucket': 'wabroadcast'
    }
    start = 0
    counter = 0
    total = 10
    for file in files:
        print(f" [{counter}] Processing file {file} ...")
        if start <= counter:
            head, base_filename = os.path.split(file)
            # eend file to s3
            print("   send to S3 ...")
            url = upload_to_s3(filename=file, s3_parameter=s3)
            print(f"   url: {url}")

            # now send it to whatsapp and get the id
            print("   send to wassenger ...")
            upload_url = f'https://api.wassenger.com/v1/files?reference={file}'
            json_data = {
                'url': url
            }
            resp = post_json(upload_url,json_data)
            id = ""
            if type(resp) is list:
                id = resp[0]["id"]
            else:
                if resp['status'] == 409:
                    id = resp["meta"]["file"]
            print(f"   id: {id}")
            token = base_filename.split(".")
            destination = f"+{token[0]}"
            print(f"   send to {destination}")
            msisdn = "+628119502673"
            # send_mesage(msisdn,id)
            # msisdn = "+62811811889"
            # send_mesage(msisdn,id)
            # msisdn = "+628118074696"
            # send_mesage(msisdn,id)
            # msisdn = "+62818809609"
            # send_mesage(msisdn,id)
        else:
            print("skipped.")
        counter+=1
        print(counter-start)
        print(total)
        if counter - start > total:
            break

    # print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
