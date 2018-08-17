Yêu cầu cơ sở :

Để có được một hình ảnh cụ thể cho người dùng, trước tiên phải băm email của họ.

- URL yêu cầu hình ảnh cơ bản nhất trông giống như sau:
```http://127.0.0.1:5000/avatar/HASH```

- Trong đó HASH được thay thế bằng hàm băm được tính cho địa chỉ email cụ thể được yêu cầu. Ví dụ: 
```http://127.0.0.1:5000/avatar/13a0b14f211ea7e5cd9c8310744a7bc6```

Kích thước :

- Có thể yêu cầu kích thước hình ảnh cụ thể bằng cách sử dụng tham số  ```?s= tham số``` và truyền một số nguyên pixel (vì hình ảnh là hình vuông):
```http://127.0.0.1:5000/avatar/13a0b14f211ea7e5cd9c8310744a7bc6?s=100```

- Có thể sử dụng hình ảnh ở bất kỳ đâu, tuy nhiên lưu ý rằng nhiều người dùng có hình ảnh có độ phân giải thấp hơn, do đó yêu cầu kích thước quá lớn hoặc quá nhỏ có thể dẫn đến hình ảnh chất lượng thấp.

Hình ảnh mặc định :

- Nếu không có hình ảnh nào được liên kết với băm email được yêu cầu, sẽ trả về một hình ảnh mặc định.

Khai báo báo env mới :

```
virtualenv .avatar_env
source .avatar/bin/activate
```

Cài các gói pip :

```
pip install -r requirements.txt
```
Khai báo File cấu hình :

```
cp app.yaml.example app.yaml
```

Sửa các giá trị trong file `app.yaml` theo đúng cấu hình cài đặt.

Thiết lập biến môi trường :

```
export FLASK_APP=run.py
```
Taọ cơ sở dữ liệu : 

```
create database avatar;
```
Tạo kho lưu trữ di chuyển :

```
flask db init
flask db migrate
flask db upgrade
```

Test app :

- Tạo cơ sở dữ liệu phục vụ test : 
```
create database avatar_test;
```

- Test :
```
python tests.py
```

Run app ở chế độ `Development`:
```
python run.py
```

