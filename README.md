# VNIT Hostel Grievance Management — Flask + MySQL (MVP)

## Quickstart
1) Create MySQL DB:
```sql
CREATE DATABASE vnit_grievance CHARACTER SET utf8mb4;
```
2) Set environment:
```bash
export DATABASE_URL="mysql+mysqldb://root:password@127.0.0.1:3306/vnit_grievance"
export SECRET_KEY="change-me"
```
3) Install & run:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
4) Visit http://localhost:5000 and create users for Admin, Worker, Resident.

## Notes
- File uploads save to `uploads/` by default.
- Emergency detection is keyword-based in `utils.detect_emergency`.
- Swap to PyMySQL by changing the driver and dependency if needed.
