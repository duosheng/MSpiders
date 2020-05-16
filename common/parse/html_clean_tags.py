#! /usr/bin/python
# -*- coding:utf-8 -*-
'''
Created on 2013-12-18

@author: Java
'''
import re

from html5lib import HTMLParser


class FilterTag():
    def __init__(self):
        pass

    def filterHtmlTag(self, htmlStr):
        '''
        过滤html中的标签
        :param htmlStr:html字符串 或是网页源码
        '''
        self.htmlStr = htmlStr
        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlStr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        blank_line = re.compile('\n+')  # 去掉多余的空行
        s = blank_line.sub('\n', s)
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('\n+')
        s = blank_line.sub('\n', s)
        filterTag = FilterTag()
        s = filterTag.replaceCharEntity(s)  # 替换实体
        print(s)

    def replaceCharEntity(self, htmlStr):
        '''
        替换html中常用的字符实体
        使用正常的字符替换html中特殊的字符实体
        可以添加新的字符实体到CHAR_ENTITIES 中
    CHAR_ENTITIES是一个字典前面是特殊字符实体  后面是其对应的正常字符
        :param htmlStr:
        '''
        self.htmlStr = htmlStr
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }
        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlStr)
        while sz:
            entity = sz.group()  # entity全称，如>
            key = sz.group('name')  # 去除&;后的字符如（" "--->key = "nbsp"）    去除&;后entity,如>为gt
            try:
                htmlStr = re_charEntity.sub(CHAR_ENTITIES[key], htmlStr, 1)
                sz = re_charEntity.search(htmlStr)
            except KeyError:
                # 以空串代替
                htmlStr = re_charEntity.sub('', htmlStr, 1)
                sz = re_charEntity.search(htmlStr)
        return htmlStr

    def replace(self, s, re_exp, repl_string):
        return re_exp.sub(repl_string)

    def strip_tags(self, htmlStr):
        '''
        使用HTMLParser进行html标签过滤
        :param htmlStr:
        '''

        self.htmlStr = htmlStr
        htmlStr = htmlStr.strip()
        htmlStr = htmlStr.strip("\n")
        result = []
        parser = HTMLParser()
        parser.handle_data = result.append
        parser.feed(htmlStr)
        parser.close()
        return ''.join(result)

    def stripTagSimple(self, htmlStr):
        '''
        最简单的过滤html <>标签的方法    注意必须是<任意字符>  而不能单纯是<>
        :param htmlStr:
        '''
        htmlStr = htmlStr.replace("\xa0", "  ").replace("\u3000", "  ")
        dr = re.compile(r'</?\w+[^>]*>', re.S)
        htmlStr = re.sub(dr, '\n', htmlStr)
        # htmlStr = htmlStr.replace("?", " ")
        return htmlStr


if __name__ == '__main__':
    #     s = file('Google.html').read()
    filters = FilterTag()
    print(filters.strip_tags('<div class="zw"><p style="text-align: right;">粤科函综字〔2019〕35号</p><p style="text-align: left;">各有关单位：</p><p style="text-align: left;">　　为加强项目管理服务，根据省人才办有关工作要求，入选2017年度“珠江人才计划”引进高层次人才（“海外来粤短期工作专家”除外）与用人单位及项目管理单位三方需签订《“珠江人才计划”引进高层次人才资助合同书》（以下简称《合同书》，见附件），现将有关事项通知如下：</p><p style="text-align: left;">　　一、要高度重视合同签订工作</p><p style="text-align: left;">　　签订《合同书》是本次“珠江人才计划”引进高层次人才的重要环节。2017年度认定引进的科技创新领军人才、高端经济管理人才、金融人才、青年拔尖人才都要由用人单位、引进人才本人以及项目管理单位三方签订《合同书》。《合同书》明确了用人单位是本次引进人才主体，引进人才本人是本次引进项目荣誉受益人，项目管理单位是见签和监督者，进一步明确了三方的责任、权利和义务，是引进高层次人才项目管理服务的重要依据。请各用人单位、入选高层次人才务必高度重视此次合同签订，认真做好相关工作。签订的《合同书》待省科技厅确认后，方可启用相应的人才生活补贴资金。</p><p style="text-align: left;">　　二、几点要求</p><p style="text-align: left;">　　（一） 本次签订《合同书》涉及用人单位和引进人才较多，时间紧急，请各有关单位加强组织，指定专人负责，及时联络沟通，按时完成合同签订工作。</p><p style="text-align: left;">　　（二） 用人单位和引进人才要认真阅读《合同书》条款特别是承诺内容，严格填写《合同书》中引进高层次人才基本情况和用人单位基本信息，严格履行承诺及合同约定事项。</p><p style="text-align: left;">　　（三） 每份《合同书》中的“来粤工作承诺书”必须由引进人才本人亲笔签名、用人单位加盖公章，“签署意见”必须由引进人才亲笔签名及用人单位法定代表人签名并加盖单位公章。</p><p style="text-align: left;">　　（四） 各用人单位签订《合同书》前要进行严格审查，有下列情形之一的，不予签订合同不得拨付资金：1.入选人才已经离开广东不在原来申报用人单位工作的；2.入选人才无法履行与用人单位签订劳动合同的。</p><p style="text-align: left;">　　（五） 请将填妥的《合同书》提供一式4份，由用人单位于1月23日前寄至省科技厅1楼综合业务办理大厅。《合同书》电子版可在省科技厅官网（www.gdstc.gov.cn）“通知公告”中下载。</p><p style="text-align: left;">　　业务咨询联系人：黄可，电话：020-83163662</p><p style="text-align: left;">　　地址：广州市连新路171号信息大楼1楼综合业务办理大厅<br>　　附件：<a href="http://www.gdstc.gov.cn/msg/image_new/wenjian/2019/01/20190111wzj01-01.doc">“珠江人才计划”引进高层次人才资助合同书</a>　　　　　</p><p style="text-align: right;"><br></p><p style="text-align: right;">广东省科学技术厅<br>2019年1月9日</p><div class="fj" style="margin-top:15px;"></div></div>'))







