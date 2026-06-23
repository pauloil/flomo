__version__ = '1.0.0-alpha'

import platform
import requests
import os
import hashlib
import requests
from typing import Any, List, Optional, Dict
from datetime import datetime
from bs4 import BeautifulSoup
from html2text import html2text


class Flomo:

    def __init__(self, authorization):
        self.token = authorization
        self.limit = 200  # memo数量上限
        self.base_url = "https://flomoapp.com/api/v1/memo"
        self.url_updated = f"{self.base_url}/updated/"
        self.salt = "dbbc3dd73364b4084c3a69346e0ce2b2"
        self.success_code = 0

    def _sign(self, params: dict) -> dict:
        """Add timestamp and MD5 signature to a params dict."""
        params.setdefault("tz", "8:0")
        params.setdefault("timestamp", str(int(datetime.now().timestamp())))
        params.setdefault("api_key", "flomo_web")
        params.setdefault("app_version", "5.25.64")
        params.setdefault("platform", "mac")
        params.setdefault("webp", "1")
        param_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        params["sign"] = hashlib.md5((param_str + self.salt).encode("utf-8")).hexdigest()
        return params

    def _get_params(self, params: dict):
        params_sorted = {
            "limit": self.limit,
            "tz": "8:0",
            "timestamp": str(int(datetime.now().timestamp())),
            "api_key": "flomo_web",
            "app_version": "5.25.64",
            "platform": "mac",
            "webp": "1"
        }
        latest_slug = params.get("latest_slug", "")
        latest_updated_at = params.get("latest_updated_at", 0)
        if latest_slug and latest_updated_at:
            params_sorted.update({
                "latest_slug": latest_slug,
                "latest_updated_at": latest_updated_at
            })

        # 排序并生成签名
        param_str = "&".join(
            [f"{k}={v}" for k, v in sorted(params_sorted.items())])
        sign = hashlib.md5((param_str + self.salt).encode("utf-8")).hexdigest()
        params_sorted["sign"] = sign

        return params_sorted

    def _headers(self) -> dict:
        return {"authorization": self.token}

    def _check(self, data: dict) -> dict:
        if data.get("code") != self.success_code:
            raise Exception(f"flomo request error: {data}")
        return data

    def request(self, params: Optional[dict] = None):
        headers = {"authorization": self.token}
        resp = requests.get(self.url_updated,
                            params=self._get_params(params or {}),
                            headers=headers)
        data = resp.json()
        if data["code"] != self.success_code:
            raise Exception(f"flomo request error: {data}")
        return data.get("data", []) or []

    def get_all_memos(self, params: Optional[dict] = None) -> List:
        """inspired by https://github.com/raoooool/flomo-reminder"""
        memos = self.request(params)
        if len(memos) >= self.limit:
            _updated_at = int(
                datetime.fromisoformat(memos[-1]["updated_at"]).timestamp())
            _params = {
                "latest_slug": memos[-1]["slug"],
                "latest_updated_at": _updated_at
            }
            return memos + self.get_all_memos(_params)
        else:
            return memos

    def create(self, content: str) -> Dict:
        """Create a new memo. Plain text is auto-wrapped in <p> tags."""
        if not content.strip().startswith("<"):
            content = f"<p>{content}</p>"
        resp = requests.put(
            f"{self.base_url}/",
            params=self._sign({"content": content}),
            headers=self._headers(),
        )
        return self._check(resp.json())["data"]

    def update(self, slug: str, content: str) -> Dict:
        """Update an existing memo by slug."""
        if not content.strip().startswith("<"):
            content = f"<p>{content}</p>"
        resp = requests.put(
            f"{self.base_url}/{slug}/",
            params=self._sign({"content": content}),
            headers=self._headers(),
        )
        return self._check(resp.json())["data"]

    def delete(self, slug: str) -> str:
        """Delete a memo by slug. Returns the API message."""
        resp = requests.delete(
            f"{self.base_url}/{slug}/",
            params=self._sign({}),
            headers=self._headers(),
        )
        return self._check(resp.json())["message"]


class Parser:

    def __init__(self, data: Dict):
        self.data = data
        for key, value in self.data.items():
            setattr(self, key, value)

    @property
    def text(self, kind='markdown'):
        if kind.lower() == 'markdown':
            return html2text(self.content)

        soup = BeautifulSoup(self.content, "lxml")
        plain_text = soup.get_text(separator='\n', strip=True)
        return plain_text

    @property
    def url(self):
        return "https://v.flomoapp.com/mine/?memo_id=" + self.slug


def notify(title,
           message,
           subtitle='',
           sound='Hero',
           open='https://flomoapp.com/',
           method='',
           activate='',
           icon='https://flomoapp.com/images/logo-192x192.png',
           terminal_notifier_path='terminal-notifier'):
    sysstr = platform.system()

    if sysstr == 'Darwin':  # macOS
        # print('macOS notification')
        if method == 'terminal-notifier':
            '''https://github.com/julienXX/terminal-notifier'''

            t = f'-title "{title}"'
            m = f'-message "{message}"'

            s = f'-subtitle "{subtitle}"'
            icon = f'-appIcon "{icon}"'
            sound = f'-sound "{sound}"'

            activate = '' if activate == '' else f'-activate "{activate}"'
            open = '' if open == '' else f'-open "{open}"'

            cmd = '{} {} '.format(
                terminal_notifier_path,
                ' '.join([m, t, s, icon, activate, open, sound]))
            os.system(cmd)
        else:
            os.system(
                f"""osascript -e 'display notification "{message}" with title "{title}"'"""
            )
    elif sysstr == "Windows":
        print('TODO: windows notification')
    elif sysstr == "Linux":
        print('TODO: Linux notification')
