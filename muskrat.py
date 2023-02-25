from playwright.sync_api import Playwright, sync_playwright, expect
from playwright_stealth import stealth_sync
import time
from termcolor import cprint
import sys
import json
import getpass
from typing import Set, Tuple, List

class Config(object):
    username = ""
    password = ""

    def __init__(self, filename: str = "config.json") -> None:
        try:
            creds = json.loads(open(filename).read())["data"]
            self.username = creds["username"]
            self.password = creds["password"]
        except:
            cprint("Unable to load credentials...", "red")
            self.username = input("Twitter username: ")
            self.password = getpass.getpass("Twitter password: ")
            creds = {"data": {"username": self.username, "password": self.password}}
            with open("config.json", "w") as config_file:
                json.dump(creds, config_file)

class Titter(object):
    verbose = False
    browser = None
    _logged_in = False
    username = ""
    password = ""

    def __init__(self, config: Config, verbose=False) -> None:
        self.password = config.password
        self.username = config.username
        self.verbose = verbose
    def get_followers(
        self, account: str, headless=False, limit: str = 69420, following: bool = False
    ) -> Set[str]:
        with sync_playwright() as play:
            browser = play.chromium.launch(headless=headless)
            page = browser.net_page()
            stealth_sync(page)
            page.goto("https://twitter.com/")
            page.get_by_test_id("login").click()
            time.sleep(2)
            page.get_by_role("dialog", name="Sign in to Twitter").locator(
                "label div"
            ).nth(3).click()
            time.sleep(2)
            page.get_by_label("Phone, email, or username").fill(self.username)
            time.sleep(2)
            page.get_by_role("button", name="Next").click()
            time.sleep(2)
            page.get_by_label("Password", exact=True).fill(self.password)
            time.sleep(2)
            page.get_by_test_id("LoginForm_Login_Button").click()
            try:
                page.get_by_test_id("SideNav_AccountSwitcher_Button").click()
            except:
                if self.verbose:
                    cprint(f"Unable to login with credentials...")
                    return set()
            ats = set()
            page.goto(f"https://twitter.com/{account}")
            time.sleep(2)
            page.get_by_role(
                "link", name="Followers"
            ).click() if not following else page.get_by_role(
                "link", name="Following"
            ).click()
            y = page.get_by_test_id("primaryColumn")
            time.sleep(2)
            v = y.get_by_role("button").all()
            shitty_hack = 0
            while True:
                for x in v:
                    r = x.get_by_role("link", name="@")
                    for s in r.all_text_contents():
                        if not s.startswith("@"):
                            continue
                        page.mouse.wheel(0, 10)
                        if s in ats:
                            shitty_hack += 1
                            if shitty_hack > 1000:
                                return ats
                            else:
                                continue
                        else:
                            shitty_hack = 0
                            if self.verbose:
                                cprint(f">>>\t{s}", "green")
                            ats.add(s)
                            if len(ats) >= limit:
                                return ats

    def get_following(
        self, account: str, headless=False, limit: str = 69420
    ) -> List[Tuple[str, str, str]]:
        return self.get_followers(
            account=account, headless=headless, limit=limit, following=True
        )

    def search(self, term: str, limit=69420, headless=False) -> Set[str]:
        with sync_playwright() as play:
            browser = play.chromium.launch(headless=headless)
            page = browser.new_page()
            stealth_sync(page)
            page.goto("https://twitter.com/")
            page.get_by_test_id("login").click()
            time.sleep(2)
            page.get_by_role("dialog", name="Sign in to Twitter").locator(
                "label div"
            ).nth(3).click()
            time.sleep(2)
            page.get_by_label("Phone, email, or username").fill(self.username)
            time.sleep(2)
            page.get_by_role("button", name="Next").click()
            time.sleep(2)
            page.get_by_label("Password", exact=True).fill(self.password)
            time.sleep(2)
            page.get_by_test_id("LoginForm_Login_Button").click()
            try:
                page.get_by_test_id("SideNav_AccountSwitcher_Button").click()
            except:
                if self.verbose:
                    cprint(f"Unable to login with credentials...","red")
                    return []
            page.goto("https://twitter.com/explore")
            time.sleep(2)
            page.get_by_test_id("SearchBox_Search_Input").click()
            time.sleep(2)
            page.get_by_test_id("SearchBox_Search_Input").fill(term)
            time.sleep(2)
            page.get_by_test_id("SearchBox_Search_Input").press("Enter")
            time.sleep(5)
            tweets = set()
            shitty_hack = 0
            formatted = []
            while True:
                potential_tweets = page.get_by_role("article").all()
                shitty_hack = 0
                for tweet in potential_tweets:
                    page.mouse.wheel(0, 10)
                    content = tweet.text_content()
                    if content in tweets:
                        shitty_hack += 1
                        if shitty_hack > 1000:
                            return formatted
                        continue

                    else:
                        tweets.add(content)
                        name = content.split("@")[0]
                        at = content.split("@")[1].split("·")[0]
                        rest = content.split("·")[1]
                        if self.verbose:
                            cprint(f"{at} ({name}) -> {rest}","green")
                        formatted.append((name, at, rest))
                        if len(formatted) >= limit:
                            return formatted

    def get_tweets(self, user: str, limit=69420, headless=False) -> Set[str]:
        with sync_playwright() as play:
            browser = play.chromium.launch(headless=headless)
            page = browser.new_page()
            stealth_sync(page)
            page.goto("https://twitter.com/")
            page.get_by_test_id("login").click()
            time.sleep(2)
            page.get_by_role("dialog", name="Sign in to Twitter").locator(
                "label div"
            ).nth(3).click()
            time.sleep(2)
            page.get_by_label("Phone, email, or username").fill(self.username)
            time.sleep(2)
            page.get_by_role("button", name="Next").click()
            time.sleep(2)
            page.get_by_label("Password", exact=True).fill(self.password)
            time.sleep(2)
            page.get_by_test_id("LoginForm_Login_Button").click()
            try:
                page.get_by_test_id("SideNav_AccountSwitcher_Button").click()
            except:
                if self.verbose:
                    cprint(f"Unable to login with credentials...","red")
                    return []
            page.goto(f"https://twitter.com/{user}")
            time.sleep(5)
            tweets = set()
            shitty_hack = 0
            formatted = []
            while True:
                potential_tweets = page.get_by_role("article").all()
                shitty_hack = 0
                for tweet in potential_tweets:
                    page.mouse.wheel(0, 10)
                    content = tweet.text_content()
                    if content in tweets:
                        shitty_hack += 1
                        if shitty_hack > 1000:
                            return formatted
                        continue

                    else:
                        tweets.add(content)
                        try:
                            name = content.split("@")[0]
                            at = content.split("@")[1].split("·")[0]
                            rest = content.split("·")[1]
                        except:
                            continue  # Unable to view tweet
                        if self.verbose:
                            cprint(f"{at} ({name}) -> {rest}","green")
                        formatted.append((name, at, rest))
                        if len(formatted) >= limit:
                            return formatted
if __name__ == "__main__":
    c = Config()
    t = Titter(c, verbose=("-v" in sys.argv))
    t.search("bl4qh4t")
