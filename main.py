from scraper.auth import AuthenticationManager


def main():

    auth = AuthenticationManager()

    token = auth.get_token()

    print()

    print("=" * 60)

    print("Authorization Token")

    print("=" * 60)

    print(token)

    print("=" * 60)


if __name__ == "__main__":

    main()