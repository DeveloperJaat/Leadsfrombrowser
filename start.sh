# Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f1)
wget https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0.0/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
chmod +x chromedriver
mv chromedriver /usr/local/bin/
