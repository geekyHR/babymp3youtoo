import browser_cookie3
import http.cookiejar

def export_cookies():
    cookies = browser_cookie3.chrome(domain_name="youtube.com")
    cookiejar = http.cookiejar.MozillaCookieJar("youtube_cookies.txt")
    for cookie in cookies:
        if cookie.expires is not None:  # Skip cookies without expiry date
            cj_cookie = http.cookiejar.Cookie(
                version=0,
                name=cookie.name,
                value=cookie.value,
                port=None,
                port_specified=False,
                domain=cookie.domain,
                domain_specified=True,
                domain_initial_dot=cookie.domain.startswith('.'),
                path=cookie.path,
                path_specified=True,
                secure=cookie.secure,
                expires=int(cookie.expires),
                discard=False,
                comment=None,
                comment_url=None,
                rest={'HttpOnly': cookie._rest.get('HttpOnly')},
                rfc2109=False
            )
            cookiejar.set_cookie(cj_cookie)
    cookiejar.save(ignore_discard=True, ignore_expires=True)
    print("✅ youtube_cookies.txt updated!")

if __name__ == "__main__":
    export_cookies()
