紀錄資料表敘述（與 models.py 的內容還未同步）
預設都有created_date、update_date
=========

# User（Django 內建，視情況使用某些欄位）
| 欄位         | 欄位敘述        |
|--------------|----------------|
| username     | 使用者名稱，帳號      |
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
| position     | 職稱 | str

# Department（部門）
| 欄位         | 欄位敘述        | 型態 |
|--------------|----------------| ---------------- |
| parent_department| 上層部門| FK |
| department_name | 部門名稱 |  str |


# Clock_in_out（打卡）
| 欄位         | 欄位敘述        | 型態 |
|--------------|----------------|----------------|
| employee_id  | 員工 ID  | FK |
| date | 簽到日期 | date |
| clock_in_or_out | 簽到簽退 | bool,T為簽到、F為簽退 |
| clock_time | 簽到時間 | time |
| clock_GPS | 當下GPS |  str | 

# News（公司公告）
| 欄位         | 欄位敘述        | 型態 |
|--------------|----------------| ---------------- |
| title        | 標題     | str |
| type         | 類型     | str |
| level        | 重要程度   | str |
| content      | 內容     | 編輯器 |

# Equipment（固定資產管理）
| 欄位         | 欄位敘述        | 型態 |
|--------------|----------------| ---------------- |
| barcode      | 資產條碼     | img |
| equipment_id | 資產標籤     | str |
| location     | 庫存地點     | str |
| stocktaker   | 盤點人       | FK，員工ID |
| no           | 序號         | str |
| name         | 品名         | str |

# Project（工作派任計畫）
| 欄位         | 欄位敘述        | 型態 |
|--------------|----------------| ---------------- |
| quotation_id | 報價單號     | str |
| projecet_id  | 工派單編號   | str |
| project_name | 工程名稱     | str |
| c_a          | 母案編號     | str |
| attendance   | 出勤日期     | date |
| work_employee| 工作人員     | FK，員工ID |
| lead_employee| 帶班人員     | FK，員工ID |
| vehicle      | 使用車輛     | str |
| location     | 工作地點     | str |
| project_type | 工作類型     | str |
| remark       | 備註         | str |
| support      | 支援人力     | str |
| attachment   | 工確單附件   | str |

