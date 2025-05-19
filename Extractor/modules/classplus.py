import requests
import os
import json
import asyncio
from pyrogram import Client, filters, idle
from Extractor import app
from config import SUDO_USERS

api = 'https://api.classplusapp.com/v2'

# ------------------------------------------------------------------------------------------------------------------------------- #

def create_html_file(file_name, batch_name, contents):
    tbody = ''
    parts = contents.split('\n')
    for part in parts:
        split_part = [item.strip() for item in part.split(':', 1)]
    
        text = split_part[0] if split_part[0] else 'Untitled'
        url = split_part[1].strip() if len(split_part) > 1 and split_part[1].strip() else 'No URL'

        tbody += f'<tr><td>{text}</td><td><a href="{url}" target="_blank">{url}</a></td></tr>'

    with open('Extractor/core/template.html', 'r') as fp:
        file_content = fp.read()
    title = batch_name.strip()
    with open(file_name, 'w') as fp:
        fp.write(file_content.replace('{{tbody_content}}', tbody).replace('{{batch_name}}', title))

# ------------------------------------------------------------------------------------------------------------------------------- #

async def get_course_content(session, course_id, folder_id=0):

    fetched_contents = []

    params = {
        'courseId': course_id,
        'folderId': folder_id,
    }

    res = session.get(f'{api}/course/content/get', params=params)

    if res.status_code == 200:
        res = res.json()

        contents = res['data']['courseContent']

        for content in contents:

            if content['contentType'] == 1:
                resources = content['resources']

                if resources['videos'] or resources['files']:
                    sub_contents = await get_course_content(session, course_id, content['id'])
                    fetched_contents += sub_contents

            else:
                name = content['name']
                url = content['url']
                fetched_contents.append(f'{name}: {url}')

    return fetched_contents

async def classplus_txt(message, session, user_id):
    headers = {
        'accept-encoding': 'gzip',
        'accept-language': 'EN',
        'api-version': '35',
        'app-version': '1.4.73.2',
        'build-number': '35',
        'connection': 'Keep-Alive',
        'content-type': 'application/json',
        'device-details': 'Xiaomi_Redmi 7_SDK-32',
        'device-id': 'c28d3cb16bbdac01',
        'host': 'api.classplusapp.com',
        'region': 'IN',
        'user-agent': 'Mobile-Android',
        'webengage-luid': '00000187-6fe4-5d41-a530-26186858be4c'
    }

    try:
        reply = await message.chat.ask(
            (
                '**'
                'Send your credentials as shown below.\n\n'
                'Organisation Code\n'
                'Phone Number\n\n'
                'OR\n\n'
                'Access Token'
                '**'
            ),
            reply_to_message_id=message.message_id
        )
        creds = reply.text

        session.headers.update(headers)

        logged_in = False

        if '\n' in creds:
            org_code, phone_no = [cred.strip() for cred in creds.split('\n')]

            if org_code.isalpha() and phone_no.isdigit() and len(phone_no) == 10:
                res = session.get(f'{api}/orgs/{org_code}')

                if res.status_code == 200:
                    res = res.json()

                    org_id = int(res['data']['orgId'])

                    data = {
                        'countryExt': '91',
                        'mobile': phone_no,
                        'viaSms': 1,
                        'orgId': org_id,
                        'eventType': 'login',
                        'otpHash': 'j7ej6eW5VO'
                    }
        
                    res = session.post(f'{api}/otp/generate', data=json.dumps(data))

                    if res.status_code == 200:
                        res = res.json()

                        session_id = res['data']['sessionId']

                        reply = await message.chat.ask(
                            (
                                '**'
                                'Send OTP ?'
                                '**'
                            ),
                            reply_to_message_id=reply.message_id
                        )

                        if reply.text.isdigit():
                            otp = reply.text.strip()

                            data = {
                                'otp': otp,
                                'sessionId': session_id,
                                'orgId': org_id,
                                'fingerprintId': 'a3ee05fbde3958184f682839be4fd0f7',
                                'countryExt': '91',
                                'mobile': phone_no,
                            }

                            res = session.post(f'{api}/users/verify', data=json.dumps(data))

                            if res.status_code == 200:
                                res = res.json()

                                user_id = res['data']['user']['id']
                                token = res['data']['token']

                                session.headers['x-access-token'] = token

                                await reply.reply(
                                    (
                                        '**'
                                        'Your Access Token for future uses - \n\n'
                                        '**'
                                        '<pre>'
                                        f'{token}'
                                        '</pre>'
                                    ),
                                    quote=True
                                )

                                logged_in = True

                            else:
                                raise Exception('Failed to verify OTP.')
                            
                        else:
                            raise Exception('Failed to validate OTP.')
                        
                    else:
                        raise Exception('Failed to generate OTP.')
                    
                else:
                    raise Exception('Failed to get organization Id.')
                
            else:
                raise Exception('Failed to validate credentials.')

        else:

            token = creds.strip()
            session.headers['x-access-token'] = token


            res = session.get(f'{api}/users/details')

            if res.status_code == 200:
                res = res.json()

                user_id = res['data']['responseData']['user']['id']
                logged_in = True
            
            else:
                raise Exception('Failed to get user details.')


        if logged_in:

            params = {
                'userId': user_id,
                'tabCategoryId': 3
            }

            res = session.get(f'{api}/profiles/users/data', params=params)

            if res.status_code == 200:
                res = res.json()

                courses = res['data']['responseData']['coursesData']

                if courses:
                    text = ''

                    for cnt, course in enumerate(courses):
                        name = course['name']
                        text += f'{cnt + 1}. {name}\n'

                    reply = await message.chat.ask(
                        (
                            '**'
                            'Send index number of the course to download.\n\n'
                            f'{text}'
                            '**'
                        ),
                        reply_to_message_id=reply.message_id
                    )

                    if reply.text.isdigit() and int(reply.text) <= len(courses):

                        selected_course_index = int(reply.text.strip())

                        course = courses[selected_course_index - 1]

                        selected_course_id = course['id']
                        selected_course_name = course['name']

                        loader = await reply.reply(
                            (
                                '**'
                                'Extracting course...'
                                '**'
                            ),
                            quote=True
                        )

                        course_content = await get_course_content(session, selected_course_id)

                        await loader.delete()

                        if course_content:

                            caption = (f"App Name : Classplus\nBatch Name : {selected_course_name}")

                            text_file = "Classplus"
                            with open(f'{text_file}.txt', 'w') as f:
                                f.write('\n'.join(course_content))

                            await app.send_document(message.chat.id, document=f"{text_file}.txt", caption=caption)

                            html_file = f'{text_file}.html'
                            create_html_file(html_file, selected_course_name, '\n'.join(course_content))

                            await app.send_document(message.chat.id, html_file, caption=caption)
                            os.remove(f'{text_file}.txt')
                            os.remove(html_file)
                            

                        else:
                            raise Exception('Did not found any content in course.')
                    else:
                        raise Exception('Failed to validate course selection.')
                else:
                    raise Exception('Did not found any course.')
            else:
                raise Exception('Failed to get courses.')
            

   
    except Exception as e:
        print(f"Error: {e}")
        await message.reply(
            (
                '**'
                f'Error : {e}'
                '**'
            ),
            quote=True
        )

@app.on_message(filters.command("extract") & filters.user(SUDO_USERS))
async def extract_handler(client, message):
    session = requests.Session()
    await classplus_txt(message, session, user_id=None)

app.start()
idle()
