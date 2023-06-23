前の開発者のアップグレード版自分用にカスタマイズしています。

サポート環境: python v.3.10.11 / discord.py v.2.3.0 / mcstatus v10.0.3

# 使い方

自分のIPの所にIPv4とTOKEN、F_nameを埋めてください。

os.chdirの()中サーバーフォルダーの場所をお願いします。

mcstatusAPIを導入しているので、mcstastusも入れてください

そのあとWindowsならバッチファイルを作成して、完成

```
python3  -m  pip  install  mcstatus
python serverstarterbot.py
```

## コマンド

```
/r.start サーバーを起動
/r.stop サーバーをを停止
/r.kill サーバー緊急停止用
/r.status サーバー起動してるか?
/r.player サーバー内のプレイヤー数
```
