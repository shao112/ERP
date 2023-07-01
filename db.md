紀錄資料表敘述（與 models.py 的內容還未同步）
預設都有created_date、update_date
=========

# User（Django 內建，視情況使用某些欄位）
| 欄位         | 欄位敘述        |
|--------------|----------------|
| username     | 使用者名稱      |
| first_name   | 名   |
| last_name    | 姓   |
| email        | 電子信箱 |
| password     | 密碼 |
| groups       | 群組 |
| user_permissions  | 派權限 |
| is_staff     | 權限較小 |
| is_active    | 是否被停用 |
| is_superuser | 權限較大 |
| last_login   | 上次登入 |
| date_joined  | 創建時間 |


# Employee（員工）
| 欄位         | 欄位敘述        | 型態 |
|--------------|----------------| ---------------- |
| user         | 繼承自 User     | FK
| employee_id | 員工 ID | str
| department   | 部門id | FK
| position     | 職位 | str

# Department（部門）
| 欄位         | 欄位敘述        | 型態 |
|--------------|----------------| ---------------- |
| upper_dept |上層部門(採取樹狀結構) | FK, default NULL |
| name   | 部門名稱 |  str |

# Clock_in_out（打卡）
| 欄位         | 欄位敘述        | 型態 |
|--------------|----------------|----------------|
| employee_id  | 員工 ID  | FK |
| date | 簽到日期 | date |
| clock_in_or_out | 簽到簽退 | bool,T為簽到、F為簽退 |
| clock_time | 簽到時間 | time |
| clock_GPS | 當下GPS |  str | 

# Information（最新消息）
| 欄位         | 欄位敘述        | 型態 |
|--------------|----------------| ---------------- |
| title        | 標題     | str
| topic        | 主題     | str
| content      | 內容     | 編輯器
