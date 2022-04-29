# SmartHome-Microbit
Sử dụng microbit làm nhà thông minh có kết nối IOT 

SmartHome trong dự án lần này có các chức năng:
+ Sử dụng nút nhấn (như 1 công tác) để điều khiển đèn bật/tắt.
+ Sử dụng cảm biến ánh sáng để nhận biết khi trời tối thì sẽ bật đèn và trời sáng thì sẽ tắt đèn.
+ Sử dụng cảm biến DHT11 để đo nhiệt độ và độ ẩm trong nhà và kết quả sẽ được hiển thị ra LCD.
+ Sử dụng cảm biến đo nồng độ khí Gas kết quả sẽ được hiển thị thông qua Led Traffic:
    + Khi mức độ khí Gas ở mức cho phép thì sẽ hiển thị Led xanh.
    + Khi mức độ khí Gas ở mức nguy hiểm thì sẽ hiển thị Led vàng.
    + Khi mức độ khí Gas ở mức rất nguy hiểm thì sẽ hiển thị Led đỏ và 1 loa buzzer sẽ được sử dụng trong TH này để phát ra tiếng động.
+ Sử dụng động cơ quạt tản nhiệt.
( Do Microbit có nhiều hạn chế và dự án lần này không được sử dụng nhiều microbit nên em chỉ dừng lại hiện thực 1 số chức năng cơ bản trên. Nếu có kinh phí thêm thì em sẽ tiếp tục xây dựng dự án có nhiều tính năng hơn nữa.)

Lập trình Gateway để là cầu nối giữa các thiết bị phần cứng và sever từ đó có thể giao tiếp thông qua web/app và phương thức giao tiếp được sử dụng trong dự án này là MQTT, sever Adafruit.

Xây dựng 1 trợ lý ảo cơ bản để điều khiển các thiết bị trong nhà bằng giọng nói. Trợ lý ảo này mới chỉ hiện thực ở mức local sử dụng mic của chiếc laptop. Cơ chế xây dựng là sẽ chuyển âm thanh thành văn bản text dựa vào API google và từ văn bản text sẽ so sánh để đưa ra hành động. Trợ lý ảo có các chức năng như sau:
+ Điều khiển đèn bật/tắt.
+ Điều khiển quạt bật ( theo 3 chế độ to, trung bình, nhỏ) / tắt quạt.
+ Đọc được nhiệt độ/độ ẩm/khí gas trong ngôi nhà.
+ Và có các tác vụ giao tiếp trò chuyện như 2 con người.
