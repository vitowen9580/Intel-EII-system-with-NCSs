from argparse import ArgumentParser, SUPPRESS


class argument:
    # def __init__(self):
    #     pass

    def build_argparser(self):
        parser = ArgumentParser(add_help=False)
        args = parser.add_argument_group('Options')
        args.add_argument("-x", "--xml_path", help="model xml file path", required=True,  type=str)
        args.add_argument("-b", "--bin_path", help="model bin file path", required=True,  type=str)
        args.add_argument("-d", "--TestData", help="Test dataset path", required=True,  type=str)
        args.add_argument("-m", "--MYRIAD_name", help="MYRIAD name", required=True,  type=str)

        return parser
