FROM mrismanaziz/man-userbot:buster

RUN git clone -b Zelda-Userbot https://github.com/nmiabdfhmy/Zelda-Userbot /home/github.com/nmiabdfhmy/Zelda-Userbot/ \
    && chmod 777 /home/github.com/nmiabdfhmy/Zelda-Userbot \
    && mkdir /home/github.com/nmiabdfhmy/Zelda-Userbot/bin/

COPY ./sample_config.env ./config.env* /home/github.com/nmiabdfhmy/Zelda-Userbot/

WORKDIR /home/github.com/nmiabdfhmy/Zelda-Userbot/

CMD ["python3", "-m", "Zelda"]
