"""
    搜索框

"""


class SearchBar:

    def __init__(self, request, inputs):
        self.request = request
        self.inputs = inputs

    class Object:
        def __init__(self, name, label, input_type, value=""):
            self.name = name
            self.label = label
            self.type = input_type
            self.value = value

    def filter_contains(self):
        data_dict = {}
        for input_name in self.inputs:
            search_input = self.request.GET.get(f"search_{input_name}", "")  # 有值传值，没值传空
            if search_input:
                data_dict[f"{input_name}__icontains"] = search_input  # __icontains：不分大小写搜索
        return data_dict

    def html(self):
        search_form = []
        for input_name in self.inputs:
            search_input = self.request.GET.get(f"search_{input_name}", "")  # 有值传值，没值传空
            if search_input:
                obj = self.Object(f"search_{input_name}", input_name, "text", search_input)
            else:
                obj = self.Object(f"search_{input_name}", input_name, "text")
            search_form.append(obj)
        return search_form
