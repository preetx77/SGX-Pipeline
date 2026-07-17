from services.historical_processing_service import HistoricalProcessingService


def main():

    processor = HistoricalProcessingService()

    processor.process_company("HQU")


if __name__ == "__main__":
    main()