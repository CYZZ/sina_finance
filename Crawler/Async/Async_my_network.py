
from types import ClassMethodDescriptorType
import requests
import asyncio
from requests import Response
import time

import aiohttp


class MyNetwork():
    '''
    aiohttp实现网络的异步请求
    '''
    tasks = []
    @classmethod
    def asyncRequest(self, url: str, callBack, headers=None,
                     method: str = 'get',
                     params=None,
                     type: str = 'text',
                     other=None):
        '''
        发起异步的网络请求，
        method:支持两种类型get,post
        type:支持text/json/data
        '''
        c = self.mystartRequest(url=url,callBack=callBack, method=method,
                                headers=headers, params=params,type=type,other=other)
        loop = asyncio.get_event_loop()
        task = asyncio.ensure_future(c)
        loop.run_until_complete(task)
        # task = asyncio.ensure_future(c)
        # self.tasks.append(task)

    # @classmethod
    # def startDownload(self):
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(asyncio.wait(self.tasks))

    @classmethod
    async def mystartRequest(self, url: str,callBack, headers=None,
                             method: str = 'get',
                             params=None,
                             type='text',
                             other=None,
                             getEncoing=False):
        if method == 'get':
            # requests发起的请求是基于同步的，必须使用基于异步的网络请求进行指定url
            # aiohttp： 基于异步的网络请求

            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, params=params) as response:
                    if type == 'text':
                        text = await response.text()
                        callBack(text,other)
                    elif type == 'json':
                        obj = await response.json()
                        callBack(obj,other)
                    elif type == 'data':
                        obj = await response.read()
                        callBack(obj,other)
                    # await callBack(response)
                    
                    # 注意：获取响应数据的时候一定要使用await进行数据的的解析
                    # pagetext = await response.text()
                    # response.text()
                    # response.json()
                    # response.read()
                    # return response
        elif method == 'post':
            async with aiohttp.ClientSession() as session:
                async with await session.post(url, headers=headers, data=params) as response:
                    if type == 'text':
                        text = await response.text()
                        callBack(text,other)
                    elif type == 'json':
                        obj = await response.json()
                        callBack(obj,other)
                    elif type == 'data':
                        obj = await response.read()
                        callBack(obj,other)


# def mycallback(obj):
#     print(obj)
#     # async with obj.text() as text:
#     #     print(text)
#     # print(obj.text())
#     print(obj)
#     print("终于收到了数据")
# # 示例
# MyNetwork.asyncRequest(url='https://www.baidu.com/s?wd=%E5%90%8D%E7%89%87%E5%9C%A8%E7%BA%BF%E8%AE%BE%E8%AE%A1&rsv_spt=1&rsv_iqid=0xc679e9b8000769e2&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&oq=%25E5%2590%258D%25E7%2589%2587&rsv_btype=t&inputT=2250&rsv_t=2f21ZDxcpb0KvxSz8LZ74OS%2ByS2oEvZIVyzD000srsZzCXh4Ny%2BUkBFVjrqzEXYLe43w&rsv_sug3=28&rsv_sug1=18&rsv_sug7=100&rsv_pq=8c89d5180001d581&rsv_sug2=0&rsv_sug4=3161',callBack=mycallback,getEncoing=True)
# MyNetwork.asyncRequest(url='https://www.pearvideo.com/videoStatus.jsp?contId=1752818&mrd=0.4265700312843941', callBack=mycallback,type='text',getEncoing=True)




# 多个任务异步执行
# tasks = []
# for url in urls:
#     c = getpage(url)
#     task = asyncio.ensure_future(c)
#     tasks.append(task)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(asyncio.wait(tasks))