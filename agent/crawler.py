from bs4 import BeautifulSoup
import re

class Crawler:
    def __init__(self):
        self.html_doc = """
        <html>
            <head>
                <title>Home</title>
            </head>
            <body>
                <div class="section">
                    <h2>영역 제목</h2>
                    <ul>
                        <li><a href="/news/news1">기사 제목1</a></li>
                        <li><a href="/news/news2">기사 제목2</a></li>
                        <li><a href="/news/news3">기사 제목3</a></li>
                    </ul>
                </div>
            </body>
        </html>
        """

        self.html_table = """
        <html>
            <div class="aside_section">
                <table class="tbl">
                    <thread>
                        <tr>
                            <th scope="col">컬럼1</th>
                            <th scope="col">컬럼2</th>
                        </tr>
                    </thread>
                    <tbody>
                        <tr>
                            <th><a href="/aside1">항목1</a></th>
                            <td>항목1값1</td>
                            <td>항목2값2</td>
                        </tr>
                        <tr>
                            <th><a href="aside2">항목2</a></th>
                            <td>항목2값1</td>
                            <td>항목2값2</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </html>
        """