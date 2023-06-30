紀錄資料表敘述（與 models.py 的內容還未同步）
=========

# Employee（員工）
| 欄位         | 欄位敘述        |
|--------------|----------------|
| user         | 繼承自 User     |
| employee_id | 員工 ID |
| department   | 部門 |
| position     | 職位 |
| created_date | 建立日期 |
| update_date  | 更新日期 |

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

# Clock_in_out（打卡）
| 欄位         | 欄位敘述        |
|--------------|----------------|
| employee_id  | 員工 ID（FK）   |
| clock_in_time| 簽到時間 |
| clock_in_location| 簽到地點 |
| clock_out_time| 簽退時間 |
| clock_out_location| 簽退地點 |
| created_date | 建立日期 |
| update_date  | 更新日期 |
