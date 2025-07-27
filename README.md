PDF Heading Extractor (Adobe Hackathon)

This script extracts the title and H1–H3 level headings from PDF files and outputs structured JSON with page numbers.

📁 Folder Structure

├── input/        # Place your PDFs here

├── output/       # Output JSON files will be saved here

├── extract.py    # Main extraction script

├── Dockerfile

├── requirements.txt

├── .gitignore

└── README.md


🚀 How to Use

Place all input PDF files in the input/ folder.

Run locally or inside Docker.

Output JSON files will appear in the output/ folder.

🐳 Run with Docker

Build the Docker image:

docker build -t heading-extractor .

Run the container:

docker run -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output heading-extractor

📌 On Windows, replace $(pwd) with full path. 

Example: docker run -v D:/Adobe/Challenge_1a/input:/app/input -v D:/Adobe/Challenge_1a/output:/app/output heading-extractor

🛠 Requirements

Python 3.9+

PyMuPDF

Docker (optional for containerization)

To install locally:

pip install -r requirements.txt

👨‍💻 Contributors

This project was developed as part of Adobe’s “Connecting the Dots” Hackathon.

Team Name: PageBreakers

Members:

Arpita Rawat

Devanshi Jain

Kavya Gupta

✅ Credits

Thanks to the organizing team at Adobe for this challenge.
