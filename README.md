# GPT Playground

詳細は後で書く

## Discord Bot

1. Discord 側で Bot を作成しトークンをコピーする
2. 以下の Bot 権限が必須
   1. Send Messages
   2. Create Public Threads
   3. Send Messages in Threads
   4. Add Reactions
3. 下記のコマンドで Bot を稼働

```sh
touch log/discord_bot.log
python src/discord_bot.py
```

### Start Service

```
cd GPT-playground
echo OPENAI_API_KEY=xxxxxxxxxxxxxxxx >> .env
echo DISCORD_BOT_TOKEN=xxxxxxxxxxxxxxxx >> .env

# path 部分は適宜書き換える
cat <<EOF > gpt-bot.service
[Unit]
Description = GPT Bot
After=network.target

[Service]
ExecStart = /usr/bin/python /path/GPT-playground/src/discord_bot.py
WorkingDirectory = /path/GPT-playground/
Restart = always
EnvironmentFile = /path/GPT-playground/.env
User=pi
Group=pi

[Install]
WantedBy = multi-user.target
EOF


sudo ln -s gpt-bot.service /etc/systemd/system/gpt-bot.service

sudo systemctl enable gpt-bot.service
sudo reboot

# 確認
sudo systemctl list-unit-files --type=service
```
