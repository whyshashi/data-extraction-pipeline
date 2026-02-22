from main import segmentTable,consolidatedTable
import os

def app():
    try:
        # Run the main segment table pipeline
        segmentTable()

        # Run the main consolidated table pipeline
        consolidatedTable()
        
    except Exception as e:
        print(f"Error: {e} occurred while processing {input_file}")
        return


if __name__ == "__main__":
    app()