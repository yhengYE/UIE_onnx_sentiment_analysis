import os
import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QComboBox, QLineEdit
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from uie_predictor import run_analysis
from jd_crawler import JDCrawler  # 导入爬虫模块
import name2id

class MyApp(QWidget):
    crawl_finished = pyqtSignal(list)  # 定义一个信号，当爬虫完成时发送

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('评论情感分析系统')
        self.setGeometry(300, 300, 1200, 800)

        main_layout = QHBoxLayout()

        left_layout = QVBoxLayout()

        # 添加一个水平布局，用于爬虫按钮和输入框
        top_layout = QHBoxLayout()
        self.input_line = QLineEdit(self)
        self.input_line.setFont(QFont('Arial', 13))
        self.input_line.setPlaceholderText('输入需要爬取的商品名称')
        top_layout.addWidget(self.input_line)

        self.crawl_btn = QPushButton('开始爬虫', self)
        self.crawl_btn.setFixedHeight(30)
        self.crawl_btn.setFont(QFont('Arial', 14))
        top_layout.addWidget(self.crawl_btn)
        self.crawl_btn.clicked.connect(self.start_crawling)

        left_layout.addLayout(top_layout)

        self.textbox = QTextEdit(self)
        self.textbox.setFont(QFont('Arial', 14))
        left_layout.addWidget(self.textbox)

        self.analyze_btn = QPushButton('开始分析', self)
        self.analyze_btn.setFixedHeight(50)
        self.analyze_btn.setFont(QFont('Arial', 14))
        left_layout.addWidget(self.analyze_btn)
        self.analyze_btn.clicked.connect(self.start_analysis)

        self.import_btn = QPushButton('导入外部文档', self)
        self.import_btn.setFixedHeight(50)
        self.import_btn.setFont(QFont('Arial', 14))
        left_layout.addWidget(self.import_btn)
        self.import_btn.clicked.connect(self.import_txt)

        self.status_label = QLabel('准备就绪', self)
        self.status_label.setFont(QFont('Arial', 16))
        left_layout.addWidget(self.status_label)

        main_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("选择要显示的图片")
        self.combo_box.addItem("方面词云")
        self.combo_box.addItem("方面频次统计")
        self.combo_box.addItem("方面极性词云")
        self.combo_box.addItem("方面极性频次统计")
        self.combo_box.addItem("正向方面观点")
        self.combo_box.addItem("正向方面观点频率")
        self.combo_box.addItem("方面情感极性")
        self.combo_box.addItem("观点词云")
        self.combo_box.addItem("观点频率")
        self.combo_box.addItem("负向方面情感频率")
        self.combo_box.addItem("负向方面观点")
        self.combo_box.addItem("正负对比")
        self.combo_box.setFont(QFont('Arial', 14))
        self.combo_box.setVisible(False)

        self.combo_box.activated[str].connect(self.on_combo_box_activated)
        right_layout.addWidget(self.combo_box)

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(700, 800)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFont(QFont('Arial', 14))
        right_layout.addWidget(self.image_label)

        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

        self.exported_file_path = "input.txt"
        self.output_dir = "output_images"

        self.crawl_finished.connect(self.display_comments)  # 连接信号和槽

    def import_txt(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", "", "Text Files (*.txt);;All Files (*)",
                                                   options=options)
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                self.textbox.setPlainText(content)

    def start_analysis(self):
        self.status_label.setText('分析中...')
        self.status_label.repaint()

        text = self.textbox.toPlainText()
        with open(self.exported_file_path, 'w', encoding='utf-8') as file:
            file.write(text)

        try:
            run_analysis(file_path=self.exported_file_path, save_path="output.json")
            self.call_visual_analysis()
            self.status_label.setText('分析完成')
            self.combo_box.setVisible(True)
        except Exception as e:
            print(f"分析时发生错误: {e}")
            self.status_label.setText('分析失败')

    def call_visual_analysis(self):
        import argparse
        from visual_analysis import default_visual_analysis

        args = argparse.Namespace(
            file_path="output.json",
            save_dir=self.output_dir,
            font_path=None,
            task_type="ext",
            options=None
        )

        default_visual_analysis(args)
    def on_combo_box_activated(self, text):
        if text == "选择要显示的图片":
            return

        image_name_map = {
            "方面词云": "aspect_wc.png",
            "方面频次统计": "aspect_hist.png",
            "方面极性词云": "aspect_opinion_wc.png",
            "方面极性频次统计": "aspect_opinion_hist.png",
            "正向方面观点": "aspect_opinion_wc_pos.png",
            "正向方面观点频率": "aspect_opinion_hist_pos.png",
            "方面情感极性": "aspect_sentiment_wc.png",
            "观点词云": "opinion_wc.png",
            "观点频率": "opinion_hist.png",
            "负向方面情感频率": "aspect_opinion_hist_neg.png",
            "负向方面观点": "aspect_opinion_wc_neg.png",
            "正负对比": "aspect_sentiment_hist.png"
        }

        if text in image_name_map:
            image_path = os.path.join(self.output_dir, image_name_map[text])
            if os.path.exists(image_path):
                pixmap = QPixmap(image_path)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio))
            else:
                self.image_label.setText(f"{text} 图片不存在")

    def start_crawling(self):
        self.status_label.setText('爬虫中...')
        self.status_label.repaint()

        keyword = self.input_line.text()
        if not keyword:
            self.status_label.setText('请输入商品名称')
            return

        crawling_thread = threading.Thread(target=self.run_crawler_in_thread, args=(keyword,))
        crawling_thread.start()

    def run_crawler_in_thread(self, keyword):
        try:
            crawler = JDCrawler(keyword, name2id.n2id)
            comments = crawler.crawl()
            self.crawl_finished.emit(comments)  # 发出信号，传递评论数据
        except Exception as e:
            print(f"爬虫时发生错误: {e}")
            self.status_label.setText('爬虫失败')

    @pyqtSlot(list)
    def display_comments(self, comments):
        self.textbox.clear()
        for comment in comments:
            self.textbox.append(comment)
        self.status_label.setText('爬虫完成')

def main():
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
