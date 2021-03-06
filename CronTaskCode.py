# 用于Cron任务调用的Action触发
import requests
import json

def run():
        payload = json.dumps({"ref": "main"})
        header = {'Authorization': 'token **********',
                  "Accept": "application/vnd.github.v3+json"}
        response_decoded_json = requests.post(
            f'https://api.github.com/repos/l549349545/crdsrw/actions/workflows/9310500/dispatches',
            data=payload, headers=header)

# 云函数入口
def main_handler(event, context):
    return run()
