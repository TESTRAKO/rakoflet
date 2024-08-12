import flet as ft

def main(page: ft.Page):
    # إنشاء عنصر إدخال نصي
    input_field = ft.TextField(label="Enter your name:", width=300)
    
    # إنشاء زر لعرض النص المدخل
    def on_submit(e):
        page.controls.append(ft.Text(f"Hello, {input_field.value}!"))
        input_field.value = ""  # تنظيف الحقل بعد الإدخال

    submit_button = ft.Button(text="Submit", on_click=on_submit)

    # إضافة العناصر إلى الصفحة
    page.add(input_field, submit_button)

# تشغيل التطبيق
ft.app(target=main)
