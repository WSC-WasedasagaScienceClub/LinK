import flet as ft
from flet.auth.providers.google_oauth_provider import GoogleOAuthProvider
import os
from dotenv import load_dotenv
import webbrowser

load_dotenv()

ClientID = os.getenv('ClientID')
ClientSecret = os.getenv('ClientSecret')
RedirectUrl = os.getenv('RedirectUrl')

def Login(page: ft.Page):
    page.title = "LinK"
    page.bgcolor = ft.Colors.BLACK87

    # GoogleOAuthのProvider定義
    provider = GoogleOAuthProvider(
        client_id=ClientID,
        client_secret=ClientSecret,
        redirect_url=RedirectUrl
    )

    # ログイン処理
    def login_google(e):
        # 親ウィンドウでリダイレクトを処理
        page.login(provider, use_popup=False)

    # ログアウト処理
    def logout_google(e):
        page.logout()

    # ログインボタン
    login_button = ft.Container(
        content=ft.ElevatedButton(
            "Sign in with Google", bgcolor=ft.Colors.LIGHT_BLUE_500, color=ft.Colors.WHITE, on_click=login_google,
        ),
        margin=ft.margin.only(right=10)
    )

    def on_login(e):
        print(page.auth.user['name'], page.auth.user['email'])
        page.go("/home")

    def on_logout(e):
        page.go("/logout")

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