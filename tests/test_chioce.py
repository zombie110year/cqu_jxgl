from bs4 import BeautifulSoup


def test_parse_dict():
    from cqu_jxgl.choice import ChoiceTable
    with open("tests/工程力学.html", "rt", encoding="utf-8") as file:
        text = file.read()
    table = ChoiceTable(text)
    lists = table.to_dict()
    results = [
        {
            "teacher": "张永祥",
            "course_id": "001",
            "left": 0,
            "schdule": ["3-4,6-16周三(9-10节)", "3-4,6-17周二(1-2节)"],
            "location": ["A5208(A区)", "A5103(A区)"],
        },
        {
            "teacher": "郭开元",
            "course_id": "014",
            "left": 20,
            "schdule": ["1-4,6-15周三(5-6节)", "1-4,6-8周一(9-10节)", "10-15周五(1-2节)"],
            "location": ["D1142(D区)", "D1338(D区)", "D1344(D区)"]
        }
    ]
    for a, b in zip(lists, results):
        assert a == b
