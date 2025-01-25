import flet as ft
import random
import datetime
import calendar
from flet import Container, ElevatedButton, Page
from flet.auth.providers.google_oauth_provider import GoogleOAuthProvider
import os
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
import webbrowser
import requests

load_dotenv()

ClientID = os.getenv('ClientID')
ClientSecret = os.getenv('ClientSecret')
RedirectUrl = os.getenv('RedirectUrl')

# Wasequeクラスの定義
class Waseque:
    def __init__(self, number, title, description="", date=None):
        self.number = number
        self.title = title
        self.description = description
        self.date = date  # 日程を追加

# サンプルWasequeデータの作成（サンプル数を増やす）
sample_waseques = [
    Waseque("WQ039", "Waseque Project 39: Game Development", "ゲーム開発プロジェクト", datetime.date(2024, 12, 1)),
    Waseque("WQ050", "Waseque Project 50: Mobile App", "モバイルアプリ開発", datetime.date(2024, 4, 15)),
    Waseque("WQ035", "Waseque Project 35: Web Development", "Webアプリケーション開発", datetime.date(2024, 5, 1)),
    Waseque("WQ042", "Waseque Project 42: AI Development", "AI開発プロジェクト", datetime.date(2024, 5, 15)),
    Waseque("WQ048", "Waseque Project 48: IoT Project", "IoTプロジェクト", datetime.date(2024, 6, 1)),
    Waseque("WQ037", "Waseque Project 37: Data Science", "データサイエンス", datetime.date(2024, 6, 15)),
    Waseque("WQ045", "Waseque Project 45: Blockchain", "ブロックチェーン開発", datetime.date(2024, 7, 1))
]

def view_waseque_details(page: ft.Page, waseque):
    # AppBarをページのプロパティとして設定
    page.appbar = ft.AppBar(
        title=ft.Text(waseque.title),
        bgcolor=ft.Colors.BLACK54,
        leading=ft.IconButton(
            icon=ft.Icons.ARROW_BACK,
            icon_color=ft.Colors.WHITE,
            on_click=lambda _: page.go("/home")
        ),
    )
    page.update()

    return ft.View(
        f"/waseque/{waseque.number}",
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.Card(
                            content=ft.Container(
                                content=ft.Column([
                                    ft.ListTile(
                                        title=ft.Text(waseque.title, size=20, weight=ft.FontWeight.BOLD),
                                        subtitle=ft.Text(f"Waseque Number: {waseque.number}"),
                                    ),
                                    ft.Container(
                                        content=ft.Text(waseque.description),
                                        padding=ft.padding.all(16),
                                    ),
                                    ft.Container(
                                        content=ft.Row(
                                            [
                                                ft.ElevatedButton(
                                                    "Back",
                                                    icon=ft.icons.ARROW_BACK,
                                                    on_click=lambda _: page.go("/home"),
                                                    style=ft.ButtonStyle(
                                                        color=ft.colors.WHITE,
                                                        bgcolor=ft.colors.GREY_700,
                                                    ),
                                                ),
                                                ft.ElevatedButton(
                                                    "Join Project",
                                                    icon=ft.icons.PERSON_ADD,
                                                    style=ft.ButtonStyle(
                                                        color=ft.colors.WHITE,
                                                        bgcolor=ft.colors.BLUE_400,
                                                    ),
                                                    on_click=lambda _: (
                                                        page.show_snack_bar(ft.SnackBar(content=ft.Text(f"エントリー完了:ワセクエ:{waseque.number}"))),
                                                        page.go("/home")
                                                    )
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        ),
                                        padding=ft.padding.all(16),
                                    ),
                                ]),
                            ),
                        ),
                    ],
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                expand=True,
            ),
        ],
    )

def Settings(page: ft.Page):
    page.title = "LinK"

    def toggle_theme(e):
        if e.control.value:
            page.theme_mode = ft.ThemeMode.DARK
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
        page.update()

    def open_link(e):
        webbrowser.open("https://ja.pngtree.com/freepng/a-modern-stylized-fox-with-sharp-geometric-lines-and-bold-head-shape_19753618.html")

    rail = create_navigation_rail(page, selected_index=1)  # Settingsページのインデックスを選択

    return ft.View(
        "/settings",
        [
            ft.Row(
                [
                    rail,
                    ft.VerticalDivider(width=1),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text("Settings", size=24, weight=ft.FontWeight.BOLD),
                                ft.Row(
                                    [
                                        ft.Text("Dark Mode"),
                                        ft.Switch(
                                            value=page.theme_mode == ft.ThemeMode.DARK,
                                            on_change=toggle_theme
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.GestureDetector(
                                    on_tap=open_link,
                                    child=ft.Text(
                                        "からの PNG 画像 ja.pngtree.com",
                                        color=ft.Colors.BLUE,
                                        style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
                                    ),
                                ),
                            ],
                            spacing=20,
                        ),
                        padding=20,  # Containerでpaddingを設定
                    ),
                ],
                expand=True,
            )
        ],
    )

