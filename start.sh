echo "Cloning Repo..."
git clone https://github.com/kratik00/EXTRACTOR-TXT
cd /EXTRACTOR-TXT
pip install -r requirements.txt
echo "Starting Bot..."
python -m Extractor
