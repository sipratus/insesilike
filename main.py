import requests
import time
import hashlib
import base64
import urllib.parse
import threading
import streamlit as st


def load_cookies_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        cookies_list = response.text.splitlines()
        return [cookie.strip() for cookie in cookies_list]
    else:
        raise Exception(f"Gagal mengunduh file cookies. Kode status: {response.status_code}")


def generate_device_id(seed="random_seed"):
    """
    Menghasilkan device_id yang mirip dengan format yang diberikan.
    """
    hash_object = hashlib.sha256(seed.encode('utf-8'))
    hash_digest = hash_object.digest()
    base64_encoded = base64.b64encode(hash_digest).decode('utf-8')
    device_id = urllib.parse.quote(base64_encoded)
    return f"device_id={device_id}"


def send_like(sessi, cookie, delaytime, like_cnt):
    url = f"https://live.shopee.co.id/api/v1/session/{sessi}/like"
    device_id = generate_device_id("unique_seed_value")

    headers = {
        "shopee_http_dns_mode": "1",
        "x-shopee-client-timezone": "Asia/Jakarta",
        "client-info": f"{device_id};device_model=I0vyOal;os=0;os_version=30;client_version=30009;network=1;platform=1;language=id",
        "x-livestreaming-source": "",
        "x-ls-sz-token": "sUBkHHFf+iqPeSH4PwKYbg==|x8sXdLoys1Y0GxSqQOnjf4Xf6bMTouLyxeDHLFvDXg/xfKcxh02OCXJeKCAiQGy9feopy4eySnvvmHJIwVlsxl2TleaIWCzSXA==|X3e/kV9eBXuxLNvf|08|1",
        "x-livestreaming-auth": "ls_android_v1_10001_1724238699_c5c51807-1426-44f8-b238-a9d2eb564051|NjgqZnHQnv4Zrdt28uAk044VgZTndB1RsMPASyse5VA=",
        "time-type": "1724238699_2",
        "content-type": "application/json;charset=UTF-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.12.4 app_type=1",
        "af-ac-enc-dat": (
            "YWNzCjAwNACpfL6Zla8tc5EBAAABAQEA8AAAAHAQUpJXn15mOnm1ZdE6fIUiMJ9dRw3adWJSfxmsYH3fy6g/WDPTRmSIVIdTb"
            "+fTzG83wL7xYY3O7uyLHVGOooL4uZz8Z0+Icn9+m4N/WAUe6wyzI/0NCAaT4jDXzep6u0e69RCyVtuy9C"
            "+kc7DRcQDtaEvJoP2wZeme2C8snECuayyteg/tHLI+P+5dRNPxxF9UokdclP/y"
            "/Ki2XNPTUCvJHyWig8066zW1RtPMko82vF1v8KlpvsbsQmkaQzw4zEUpnqgXzFXo60tX2ac5IIWeFht+l4XNDKbwkLRbCvigk6fN647t"
            "/oOHOgkn9xn9EA=="
        ),
        "af-ac-enc-id": "UIp+1d0QH2Hxhx2LO5In0RJ++LGPUcR51YrsiZvVo8jMD1qUzg9YcnK+huW6InuAfz9S9w==",
        "af-ac-enc-sz-token": "sUBkHHFf+iqPeSH4PwKYbg==|x8sXdLoys1Y0GxSqQOnjf4Xf6bMTouLyxeDHLFvDXg/xfKcxh02OCXJeKCAiQGy9feopy4eySnvvmHJIwVlsxl2TleaIWCzSXA==|X3e/kV9eBXuxLNvf|08|1",
        "x-sap-access-t": "1724238699",
        "x-sap-access-s": "BkqImkJWB27EF220MM8VXTLk4O65d84DiSqxptQLjeQ=",
        "x-sap-access-f": "1.30|13|2.6.1_14|0b2ffa5775d840cbb872f4fe5bca01a388c19dbf246440|900|100",
        "authority": "live.shopee.co.id",
        "method": "POST",
        "path": f"/api/v1/session/{sessi}/like",
        "scheme": "https"
    }

    data = {
        "like_cnt": like_cnt
    }

    while True:
        headers["cookie"] = cookie
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            st.write(f"Sukses mengirim like ke sesi {sessi} dengan cookie: {cookie[:50]}...")
        else:
            st.write(f"Gagal mengirim like ke sesi {sessi}, kode error: {response.status_code}")
        st.write(response.json())
        time.sleep(delaytime)


def start_multithreaded_love(sessi_list, cookies_list, delaytime, like_cnt):
    threads = []
    for sessi in sessi_list:
        for cookie in cookies_list:
            t = threading.Thread(target=send_like, args=(sessi, cookie, delaytime, like_cnt))
            t.start()
            threads.append(t)

    for t in threads:
        t.join()


# Streamlit interface
st.title("Shopee Like Automation")

github_url = st.text_input("Masukkan URL file cookies dari GitHub:", "https://raw.githubusercontent.com/ImanaTahira/my-cookies/main/cookies.txt")
sessi_input = st.text_input("Masukkan session IDs (pisahkan dengan koma jika lebih dari satu):")
delaytime = st.number_input("Masukan delay dalam detik:", min_value=0.0, value=1.0)
like_cnt = st.number_input("Masukan jumlah like yang akan dikirimkan:", min_value=1, value=1)

if st.button("Mulai"):
    sessi_list = sessi_input.split(',')
    try:
        cookies_list = load_cookies_from_github(github_url)
        st.write(f"Total cookies yang dimuat: {len(cookies_list)}")
        start_multithreaded_love(sessi_list, cookies_list, delaytime, like_cnt)
    except Exception as e:
        st.error(f"Error: {str(e)}")
