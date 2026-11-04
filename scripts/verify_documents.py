from database.database import DatabaseManager


def separator(title):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main():

    db = DatabaseManager()

    # ---------------------------------------------------------
    separator("DOCUMENT PIPELINE VERIFICATION")

    # ---------------------------------------------------------
    separator("1. DOCUMENT COUNT")

    row = db.fetchone(
        """
        SELECT COUNT(*)
        FROM documents
        """
    )

    total_documents = row[0]

    print(f"Total Documents : {total_documents}")
    print("Expected        : Around 135")

    if total_documents > 0:
        print("Status          : PASS")
    else:
        print("Status          : FAIL")

    # ---------------------------------------------------------
    separator("2. DOCUMENT TYPE DISTRIBUTION")

    rows = db.fetchall(
        """
        SELECT
            document_type,
            COUNT(*)
        FROM documents
        GROUP BY document_type
        ORDER BY COUNT(*) DESC
        """
    )

    print(f"{'Document Type':40} {'Count'}")
    print("-" * 55)

    for row in rows:
        print(f"{row[0]:40} {row[1]}")

    # ---------------------------------------------------------
    separator("3. ATTACHMENT DOWNLOAD STATUS")

    row = db.fetchone(
        """
        SELECT COUNT(*)
        FROM attachments
        WHERE downloaded = 1
        """
    )

    downloaded = row[0]

    row = db.fetchone(
        """
        SELECT COUNT(*)
        FROM attachments
        """
    )

    total_attachments = row[0]

    print(f"Downloaded : {downloaded}")
    print(f"Total      : {total_attachments}")

    # ---------------------------------------------------------
    separator("4. DOCUMENTS WITH EMPTY TEXT")

    row = db.fetchone(
        """
        SELECT COUNT(*)
        FROM documents
        WHERE extracted_text IS NULL
           OR LENGTH(TRIM(extracted_text)) = 0
        """
    )

    print(f"Documents with empty text : {row[0]}")

    # ---------------------------------------------------------
    separator("5. SAMPLE DOCUMENTS")

    rows = db.fetchall(
        """
        SELECT
            document_type,
            filename,
            page_count,
            word_count
        FROM documents
        LIMIT 10
        """
    )

    for row in rows:

        print(f"""
Type       : {row[0]}
Filename   : {row[1]}
Pages      : {row[2]}
Words      : {row[3]}
------------------------------------------------------------
""")

    # ---------------------------------------------------------
    separator("6. PDF DOWNLOAD PATH CHECK")

    rows = db.fetchall(
        """
        SELECT
            filename,
            local_path
        FROM attachments
        LIMIT 5
        """
    )

    for row in rows:

        print(f"{row[0]}")
        print(f"  {row[1]}")
        print()

    db.close()

    separator("VERIFICATION COMPLETE")


if __name__ == "__main__":
    main()