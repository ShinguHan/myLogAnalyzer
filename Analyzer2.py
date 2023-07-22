from PySide6.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["AGV", "CNV", "STK"])
        self.combo_box.currentTextChanged.connect(self.load_file)

        self.web_view = QWebEngineView()

        layout = QVBoxLayout()
        layout.addWidget(self.combo_box)
        layout.addWidget(self.web_view)
        self.setLayout(layout)

    def load_file(self, text):
        # Adjust this method to load the markdown file based on the selected category
        with open(f"{text}.md", "r") as file:
            content = file.read()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://unpkg.com/mermaid/dist/mermaid.min.js"></script>
            <style>
                .clicked {{
                    fill: red !important;
                    stroke: red !important;
                }}
            </style>
            <script>
                mermaid.initialize({{'startOnLoad':true}});
                window.onload = function() {{
                    var messages = document.querySelectorAll('.messageText');
                    messages.forEach(function(message) {{
                        message.addEventListener('click', function(e) {{
                            messages.forEach(function(msg) {{
                                msg.classList.remove('clicked');
                            }});
                            this.classList.add('clicked');
                            document.getElementById('detail').textContent = this.textContent;
                        }});
                    }});
                }};
            </script>
        </head>
        <body>
            <div class="mermaid">
                {content}
            </div>
            <div id="detail"></div>
        </body>
        </html>
        """

        self.web_view.setHtml(html)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