def create_navigation_rail(page: ft.Page, selected_index: int = 0):
    def handle_rail_change(e):
        selected_index = e.control.selected_index
        if selected_index == 0:
            page.go("/home")
        elif selected_index == 1:
            page.go("/settings")
        elif selected_index == 2:
            page.go("/community")
        elif selected_index == 3:
            page.go("/messages")

    return ft.NavigationRail(
        selected_index=selected_index,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        height=700,
        bgcolor=ft.Colors.BLACK54,
        leading=ft.Container(
            content=ft.Image(
                src="images/logos/50px_white.png",
                width=50,
                height=50,
                fit=ft.ImageFit.CONTAIN,
            ),
            margin=ft.margin.only(bottom=20),
        ),
        group_alignment=-0.9,
        on_change=handle_rail_change,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DASHBOARD_OUTLINED,
                selected_icon=ft.Icons.DASHBOARD,
                label="Dashboard",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.SETTINGS_OUTLINED,
                selected_icon=ft.Icons.SETTINGS,
                label="Settings",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.PEOPLE_OUTLINED,
                selected_icon=ft.Icons.PEOPLE,
                label="Community",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FORUM_OUTLINED,
                selected_icon=ft.Icons.FORUM,
                label="Messages",
            ),
        ],
    )

def main(page: ft.Page):
    page.title = "LinK"
    page.bgcolor = ft.Colors.BLACK87

    provider = GoogleOAuthProvider(
        client_id=ClientID,
        client_secret=ClientSecret,
        redirect_url=RedirectUrl
    )

    def route_change(route):
        print(f"Route changed to: {route.route}")
        troute = ft.TemplateRoute(route.route)
        page.views.clear()

        if troute.match("/"):
            page.go("/login")
        elif troute.match("/login"):
            page.views.append(Login(page))
        elif troute.match("/home"):
            print("Navigating to Home view")
            page.views.append(Home(page))
        elif troute.match("/Settings"):
            page.views.append(Settings(page))
        elif troute.match("/waseque/:number"):
            number = route.route.split("/")[-1]
            waseque = next((w for w in sample_waseques if w.number == number), None)
            if waseque:
                page.views.append(view_waseque_details(page, waseque))
        elif troute.match("/api/oauth/redirect"):
            print("Handling OAuth redirect")
            query_params = troute.query_parameters
            code = query_params.get('code')
            if code:
                try:
                    token_url = "https://oauth2.googleapis.com/token"
                    token_data = {
                        'code': code,
                        'client_id': ClientID,
                        'client_secret': ClientSecret,
                        'redirect_uri': RedirectUrl,
                        'grant_type': 'authorization_code'
                    }
                    token_response = requests.post(token_url, data=token_data)
                    token_response.raise_for_status()
                    token_json = token_response.json()
                    access_token = token_json.get('access_token')

                    if access_token:
                        user_info_url = "https://www.googleapis.com/oauth2/v1/userinfo"
                        user_info_params = {'access_token': access_token}
                        user_info_response = requests.get(user_info_url, params=user_info_params)
                        user_info_response.raise_for_status()
                        user_info = user_info_response.json()
                        user_email = user_info.get('email', 'No email found')
                        print(f"User email: {user_email}")
                        page.go(f"/home?email={user_email}")
                    else:
                        print("Failed to obtain access token.")
                except requests.exceptions.RequestException as err:
                    print(f"Error during token exchange or user info retrieval: {err}")

        page.update()

    def view_pop(view):
        print("Popping view")
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

def Home(page: ft.Page):
    email = page.route.split("?email=")[-1]
    return ft.View(
        "/home",
        [
            ft.Text(f"Welcome to Home Page! Email: {email}")
        ]
    )

def Login(page: ft.Page):
    page.title = "LinK"
    page.bgcolor = ft.Colors.BLACK87

    def login_google(e):
        print("Attempting to log in...")
        # Fletのlaunch_urlを使用してリダイレクト
        auth_url = (
            "https://accounts.google.com/o/oauth2/auth"
            f"?client_id={ClientID}"
            f"&redirect_uri={RedirectUrl}"
            "&response_type=code"
            "&scope=email%20profile%20openid"
            "&access_type=offline"
        )
        page.launch_url(auth_url)

    def logout_google(e):
        print("Logging out...")
        page.logout()

    login_button = Container(
        content=ElevatedButton(
            "Sign in with Google", bgcolor=ft.Colors.LIGHT_BLUE_500, color=ft.Colors.WHITE, on_click=login_google,
        ),
        margin=ft.margin.only(right=10)
    )

    def on_login(e):
        if e.error:
            print("Login error:", e.error)
        else:
            user_email = page.auth.user.get('email', 'No email found')
            print(f"User email: {user_email}")
            page.go(f"/home?email={user_email}")

    def on_logout(e):
        print("Logged out.")
        page.go("/logout")

    login_button = Container(
        content=ElevatedButton(
            "Sign in with Google", bgcolor=ft.Colors.LIGHT_BLUE_500, color=ft.Colors.WHITE, on_click=login_google,
        ),
        margin=ft.margin.only(right=10)
    )

    page.on_login = on_login
    page.on_logout = on_logout

    return ft.View(
        "/login",
        [
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Image(
                                            src="images/logos/50px_white.png",
                                            width=150,
                                            height=150,
                                            fit=ft.ImageFit.CONTAIN,
                                        ),
                                        ft.Text("Welcome back!", size=16, color=ft.Colors.GREY_400),
                                        ft.Container(height=20),
                                        login_button,
                                    ],
                                    spacing=15,
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                width=400,
                                height=500,
                                padding=ft.padding.all(40),
                                border_radius=15,
                                bgcolor=ft.Colors.BLACK54,
                                shadow=ft.BoxShadow(
                                    spread_radius=0,
                                    blur_radius=25,
                                    color=ft.Colors.with_opacity(0.3, ft.Colors.BLUE_GREY_100),
                                    offset=ft.Offset(0, 4)
                                ),
                                border=ft.border.all(0.5, ft.Colors.BLUE_GREY_700),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True,
            )
        ],
    )


if __name__ == "__main__":
    ft.app(target=main, port=8000, view=ft.AppView.WEB_BROWSER)
