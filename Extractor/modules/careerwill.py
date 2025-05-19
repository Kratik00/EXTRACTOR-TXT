import os, requests, asyncio, cloudscraper
from pyrogram import filters
from Extractor import app
from config import SUDO_USERS

requests = cloudscraper.create_scraper()

@app.on_message(filters.command(["cw"]) & filters.user(SUDO_USERS))
async def career_willl(app, message):
    try:
        input1 = await app.ask(message.chat.id, "Send ID*Password or Token")
        login_url = "https://elearn.crwilladmin.com/api/v5/login-other"
        raw_text = input1.text

        headers = {
            'authority': 'elearn.crwilladmin.com', 'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded', 'origin': 'https://web.careerwill.com',
            'user-agent': 'okhttp/5.2', 'referer': 'https://web.careerwill.com/'
        }

        if "*" in raw_text:
            e, p = raw_text.split("*", 1)
            payload = {"email": e, "password": p}
            response = requests.post(login_url, headers=headers, data=payload)
            token = response.json()["data"].get("token")
        else: token = raw_text

        headers["token"] = f"{token}"
        batch_url = "https://elearn.crwilladmin.com/api/v5/my-batch"
        batch_data = requests.get(batch_url, headers=headers).json()["data"]["batchData"]

        batch_details = [f"{item.get('id')} ☆ {item.get('batchName')} by {item.get('instructorName')}" for item in batch_data]
        await app.send_message(message.chat.id, "\n".join(batch_details))

        ci = (await app.ask(message.chat.id, "Please input your Course ID")).text
        batch_detail_url = f"https://elearn.crwilladmin.com/api/v5/batch-detail/{ci}"
        b_dta = requests.get(batch_detail_url, headers=headers).json()

        file_path = f"{b_dta['data']['class_list']['id']}_{b_dta['data']['class_list']['batchName']}.txt"
        with open(file_path, "w") as f:
            topic_url = f"https://elearn.crwilladmin.com/api/v5/batch-topic/{ci}?type=class"
            topics = requests.get(topic_url, headers=headers).json()["data"]["batch_topic"]
            for item in topics:
                ti = item.get("id")
                u4 = requests.get(f"https://elearn.crwilladmin.com/api/v5/batch-detail/{ci}?topicId={ti}", headers=headers).json()
                for lesson in reversed(u4["data"]["class_list"]["classes"]):
                    lu = requests.get(f"https://elearn.crwilladmin.com/api/v5/class-detail/{lesson.get('id')}", headers=headers).json()["data"]["class_detail"]["lessonUrl"]
                    if lu.startswith(("62", "63")):
                        vt = requests.get(f"https://elearn.crwilladmin.com/api/v5/livestreamToken?base=web&module=batch&type=brightcove&vid={lesson.get('id')}", headers=headers).json()["data"]["token"]
                        u7 = requests.get(f"https://edge.api.brightcove.com/playback/v1/accounts/6206459123001/videos/{lu}", headers={"BCOV-POLICY": "BCpkADawqM1474MvKwYlMRZNBPoqkJY-UWm7zE1U769d5r5kqTjG0v8L-THXuVZtdIQJpfMPB37L_VJQxTKeNeLO2Eac_yMywEgyV9GjFDQ2LTiT4FEiHhKAUvdbx9ku6fGnQKSMB8J5uIDd"}).json()
                        vu = next((src.get("src") for src in u7.get("sources", []) if src.get("ext_x_version") == "4"), "")
                        f.write(f"{lesson.get('lessonName')}: {vu}&bcov_auth={vt}\n")
                    else: f.write(f"{lesson.get('lessonName')}: https://www.youtube.com/embed/{lu}\n")
        
        await app.send_document(message.chat.id, file_path)
        os.remove(file_path)

    except Exception as e:
        await app.send_message(message.chat.id, f"An error occurred: {str(e)}")
