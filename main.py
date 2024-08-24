from flet import Page, Text, TextField, ElevatedButton, Column, app, Row
import yt_dlp

# Function to download the video
def download_video(url, output_path='c:\\00\\vids'):
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "Download completed successfully!"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main function for Flet application
def main(page: Page):
    page.title = "YouTube Video Downloader"
    page.window_width = 400
    page.window_height = 300

    # UI components
    url_input = TextField(label="Enter video URL", width=350, autofocus=True)
    download_button = ElevatedButton(text="Download", on_click=lambda _: start_download())
    status_text = Text(value="", size=14, color="green")

    # Function to handle button click
    def start_download():
        url = url_input.value
        if url:
            status_text.value = "Downloading..."
            page.update()  # Update the page to show the status change
            result = download_video(url)
            status_text.value = result
            page.update()  # Update the page to show the final status

    # Adding components to the page
    page.add(
        Column(
            [
                Text(value="YouTube Video Downloader", size=20, weight="bold"),
                Row([url_input]),
                Row([download_button]),
                Row([status_text]),
            ],
            alignment="center",
            spacing=10
        )
    )

# Run the Flet app
app(target=main)
