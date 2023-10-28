from misc import pp
from args import Args


def main(args: Args):
    pp(args)


if __name__ == "__main__":
    main(Args.parse())
