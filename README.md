# live-video-from-RPi-to-PC-by-TCP-IP-socket
所需硬體材料:  RPi + 筆電 + python環境 + pi camera(webcam也可以)

影像是pi camera的畫面，樹梅派經由socket將圖片傳到筆電，並且在筆電上顯示圖像。

在這裡，server為樹梅派 / client為筆電

這是一個camera img transfer by TCP/IP socket from server to client的實作

藉由socket實現以"不需要額外建立網站，不需進行網頁資料抓取的"方式，來進行內網範圍的無線資料傳輸，並將影像顯示，以達成即時影像的效果。

My hackmd note about this project:

https://hackmd.io/nlcRvzZOQu-BQyZPSqh2vg?view

若樹梅派有裝motion daemon，則一開始操作前要先執行
`$ sudo /etc/init.d/motion stop`，這樣相機資源才可以被正常的取用。
