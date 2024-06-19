def test_camel_case_lower_first():
    from cookit import camel_case

    assert camel_case("hello_world") == "helloWorld"


def test_camel_case_upper_first():
    from cookit import camel_case

    assert camel_case("hello_world", upper_first=True) == "HelloWorld"


def test_camel_case_single_word():
    from cookit import camel_case

    assert camel_case("hello") == "hello"


def test_camel_case_empty_string():
    from cookit import camel_case

    assert camel_case("") == ""


def test_full_to_half():
    from cookit import full_to_half

    assert full_to_half("Ｈｅｌｌｏ　Ｗｏｒｌｄ！") == "Hello World!"
    assert full_to_half("１２３４５６７８９０") == "1234567890"
    assert full_to_half("ＡＢＣＤＥＦＧ") == "ABCDEFG"
    assert full_to_half("！＠＃＄％＾＆＊") == "!@#$%^&*"
    assert full_to_half("［］｛｝（）＜＞＝＋－／＊＆％＃＠") == "[]{}()<>=+-/*&%#@"
    assert (
        full_to_half("ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ")
        == "abcdefghijklmnopqrstuvwxyz"
    )
    assert (
        full_to_half("ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ")
        == "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    assert (
        full_to_half(
            "１２３４５６７８９０！＠＃＄％＾＆＊（）＿＋｛｝［］：＂；＇＜＞，．／？",
        )
        == "1234567890!@#$%^&*()_+{}[]:\";'<>,./?"
    )


def test_escape_single_quotes():
    from cookit import escape_single_quotes

    assert escape_single_quotes("Hello, 'World'!") == "Hello, \\'World\\'!"

    assert escape_single_quotes("Hello, World!") == "Hello, World!"
    assert escape_single_quotes('Hello, "World"!') == 'Hello, "World"!'
    assert escape_single_quotes("Hello, `World`!") == "Hello, `World`!"


def test_escape_double_quotes():
    from cookit import escape_double_quotes

    assert escape_double_quotes('Hello, "World"!') == 'Hello, \\"World\\"!'

    assert escape_double_quotes("Hello, World!") == "Hello, World!"
    assert escape_double_quotes("Hello, 'World'!") == "Hello, 'World'!"
    assert escape_double_quotes("Hello, `World`!") == "Hello, `World`!"


def test_escape_backticks():
    from cookit import escape_backticks

    assert escape_backticks("Hello, `World`!") == "Hello, \\`World\\`!"

    assert escape_backticks("Hello, World!") == "Hello, World!"
    assert escape_backticks("Hello, 'World'!") == "Hello, 'World'!"
    assert escape_backticks('Hello, "World"!') == 'Hello, "World"!'
