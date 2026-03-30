name: Build APK
on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y python3-pip build-essential git python3 python3-dev ffmpeg libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libportmidi-dev libswscale-dev libavformat-dev libavcodec-dev zlib1g-dev
          sudo apt-get install -y libgstreamer1.0-gstreamer-lite1.0-dev libgstreamer-plugins-base1.0-dev

      - name: Build with Buildozer
        uses: ArtemSerebrennikov/buildozer-action@v1
        with:
          command: yes | buildozer android debug
          buildozer_version: master

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: Tufan-VPN-Final
          path: bin/*.apk

