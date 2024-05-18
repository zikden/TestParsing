from tasks import ParseTask


def main():
    for page in range(1, 3):
        ParseTask().apply_async(args=[str(page)])


if __name__ == "__main__":
    main()
