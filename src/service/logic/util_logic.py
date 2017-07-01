import math


class UtilLogic:
    exec_result = True

    def new_result_page(self, result=None, list_filter=None, total=None):
        self._verify_except_case()

        _result_row = [m.parse() for m in result]
        _page = {
            "cur_page": list_filter.page_num,
            "max_page": math.ceil(total / list_filter.page_size),
            "total_rows": 0 if total is None else total
        }

        return _result_row, _page

    def result_page(self, result_page=None):
        self._verify_except_case()

        _result_row = [m.parse() for m in result_page.items]
        _page = {
            "cur_page": result_page.page,
            "max_page": result_page.pages,
            "total_rows": result_page.total
        }

        return _result_row, _page

    def _verify_except_case(self, case=None):
        self.exec_result = True
        pass


class ListFilter:
    page_num = 1
    page_size = 100
    publish_status = 0
    is_recommend = 0
    offset_limit_sql = ""
    filter_sql = "1=1"

    def base_parse(self, data_filter=None):
        if data_filter is not None:
            self.page_num = 1 if 'page_num' not in data_filter else data_filter['page_num']
            self.page_size = 1 if 'page_size' not in data_filter else data_filter['page_size']

            if 'publish_status' in data_filter:
                self.publish_status = data_filter['publish_status']
            if 'is_recommend' in data_filter:
                self.is_recommend = data_filter["is_recommend"]

        self.offset_limit_sql = "offset " + str((self.page_num - 1) * self.page_size) + " limit " + str(self.page_size)
