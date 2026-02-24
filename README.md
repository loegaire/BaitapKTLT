# BaitapKTLT – Test Grade Calculator

## Yêu cầu

- Python 3
- Thư viện: `numpy`, `pandas`

## Cấu trúc thư mục

- `Data Files/`: chứa dữ liệu đầu vào `class1.txt` ... `class8.txt`
- `Data Files/Expected Output/`: chứa output mẫu để đối chiếu
- Chương trình: `Data Files/To_Thinh_grade_the_exams.py`

## Cài đặt

Từ thư mục gốc của project:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Chạy chương trình

### Cách 1 (khuyến nghị): chạy trong thư mục `Data Files/`

```bash
cd "Data Files"
python To_Thinh_grade_the_exams.py
```

Khi được hỏi, nhập tên lớp (ví dụ `class1` hoặc `class1.txt`).

### Cách 2: chạy từ thư mục gốc

```bash
python "Data Files/To_Thinh_grade_the_exams.py"
```

## Kết quả

- Chương trình sẽ in báo cáo phân tích dữ liệu (dòng hợp lệ/không hợp lệ) và thống kê điểm.
- Đồng thời tạo file kết quả theo tên lớp, ví dụ:
	- Input: `Data Files/class1.txt`
	- Output: `Data Files/class1_grades.txt`

Bạn có thể đối chiếu với các file mẫu tương ứng trong `Data Files/Expected Output/`.
