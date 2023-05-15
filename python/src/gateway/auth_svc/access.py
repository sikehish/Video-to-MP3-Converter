import os, requests

# REFERENCE:  https://www.w3schools.com/python/module_requests.asp


def login(request):
    auth = request.authroization
    if not auth:
        # this is our return format as "token, err = access.login(request)"
        return None, ("missing credentials", 401)  # returning a tuple(token,err)

    res = requests.post(
        f"http://{os.environ.get('AUTHSVC_ADDRESS')}/login",
        auth=(auth.username, auth.password),
    )

    print(res)

    if res.status_code == 201:
        return res.txt, None
    else:
        return None, (res.txt, res.status_code)
