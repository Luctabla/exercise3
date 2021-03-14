import time

import aiohttp
import asyncio

username = 'Admin'
password = 'nullable=False'

class Client(object):

    async def fetch(self, url):
        async with self.session.get(url) as response:
            return await response.read()

    async def run(self, r, sync_or_async):
        url = "http://localhost:5000/{}?id_post={}"
        tasks = []

        for i in range(r):
            task = asyncio.create_task(self.fetch(url.format(sync_or_async, 1)))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses[:15])
        await self.session.close()

    async def login(self):
        self.session = aiohttp.ClientSession()
        payload = {'username': 'Admin', 'password': 'nullable=False'}
        response = await self.session.post('http://localhost:5000/login', data=payload)
        print("Status:", response.status)
        print("Content-type:", response.headers['content-type'])

        html = await response.text()
        print("Body:", html[:15], "...")

def start_client(route, count_requests):
    start = time.time()
    client = Client()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.login())

    loop.run_until_complete(client.run(count_requests, route))
    end = time.time()
    print('Running in {} mode has taken: {} seconds.'.format(route, end - start))


if __name__ == '__main__':
    SERVER_TYPE = {1: 'sync', 2: 'async', 3: 'asgi_server'}
    correct_input = False
    while not correct_input:
        try:
            server_type = int(input('Choose which type server would you do the requests:\n'
                                    '1 - sync\n'
                                    '2 - async with an wsgi server\n'
                                    '3 - async with an asgi server\n'))
            if server_type > 0 & server_type <= 3:
                count_requests = int(input('Input how many request want to do'))
                if count_requests > 0 and count_requests < 1000:
                    route = SERVER_TYPE[server_type]
                    correct_input = True
                    start_client(route, count_requests)
                    break

        except KeyboardInterrupt:
            break
        except:
            print("Input a correct input.\n")




