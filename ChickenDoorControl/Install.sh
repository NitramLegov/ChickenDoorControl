DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo 'Welcome to the Chicken door control setup'
echo 'Please note that the initial setup requires an active internet connection.'
echo 'First, we will update the apt-get database'
sudo apt-get -qq update
echo '----------------'
echo 'Installing python prerequisites for the Chicken door control Software: web.py and pyephem'
sudo pip install web.py pyephem 