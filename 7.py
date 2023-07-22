from PySide6.QtWidgets import QApplication, QComboBox, QHBoxLayout, QVBoxLayout, QWidget, QFrame, QFileDialog, QPushButton
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Qt
import csv
import re

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.combo_box = QComboBox()
        self.combo_box.addItems(["AGV", "CNV", "STK"])
        self.combo_box.currentTextChanged.connect(self.load_standard_file)

        self.compare_button = QPushButton("Compare with...")
        self.compare_button.clicked.connect(self.load_compare_file)

        self.web_view = QWebEngineView()
        self.detail_view = QWebEngineView()
        
        # Set a simple border style to detail view
        self.detail_view.setStyleSheet("border: 1px solid lightgray;")

        layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.combo_box)
        left_layout.addWidget(self.compare_button)
        left_layout.addWidget(self.web_view)

        layout.addLayout(left_layout)
        layout.addWidget(self.detail_view)

        self.setLayout(layout)

    def load_standard_file(self, text):
        # Let the user choose the standard file
        self.standard_file, _ = QFileDialog.getOpenFileName(self, "Select Standard File", "", "Markdown Files (*.md)")
        self.load_file(self.standard_file)

    def load_compare_file(self):
        # Let the user choose the file to compare
        compare_file, _ = QFileDialog.getOpenFileName(self, "Select File to Compare", "", "Markdown Files (*.csv)")
        differences = self.compare_files(self.standard_file, compare_file)
        self.load_file(self.standard_file, differences)

    def load_file(self, file, differences=[]):
        with open(file, "r", encoding='utf-8') as file:
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
                .hovered {{
                    fill: lightgray !important;
                    stroke: lightgray !important;
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
                        message.addEventListener('mouseover', function(e) {{
                            this.classList.add('hovered');
                        }});
                        message.addEventListener('mouseout', function(e) {{
                            this.classList.remove('hovered');
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
        with open(standard_file, "r", encoding='utf-8') as sf:
            standard_lines = sf.readlines()

        with open(compare_file, "r", encoding='utf-8') as cf:
            lines = cf.readlines()
            compare_data = [line.split(',') for line in lines]
            
        for str in compare_data:
            print(str)

        # Extract CEID values from the standard file
        standard_ceids = [re.search(r'CEID = (\d+)', line).group(1) for line in standard_lines if 'S6F11' in line]

        # Extract CEID values from the compare file
        compare_ceids = [re.search(r'<U2 (\d+)>', line[7]).group(1) for line in compare_data if line[0] == '"Com"' and 'S01F03' in line[7]]

        # Find the CEIDs that exist in the standard file but not in the compare file
        differences = [ceid for ceid in standard_ceids if ceid not in compare_ceids]

        return differences


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
