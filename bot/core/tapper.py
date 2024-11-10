import asyncio
import random
from urllib.parse import unquote

import aiohttp
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.functions import account, messages
from pyrogram.raw.types import InputBotAppShortName, InputNotifyPeer, InputPeerNotifySettings
from .agents import generate_random_user_agent
from bot.config import settings
from typing import Callable
import functools
from bot.utils import logger
from bot.exceptions import InvalidSession
from .headers import headers

def error_handler(func: Callable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            await asyncio.sleep(1)
    return wrapper

class Tapper:
    def __init__(self, tg_client: Client, proxy: str):
        self.tg_client = tg_client
        self.session_name = tg_client.name
        self.proxy = proxy
        self.tg_web_data = None
        self.tg_client_id = 0
        
    async def get_tg_web_data(self) -> str:
        
        if self.proxy:
            proxy = Proxy.from_str(self.proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()

                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)
            
            while True:
                try:
                    peer = await self.tg_client.resolve_peer('DuckChain_bot')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"{self.session_name} | FloodWait {fl}")
                    logger.info(f"{self.session_name} | Sleep {fls}s")
                    await asyncio.sleep(fls + 3)
            
            ref_id = random.choice([settings.REF_ID, "KvNYn05S"]) if settings.SUPPORT_AUTHOR else settings.RED_ID
            
            web_view = await self.tg_client.invoke(messages.RequestAppWebView(
                peer=peer,
                app=InputBotAppShortName(bot_id=peer, short_name="quack"),
                platform='android',
                write_allowed=True,
                start_param=ref_id
            ))

            auth_url = web_view.url
            tg_web_data = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

            me = await self.tg_client.get_me()
            self.tg_client_id = me.id
            
            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return ref_id, tg_web_data

        except InvalidSession as error:
            logger.error(f"{self.session_name} | Invalid session")
            await asyncio.sleep(delay=3)
            return None, None

        except Exception as error:
            logger.error(f"{self.session_name} | Unknown error: {error}")
            await asyncio.sleep(delay=3)
            return None, None
        
    @error_handler
    async def join_and_mute_tg_channel(self, link: str):
        await asyncio.sleep(delay=random.randint(15, 30))
        
        if not self.tg_client.is_connected:
            await self.tg_client.connect()

        try:
            parsed_link = link if 'https://t.me/+' in link else link[13:]
            
            chat = await self.tg_client.get_chat(parsed_link)
            
            if chat.username:
                chat_username = chat.username
            elif chat.id:
                chat_username = chat.id
            else:
                logger.info("Unable to get channel username or id")
                return
            
            logger.info(f"{self.session_name} | Retrieved channel: <y>{chat_username}</y>")
            try:
                await self.tg_client.get_chat_member(chat_username, "me")
            except Exception as error:
                if error.ID == 'USER_NOT_PARTICIPANT':
                    await asyncio.sleep(delay=3)
                    chat = await self.tg_client.join_chat(parsed_link)
                    chat_id = chat.id
                    logger.info(f"{self.session_name} | Successfully joined chat <y>{chat_username}</y>")
                    await asyncio.sleep(random.randint(5, 10))
                    peer = await self.tg_client.resolve_peer(chat_id)
                    await self.tg_client.invoke(account.UpdateNotifySettings(
                        peer=InputNotifyPeer(peer=peer),
                        settings=InputPeerNotifySettings(mute_until=2147483647)
                    ))
                    logger.info(f"{self.session_name} | Successfully muted chat <y>{chat_username}</y>")
                else:
                    logger.error(f"{self.session_name} | Error while checking channel: <y>{chat_username}</y>: {str(error.ID)}")
        except Exception as e:
            logger.error(f"{self.session_name} | Error joining/muting channel {link}: {str(e)}")
            await asyncio.sleep(delay=3)    
        finally:
            if self.tg_client.is_connected:
                await self.tg_client.disconnect()
            await asyncio.sleep(random.randint(10, 20))
    
    @error_handler
    async def make_request(self, http_client, method, endpoint=None, url=None, **kwargs):
        full_url = url or f"https://preapi.duckchain.io{endpoint or ''}"
        response = await http_client.request(method, full_url, **kwargs)
        # print("Request URL:", full_url)
        # print("Request Headers:", http_client.headers)
        # print("Response:", response)
        response.raise_for_status()
        return await response.json()
    
    @error_handler
    async def login(self, http_client):
        response = await self.make_request(http_client, 'GET', endpoint="/user/info")
        return response if response.get("code") == 200 else None
    
    @error_handler
    async def open_box(self, http_client, open_type=1):
        response = await self.make_request(http_client, 'POST', endpoint="/box/open", json={'openType': open_type})
        return response if response.get("code") == 200 else None
    
    @error_handler
    async def claim_daily_egg(self, http_client):
        return await self.make_request(http_client, 'GET', endpoint="/property/daily/finish?taskId=1")
    
    @error_handler
    async def task_list(self, http_client):
        return await self.make_request(http_client, 'GET', endpoint="/task/task_list")
    
    @error_handler
    async def task_info(self, http_client):
        return await self.make_request(http_client, 'GET', endpoint="/task/task_info")
    
    @error_handler
    async def sign_in(self, http_client):
        return await self.make_request(http_client, 'GET', endpoint="/task/sign_in?")
    
    @error_handler
    async def done_task(self, http_client, task_type, task_id):
        response = await self.make_request(http_client, 'GET', endpoint=f"/task/{task_type}?taskId={task_id}")
        return response if response.get("code") and response.get("message") == "SUCCESS" == 200 else None
    
    @error_handler
    async def quack_tap(self, http_client):
        response = await self.make_request(http_client, 'GET', endpoint="/quack/execute")
        return response if response.get("code") == 200 else None
    
    @error_handler
    async def get_task_type(self, category):
        """Return the task type based on the category."""
        if category == 'socialMedia':
            return 'socialMedia'
        elif category == 'daily':
            return 'daily'
        elif category == 'partner':
            return 'partner'
        elif category == 'oneTime':
            return 'oneTime'
        else:
            return None
        
    @error_handler
    async def check_proxy(self, http_client: aiohttp.ClientSession) -> None:
        response = await self.make_request(http_client, 'GET', url='https://httpbin.org/ip', timeout=aiohttp.ClientTimeout(5))
        ip = response.get('origin')
        logger.info(f"{self.session_name} | Proxy IP: {ip}")
    
    async def run(self) -> None:
        if settings.USE_RANDOM_DELAY_IN_RUN:
                random_delay = random.randint(settings.RANDOM_DELAY_IN_RUN[0], settings.RANDOM_DELAY_IN_RUN[1])
                logger.info(f"{self.session_name} | Bot will start in <y>{random_delay}s</y>")
                await asyncio.sleep(random_delay)
                
        proxy_conn = ProxyConnector().from_url(self.proxy) if self.proxy else None
        http_client = aiohttp.ClientSession(headers=headers, connector=proxy_conn)
        ref_id, init_data = await self.get_tg_web_data()
        
        if not init_data:
            if not http_client.closed:
                await http_client.close()
            if proxy_conn:
                if not proxy_conn.closed:
                    proxy_conn.close()
            return

        http_client.headers['authorization'] = "tma " + init_data
        
        if self.proxy:
            await self.check_proxy(http_client=http_client)
        
        fake_user_agent = generate_random_user_agent(device_type='android', browser_type='chrome')
        
        
        if settings.FAKE_USERAGENT:
            http_client.headers['User-Agent'] = fake_user_agent
        
        while True:
            try:
                if http_client.closed:
                    if proxy_conn:
                        if not proxy_conn.closed:
                            proxy_conn.close()

                    proxy_conn = ProxyConnector().from_url(self.proxy) if self.proxy else None
                    http_client = aiohttp.ClientSession(headers=headers, connector=proxy_conn)
                    if settings.FAKE_USERAGENT:            
                        http_client.headers['User-Agent'] = fake_user_agent
                
                user_data = await self.login(http_client=http_client)
                if not user_data:
                    logger.info(f"{self.session_name} | <r>Login Failed!</r>")
                    sleep_time = random.randint(settings.SLEEP_TIME[0], settings.SLEEP_TIME[1])
                    logger.info(f"{self.session_name} | Sleep <y>{sleep_time}s</y>")
                    await asyncio.sleep(delay=sleep_time)
                    continue
                
                full_name = user_data["data"].get("defaultName")
                quack_times = user_data["data"].get("quackTimes", 0)
                box_amount = user_data["data"].get("boxAmount", 0)
                total_points = user_data["data"].get("decibels")
                card_id = user_data["data"].get("cardId")
                wallet_address = user_data["data"].get("particleWallet")
                total_eggs = user_data["data"].get("eggs", 0)
                
                logger.info(f"{self.session_name} | <y>🦆 Login successful</y> | <g>{full_name}</g>")
                logger.info(f"{self.session_name} | Card ID : <g>{card_id}</g> | Points : <g>{total_points}</g> | Eggs : <g>{total_eggs}</g> | Quack Times : <g>{quack_times}</g> | Total Box : <g>{box_amount}</g>")
                logger.info(f"{self.session_name} | Particle Network Wallet : <g>{wallet_address}</g>")
                
                await asyncio.sleep(random.randint(1, 5))
                
                daily_eggs = await self.claim_daily_egg(http_client=http_client)
                if daily_eggs.get("code") == 500:
                    logger.info(f"{self.session_name} | <y>🥚 Eggs are already claimed.</y>")
                elif daily_eggs.get("code") == 200:
                    if daily_eggs.get("data") == 1:
                        logger.info(f"{self.session_name} | <g>🥚 Successfully claimed daily eggs.</g>")
                    else:
                        logger.info(f"{self.session_name} | <r>Failed to claim daily eggs!</r>")
                        
                await asyncio.sleep(random.randint(1, 5))
                
                if settings.OPEN_BOX and box_amount > 0:
                    logger.info(f"{self.session_name} | <y>Opening Boxes...</y>")
                    while True:
                        box_data = await self.open_box(http_client=http_client)
                        if not box_data:
                            logger.info(f"{self.session_name} | <r>Failed to open the box!</r>")
                            logger.info(f"{self.session_name} | Sleep <y>10s</y>")
                            await asyncio.sleep(delay=10)
                            continue
                        
                        quantity = box_data['data'].get('quantity', 0)
                        obtain_point = box_data['data'].get('obtain', 0)
                        boxes_left = box_data['data'].get('boxesLeft', 0)
                        logger.info(f"{self.session_name} | Quantity : <g>{quantity}</g> | Points : <g>{obtain_point}</g>")
                        
                        if boxes_left == 0:
                            logger.info(f"{self.session_name} | <y>All box opened!</y>")
                            break
                
                await asyncio.sleep(random.randint(1, 3))
                
                if settings.AUTO_TASK:
                    #Task List
                    task_list_response = await self.task_list(http_client=http_client)
                    
                    if isinstance(task_list_response, dict):
                        task_list = task_list_response.get('data')
                    else:
                        task_list = None

                    if not task_list:
                        logger.info(f"{self.session_name} | <r>Failed to process tasks!</r>")
                        logger.info(f"{self.session_name} | Sleep <y>10s</y>")
                        await asyncio.sleep(delay=10)
                        continue
                    
                    #Task Completed
                    task_info_response = await self.task_info(http_client=http_client)
                    
                    if isinstance(task_info_response, dict):
                        task_info = task_info_response.get('data', {})
                    else:
                        task_info = None

                    if not task_info:
                        logger.info(f"{self.session_name} | <r>Failed to process tasks!</r>")
                        logger.info(f"{self.session_name} | Sleep <y>10s</y>")
                        await asyncio.sleep(delay=10)
                        continue
                    
                    completed_task_ids = set(
                        task_info.get('socialMedia', []) +
                        task_info.get('daily', []) +
                        task_info.get('partner', []) +
                        task_info.get('oneTime', [])
                    )
                    
                    for category, task_list in task_list.items():
                        if isinstance(task_list, list):
                            for task in task_list:
                                task_id = task.get('taskId')
                                content = task.get('content')
                                integral = task.get('integral')
                                
                                if task_id in completed_task_ids or task_id == 137:
                                    continue
                                
                                if task_id == 8:
                                    sign_in_response = await self.sign_in(http_client=http_client)
                                    if sign_in_response and sign_in_response.get("code") == 200:
                                        logger.info(f"{self.session_name} | <y>Successfully claimed {content} :</y> <g>+{integral}</g>")
                                    elif sign_in_response.get("code") == 500:
                                        logger.info(f"{self.session_name} | <y>{content} already claimed.</y>")
                                    else:
                                        logger.info(f"{self.session_name} | <r>Error claiming {content}.</r>")
                                        
                                await asyncio.sleep(random.randint(1, 3))
                                
                                task_type = await self.get_task_type(category=category)
                                if not task_type or task_type is None:
                                    logger.info(f"{self.session_name} | <r>{category} is unknown task type, skipping!</r>")
                                    continue
                                
                                await asyncio.sleep(random.randint(1, 5))
                                
                                make_task = await self.done_task(http_client=http_client, task_type=task_type, task_id=task_id)
                                
                                if make_task is None:
                                    logger.info(f"{self.session_name} | <r>Failed to process tasks!</r>")
                                    logger.info(f"{self.session_name} | Sleep <y>10s</y>")
                                    await asyncio.sleep(delay=10)
                                    continue
                                
                                logger.info(f"{self.session_name} | <y>Task {content} Done :</y> <g>+{integral}</g>")
                        else:
                            logger.info(f"{self.session_name} | <r>Failed to process tasks!</r>")
                            logger.info(f"{self.session_name} | Sleep <y>10s</y>")
                            await asyncio.sleep(delay=10)
                            continue
                        
                await asyncio.sleep(random.randint(1, 5))
                
                if settings.AUTO_QUACK:
                    quack_time = random.randint(settings.TOTAL_QUACK[0], settings.TOTAL_QUACK[1])
                    for i in range(quack_time):
                        quack_response = await self.quack_tap(http_client=http_client)
                        if quack_response is None:
                            logger.info(f"{self.session_name} | <r>Failed to Quack!</r>")
                            logger.info(f"{self.session_name} | Sleep <y>10s</y>")
                            await asyncio.sleep(delay=10)
                            continue
                        
                        quack_records = quack_response["data"].get("quackRecords", [])
                        
                        result = int(quack_records[-1]) if quack_records else None
                        
                        logger.info(f"{self.session_name} | Quack : <g>{i + 1}</g> | Result : <g>{result}</g> | New Points : <g>{quack_response['data'].get('decibel', 0)}</g> | Total Quack : <g>{quack_response['data'].get('quackTimes', None)}</g>")

                        await asyncio.sleep(random.uniform(settings.QUACK_DELAY[0], settings.QUACK_DELAY[1]))
                

                await http_client.close()
                if proxy_conn:
                    if not proxy_conn.closed:
                        proxy_conn.close()

            except Exception as error:
                logger.error(f"{self.session_name} | Unknown error: {error}")
                await asyncio.sleep(delay=3)
                
                   
            sleep_time = random.randint(settings.SLEEP_TIME[0], settings.SLEEP_TIME[1])
            logger.info(f"{self.session_name} | Sleep <y>{sleep_time}s</y>")
            await asyncio.sleep(delay=sleep_time)    

async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        await Tapper(tg_client=tg_client, proxy=proxy).run()
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
