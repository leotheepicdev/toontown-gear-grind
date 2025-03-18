import requests, json

def main():
    url = 'http://127.0.0.1:8080/jsonrpc'
    secretKey = 'F2528A79A2431CA29BF112DBBA456'

    params = {}
    params['secretKey'] = secretKey
    params['action'] = 'systemMessage'
    params['arguments'] = ['Hello, world!']
    print(params)

    # System message payload.
    payload = {
        'method': 'action',
        'params': params,
        'jsonrpc': '2.0',
        'id': 0
    }

    response = requests.post(url, json = payload).json()
    print(response)

    assert response['result'] == 'Broadcasted system message to shard.'
    assert response['jsonrpc']
    assert response['id'] == 0

if __name__ == '__main__':
    main()