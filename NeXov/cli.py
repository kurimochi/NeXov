import argparse
import sys
import os
from NeXov.core import MarkovModel
from NeXov.tokenizer import mecab_split, char_split


def run_tokenize(args):
    with open(args.input, 'r', encoding='utf-8') as f:
        raw = f.read()

    if args.method == 'mecab':
        result = mecab_split(raw)
    else:
        result = char_split(raw)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"[+] Wrote tokenized data to {args.output}")
    else:
        print(result)


def run_generate(args):
    model = MarkovModel()

    _, ext = os.path.splitext(args.input)
    ext = ext.lower()

    if ext in [".pkl", ".pickle"]:
        model.load_pickle(args.input)
    elif ext == ".json":
        model.load_json(args.input)
    else:
        with open(args.input, 'r', encoding='utf-8') as f:
            tokens = [w for l in f for w in l.strip().split()]
        model.build(tokens)

    if args.visualize:
        model.visualize(args.visualize, font='Noto Sans JP')
        return

    if args.export:
        _, export_ext = os.path.splitext(args.export)
        export_ext = export_ext.lower()

        if export_ext in [".pkl", ".pickle"]:
            model.save_pickle(args.export)
            print(f"[+] The model was saved to {args.export}")
        elif export_ext == ".json":
            model.save_json(args.export)
            print(f"[+] The model was exported to {args.export}")
        else:
            print("[-] Unsupported file format: Please specify a pickle file or a json file.", file=sys.stderr)
            sys.exit(1)
        return

    if not args.start:
        print("[-] Specify the start token (--start).", file=sys.stderr)
        sys.exit(1)

    model.result.append(args.start)
    current = args.start
    while len(model.result) < args.length:
        current = model.generate(current)
    print(''.join(model.result))


def run_visualize(args):
    model = MarkovModel()

    _, ext = os.path.splitext(args.input)
    ext = ext.lower()

    if ext in [".pkl", ".pickle"]:
        model.load_pickle(args.input)
    elif ext == ".json":
        model.load_json(args.input)
    else:
        print("[-] Unsupported file format: Please specify a pickle file or a json file.", file=sys.stderr)
        sys.exit(1)

    model.visualize(args.output, args.font)


def main():
    parser = argparse.ArgumentParser(prog="nexov", description="NeXov Enables eXtensible Observation of Vertices")
    subparsers = parser.add_subparsers(dest="command")

    # Sub command: tokenize
    tokenize_parser = subparsers.add_parser("tokenize", help="テキストをトークンに分割")
    tokenize_parser.add_argument('-i', '--input', required=True, help='入力ファイル')
    tokenize_parser.add_argument('-o', '--output', help='出力ファイル')
    tokenize_parser.add_argument('--method', choices=['mecab', 'char'], default='mecab', help='分割方法')
    tokenize_parser.set_defaults(func=run_tokenize)

    # Sub command: generate
    generate_parser = subparsers.add_parser("generate", help="モデルまたはテキストを生成")
    generate_parser.add_argument('-i', '--input', required=True, help='モデルまたはトークン済みデータファイル')
    generate_parser.add_argument('-s', '--start', help='開始トークン')
    generate_parser.add_argument('-l', '--length', type=int, default=1000, help='生成するトークン数')
    generate_parser.add_argument('-e', '--export', help='生成後のモデルをファイルにエクスポート')
    generate_parser.add_argument('-v', '--visualize', help='生成と同時に可視化を実行(拡張子を除く出力ファイル名を指定)')
    generate_parser.set_defaults(func=run_generate)

    # Sub command: visualize
    visualize_parser = subparsers.add_parser("visualize", help="モデルを画像として可視化")
    visualize_parser.add_argument('-i', '--input', required=True, help='モデルファイル')
    visualize_parser.add_argument('-o', '--output', required=True, help='出力ファイル(拡張子を除くファイル名を指定)')
    visualize_parser.add_argument('--font', default='Noto Sans JP', help='使用するフォント')
    visualize_parser.set_defaults(func=run_visualize)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == '__main__':
    main()
