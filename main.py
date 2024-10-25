import flet as ft
import asyncio
from google_mobile_ads import initialize_mobile_ads, load_rewarded_ad, show_rewarded_ad

class RewardedAdApp:
    def __init__(self):
        self.points = 0
        self.ad_unit_id = "ca-app-pub-2795005033779813/1585312974"
        self.app_id = "ca-app-pub-2795005033779813~6258221006"
        self.package_name = "com.aapp.sh"

    async def main(self, page: ft.Page):
        page.title = "تطبيق الإعلانات المكافئة"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # تهيئة SDK الإعلانات
        await initialize_mobile_ads(self.app_id, self.package_name)

        self.points_text = ft.Text(f"النقاط: {self.points}", size=20)
        
        async def show_rewarded_ad(e):
            ad_button.disabled = True
            page.update()
            
            # تحميل وعرض الإعلان المكافئ
            ad = await load_rewarded_ad(self.ad_unit_id)
            if ad:
                result = await show_rewarded_ad(ad)
                if result.rewarded:
                    self.points += result.reward_amount
                    self.points_text.value = f"النقاط: {self.points}"
            
            ad_button.disabled = False
            page.update()

        ad_button = ft.ElevatedButton("عرض الإعلان", on_click=show_rewarded_ad)

        page.add(
            ft.Column(
                [
                    self.points_text,
                    ad_button
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

if __name__ == "__main__":
    app = RewardedAdApp()
    ft.app(target=app.main)
