import facebook

token = 'токен'

# page_id = '135248329880846'
# api = Api(app_id="325186945248963", app_secret="a1cb3a9fb1a8f8e5889fa451fee0fce3")
# b = api.get_token_info()
# a = api.get_video_info("632268054147035")
# print(b)
graph = facebook.GraphAPI(access_token=token)
post = graph.get_object(id='1232132131231')
print(post)
