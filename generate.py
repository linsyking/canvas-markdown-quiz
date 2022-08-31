# coding=utf-8
'''
@Author: King
@Date: 2022-08-31 星期三 10-51-42
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

import yaml
import re
import config
from canvasapi import course, requester
from markdown import markdown



class quiz_utils:
    def _re(self, m_target: str, m_pattern: str):
        rec = re.compile(m_pattern)
        return re.findall(rec, m_target)

    def _decode_yaml(self, m_string: str):
        return yaml.safe_load(m_string)

    def _render_md(self, m_string: str):
        html = markdown(m_string,
                        extensions=["codehilite", "fenced_code", "mdx_math_img"],
                        extension_configs={
                            'mdx_math_img': {
                                'enable_dollar_delimiter': True,
                                'add_preview': True
                            }
                        }
                        )
        return html

class quiz_maker(quiz_utils):
    def __init__(self, course_id: int) -> None:
        self.__init_canvas(course_id)
        # Quiz Meta Info
        self.quiz_p = {}
        # All quiz questions
        self.quiz_aq = []
        self.inited = False

    def init_by_file_path(self, fp):
        with open(fp, "r") as f:
            self.file_content = f.read()
        self.inited = True

    def init_by_file_content(self, fc):
        self.file_content = fc
        self.inited = True

    def __init_canvas(self, course_id: int):
        # Load Canvas Facility by file
        self.c_req = requester.Requester(
            config.CANVAS_API_URL, config.CANVAS_API_KEY)
        self.c_course_id = course_id
        self.c_course = course.Course(self.c_req, {"id": course_id})

    def create_quiz(self):
        self.__parse_md()

        # Publish
        myquiz = self.c_course.create_quiz(self.quiz_p)

        for q in self.quiz_aq:
            myquiz.create_question(question = q)

        print("Success")

    def __parse_md(self):
        # Parse the md file

        if not self.inited:
            raise RuntimeError(
                "Use `init_by_file_path` or `init_by_file_content` to initialize.")

        q_blocks = self.file_content.split("---")
        q_meta_info = self._decode_yaml(q_blocks[1].strip())
        q_title, q_desc = self.__get_title_and_desc(q_blocks[2])
        self.quiz_p["title"] = q_title
        self.quiz_p["description"] = q_desc + config.HTML_SCRIPT
        self.quiz_p.update(q_meta_info)

        for q_qid in range(3, len(q_blocks)):
            m_q = question(q_blocks[q_qid]).parse()
            self.quiz_aq.append(m_q)


    def __get_title_and_desc(self, block: str):
        res = self._re(block.strip(), r"# (.*?)[\n\r]+([^\n\r][\s\S]*)")[0]
        return res[0], self._render_md(res[1])



class question(quiz_utils):
    def __init__(self, block: str) -> None:
        self.raw = block.strip()

    def parse(self):
        # Parse
        m_q = {}
        # print(self.raw)
        res = self._re(self.raw, r"```.*([\s\S]+?)```([\s\S]*)$")[0]
        q_meta = self._decode_yaml(res[0].strip()) 
        q_desc = self._render_md(res[1].strip())
        m_q.update(q_meta)
        m_q["question_text"]=q_desc
        return m_q


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: ./generate.py <md filepath>")
        exit(0)
    qm = quiz_maker(config.COURSE_ID)
    qm.init_by_file_path(sys.argv[1])
    qm.create_quiz()
