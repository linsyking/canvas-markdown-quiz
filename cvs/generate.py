#!/usr/bin/env python3
'''
@Author: King
@Date: 2022-09-01 09-41-09
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

import yaml
import re
from .default import HTML_HEADER
from canvasapi import course, requester
from markdown import markdown


class quiz_utils:
    def _re(self, m_target: str, m_pattern: str):
        rec = re.compile(m_pattern)
        return re.findall(rec, m_target)

    def _decode_yaml(self, m_string: str):
        return yaml.safe_load(m_string)

    def _render_md(self, m_string: str):
        m_ext = ["codehilite", "fenced_code", "mdx_math_img"]
        m_ext_conf = {
            'mdx_math_img': {
                'enable_dollar_delimiter': True,
                'add_preview': True
            }
        }
        if "markdown_options" in self.options:
            m_opt = self.options["markdown_options"]
            if "extensions" in m_opt:
                m_ext = m_opt["extensions"]
            if "extension_configs" in m_opt:
                m_ext_conf = m_opt["extension_configs"]
        html = markdown(m_string,
                        extensions=m_ext,
                        extension_configs=m_ext_conf
                        )
        return html


class quiz_maker(quiz_utils):
    def __init__(self,  api_url: str, api_key: str, options) -> None:
        self.api_url = api_url
        self.api_key = api_key
        # Quiz Meta Info
        self.quiz_p = {}
        # All quiz questions
        self.quiz_aq = []
        self.quiz_groups = []
        self.inited = False
        self.options = options

        if "html_header" in options:
            self.html_header = options["html_header"]
        else:
            self.html_header = HTML_HEADER

    def set_courseid(self, id: int):
        self.__init_canvas(id)

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
            self.api_url, self.api_key)
        self.c_course_id = course_id
        self.c_course = course.Course(self.c_req, {"id": course_id})

    def create_quiz(self):
        self.__parse_md()

        # print(self.quiz_groups)
        # print(self.quiz_aq)

        # Publish
        myquiz = self.c_course.create_quiz(self.quiz_p)

        if len(self.quiz_groups) > 0:
            g_name2id = {}
            for group in self.quiz_groups:
                resp_group = myquiz.create_question_group([group])
                g_name2id[group["name"]] = resp_group.id
            for q in self.quiz_aq:
                if "quiz_group_id" in q:
                    q["quiz_group_id"] = g_name2id[q["quiz_group_id"]]
                myquiz.create_question(question=q)
        else:
            for q in self.quiz_aq:
                myquiz.create_question(question=q)

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
        self.quiz_p["description"] = q_desc + self.html_header
        self.quiz_p.update(q_meta_info)

        # By default no groups are enabled
        cur_group_name = ""
        for q_qid in range(3, len(q_blocks)):
            m_q = question(q_blocks[q_qid], self.options).parse()
            if "question_text" not in m_q:
                # Create a group
                cur_group_name = m_q["name"]
                if cur_group_name != "":
                    self.quiz_groups.append(dict(m_q))
                continue
            if cur_group_name != "":
                # Inside a group
                m_q["quiz_group_id"] = cur_group_name
            self.quiz_aq.append(m_q)

    def __get_title_and_desc(self, block: str):
        res = self._re(block.strip(), r"# (.*?)[\n\r]+([^\n\r][\s\S]*)")[0]
        return res[0], self._render_md(res[1])


class question(quiz_utils):
    def __init__(self, block: str, options) -> None:
        self.raw = block.strip()
        self.options = options

    def parse(self):
        # Parse
        m_q = {}
        # print(self.raw)
        res = self._re(self.raw, r"```.*([\s\S]+?)```([\s\S]*)$")[0]
        q_meta = self._decode_yaml(res[0].strip())
        q_desc = self._render_md(res[1].strip())
        m_q.update(q_meta)
        if len(q_desc) > 0:
            m_q["question_text"] = q_desc
        return m_q
