import flet as ft
import re
import webbrowser
import platform
import subprocess

def main(page: ft.Page):
    page.title = "WV.cash"
    page.padding = 20
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    page.window_height = 650

    def validate_phone(phone):
        return re.match(r'^01[0125][0-9]{8}$', phone) is not None

    def validate_ussd_code(code):
        return re.match(r'^\*[0-9*]+#$', code) is not None

    def call_ussd(ussd_code):
        system = platform.system()
        if system == "Android":
            try:
                import android
                android.activity.dial(ussd_code)
            except ImportError:
                webbrowser.open(f"tel:{ussd_code}")
        elif system == "iOS":
            webbrowser.open(f"tel:{ussd_code}")
        elif system == "Windows":
            subprocess.run(["start", f"tel:{ussd_code}"], shell=True)
        elif system == "Darwin":  # macOS
            subprocess.run(["open", f"tel:{ussd_code}"])
        else:
            print(f"غير قادر على الاتصال تلقائيًا. الرجاء استخدام الكود: {ussd_code}")

    def copy_to_clipboard(e):
        page.set_clipboard(ussd_code_display.value)
        page.show_snack_bar(ft.SnackBar(content=ft.Text("تم نسخ الكود إلى الحافظة")))

    def clear_fields(e):
        phone1.value = ""
        phone2.value = ""
        amount.value = ""
        result.visible = False
        ussd_code_display.visible = False
        copy_button.visible = False
        call_button.visible = False
        page.update()

    def on_submit(e):
        is_valid = True
        if not validate_phone(phone1.value):
            result.value = "رقم الهاتف الأول غير صحيح"
            result.color = ft.colors.RED
            is_valid = False
        elif not validate_phone(phone2.value):
            result.value = "رقم الهاتف الثاني غير صحيح"
            result.color = ft.colors.RED
            is_valid = False
        elif not amount.value.isdigit():
            result.value = "المبلغ يجب أن يكون أرقامًا فقط"
            result.color = ft.colors.RED
            is_valid = False
        elif phone1.value != phone2.value:
            result.value = "الأرقام غير متطابقة"
            result.color = ft.colors.RED
            is_valid = False

        if is_valid:
            ussd_code = f"*9*7*{phone1.value}*{amount.value}#"
            if validate_ussd_code(ussd_code):
                result.value = "تم التحقق بنجاح!"
                result.color = ft.colors.GREEN
                ussd_code_display.value = ussd_code
                ussd_code_display.visible = True
                copy_button.visible = True
                call_button.visible = True
            else:
                result.value = "كود USSD غير صالح"
                result.color = ft.colors.RED
                is_valid = False

        result.visible = True
        if not is_valid:
            ussd_code_display.visible = False
            copy_button.visible = False
            call_button.visible = False
        page.update()

    def confirm_call(e):
        def on_confirm(e):
            if e.control.text == "نعم":
                call_ussd(ussd_code_display.value)
            dialog.open = False
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("تأكيد الاتصال"),
            content=ft.Text("هل أنت متأكد أنك تريد إجراء الاتصال؟"),
            actions=[
                ft.TextButton("نعم", on_click=on_confirm),
                ft.TextButton("لا", on_click=on_confirm),
            ],
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        page.update()

    phone1 = ft.TextField(label="رقم الهاتف الأول", prefix_icon=ft.icons.PHONE)
    phone2 = ft.TextField(label="تأكيد رقم الهاتف", prefix_icon=ft.icons.PHONE_CALLBACK)
    amount = ft.TextField(label="المبلغ", prefix_icon=ft.icons.ATTACH_MONEY)
    submit_btn = ft.ElevatedButton("تحقق", on_click=on_submit, icon=ft.icons.CHECK_CIRCLE)
    clear_btn = ft.ElevatedButton("مسح", on_click=clear_fields, icon=ft.icons.CLEAR)
    result = ft.Text(visible=False, size=16)
    ussd_code_display = ft.Text(visible=False, size=18, weight=ft.FontWeight.BOLD)
    copy_button = ft.ElevatedButton("نسخ الكود", on_click=copy_to_clipboard, visible=False)
    call_button = ft.ElevatedButton("اتصال", on_click=confirm_call, visible=False)
    theme_switch = ft.Switch(label="الوضع الليلي", on_change=toggle_theme)

    page.add(
        ft.Column(
            [
                ft.Text("تطبيق التحقق من الأرقام", size=24, weight=ft.FontWeight.BOLD),
                phone1,
                phone2,
                amount,
                ft.Row([submit_btn, clear_btn], alignment=ft.MainAxisAlignment.CENTER),
                result,
                ussd_code_display,
                ft.Row([copy_button, call_button], alignment=ft.MainAxisAlignment.CENTER),
                theme_switch,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )
    )

ft.app(target=main)
