class UtilLogic:
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
        pass
