import time

from watchers.sgx_watcher import SGXWatcher


def main():

    watcher = SGXWatcher()
    print("=" * 70)
    print("SGX WATCHER SERVICE STARTED")
    print("=" * 70)

    try:

        while True:
            watcher.run_once()
            print("\nSleeping for 60 seconds...\n")
            time.sleep(60)

    except KeyboardInterrupt:
        print("\nStopping service...\n")
        watcher.pipeline.notifier.close()


if __name__ == "__main__":

    main()