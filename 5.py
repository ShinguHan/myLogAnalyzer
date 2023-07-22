from PySide6.QtWidgets import QApplication, QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QFrame, QFileDialog
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["AGV", "CNV", "STK"])
        self.combo_box.currentTextChanged.connect(self.load_file)

        self.web_view = QWebEngineView()
        self.detail_view = QWebEngineView()
        
        # Set a simple border style to detail view
        self.detail_view.setStyleSheet("border: 1px solid lightgray;")

        layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.combo_box)
        left_layout.addWidget(self.web_view)

        layout.addLayout(left_layout)
        layout.addWidget(self.detail_view)

        self.setLayout(layout)

    def load_file(self, text):
        # Let the user choose the standard file and the file to compare
        standard_file, _ = QFileDialog.getOpenFileName(self, "Select Standard File", "", "Markdown Files (*.md)")
        compare_file, _ = QFileDialog.getOpenFileName(self, "Select File to Compare", "", "Markdown Files (*.md)")

        differences = self.compare_files(standard_file, compare_file)

        with open(standard_file, "r") as file:
            content = file.read()

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://unpkg.com/mermaid/dist/mermaid.min.js"></script>
            <style>
                .difference {{
                    fill: red !important;
                    stroke: red !important;
                }}
            </style>
            <script>
                mermaid.initialize({{'startOnLoad':true}});
                window.onload = function() {{
                    var messages = document.querySelectorAll('.messageText');
                    messages.forEach(function(message, index) {{
                        message.addEventListener('click', function(e) {{
                            messages.forEach(function(msg) {{
                                msg.classList.remove('difference');
                            }});
                            this.classList.add('difference');
                            document.getElementById('detail').textContent = this.textContent;
                        }});
                        if ({differences}.includes(index)) {{
                            message.classList.add('difference');
                        }}
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

    def compare_files(self, standard_file, compare_file):
        with open(standard_file, "r") as sf, open(compare_file, "r") as cf:
            standard_lines = sf.readlines()
            compare_lines = cf.readlines()

        # Find the lines that exist in the standard file but not in the compare file at the same position
        differences = [i for i in range(len(standard_lines)) if i >= len(compare_lines) or standard_lines[i] != compare_lines[i]]

        return differences



if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()