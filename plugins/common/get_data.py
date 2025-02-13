import requests,json

def api_check(station_id):
    url = f"http://openapi.seoul.go.kr:8088/584a6e6b54706f703730746f44786b/json/bikeList/1/5/{station_id}" 
    response = requests.get(url)

    if response.status_code == 200:
        print("Connect Success")
        print(f"Status Code : {response.status_code}")
        return True
    print("Connect Fail")
    print(f"Status Code : {response.status_code}")
    return False

def get_data(station_id):
    url = f"http://openapi.seoul.go.kr:8088/584a6e6b54706f703730746f44786b/json/bikeList/1/5/{station_id}" 
    response = requests.get(url)
    data = response.json()
    print(data["rentBikeStatus"]["list_total_count"])