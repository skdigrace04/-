import calendar
from datetime import datetime
import ast
import tkinter as tk
from tkinter import simpledialog, messagebox

chart = {}

def add_schedule():
    date = input_date(0)
    if not date:
        return "일정 추가가 취소되었습니다."
    while True:
        schedule = simpledialog.askstring("일정 추가", "등록할 일정을 입력하세요:")
        if not schedule:
            if messagebox.askyesno("취소", "일정 추가를 취소하시겠습니까?"):
                return "일정 추가가 취소되었습니다."
        else:
            break
    if date in chart.keys():
        chart[date].append(schedule)
    else:
        chart[date] = [schedule]

    return "일정이 추가되었습니다."

def check_schedule():
    date = input_date(1)  
    if not date:
        if messagebox.askyesno("취소", "일정 확인을 취소하시겠습니까?"):
            return "일정 확인이 취소되었습니다."
    if date not in chart.keys():
        return "해당 날짜에는 일정이 없습니다."
    else:
        schedules = print_schedule(chart[date])
        return f"{date}에 예정된 스케줄\n\n{schedules}"

def modify_schedule():
    date = input_date(2)
    if not date:
        if messagebox.askyesno("취소", "일정 수정을 취소하시겠습니까?"):
            return "일정 수정이 취소되었습니다."
    if date not in chart.keys():
        return "해당 날짜에는 일정이 없습니다."
    else:
        schedules = chart[date]
        schedule_list = print_schedule(schedules)
        while True:
            mod = simpledialog.askinteger("일정 수정", f"수정할 일정 번호를 선택하세요:\n{schedule_list}")
            if mod is None:
                return "수정이 취소되었습니다."
            if mod < 1 or mod > len(schedules):
                messagebox.showerror("오류", "유효한 번호를 선택하세요.")
            else:
                break
        new_schedule = simpledialog.askstring("일정 수정", "새로운 스케줄을 입력하세요:")
        if not new_schedule:
            if messagebox.askyesno("취소", "일정 수정을 취소하시겠습니까?"):
                return "수정이 취소되었습니다."
        schedules[mod - 1] = new_schedule
        updated_schedule = print_schedule(schedules)
        return f"일정이 수정되었습니다.\n\n수정된 일정:\n\n{updated_schedule}"

def delete_schedule():
    date = input_date(3)
    if not date:
        if messagebox.askyesno("취소", "일정 삭제를 취소하시겠습니까?"):
            return "일정 삭제가 취소되었습니다."
    if date not in chart.keys():
        return "해당 날짜에는 일정이 없습니다."
    else:
        while True:
            mod = simpledialog.askstring("일정 삭제", "1. 전체 일정 삭제\n2. 일부 일정 삭제")
            if not mod:
                if messagebox.askyesno("취소", "일정 삭제를 취소하시겠습니까?"):
                    return "삭제 작업이 취소되었습니다."
            elif mod == "1":
                chart[date] = []
                if chart[date] == []:
                    del chart[date]
                return "삭제 완료되었습니다."
            elif mod == "2":
                schedule_list = print_schedule(chart[date])
                while True:
                    try:
                        mod = simpledialog.askinteger("일정 삭제", f"삭제할 일정 번호를 선택하세요:\n{schedule_list}")
                        if mod is None:
                            if messagebox.askyesno("취소", "일정 삭제를 취소하시겠습니까?"):
                                return "삭제 작업이 취소되었습니다."
                        if mod < 1 or mod > len(chart[date]):
                            messagebox.showerror("오류", "유효한 번호를 선택하세요.")
                        else:
                            chart[date].pop(mod - 1)
                            if chart[date] == []:
                                del chart[date]
                            return "선택한 일정이 삭제되었습니다."
                    except ValueError:
                        messagebox.showerror("오류", "유효한 번호를 선택하세요.")
                        continue
            else:
                messagebox.showerror("오류", "잘못된 선택입니다.")
    
def print_schedule(d):
    return "\n".join([f"{i+1}. {s}" for i, s in enumerate(d)])

def input_date(v):
    work = ["추가", "확인", "수정", "삭제"]
    while True:
        date = simpledialog.askstring("날짜 입력", f"일정을 {work[v]}할 날짜를 입력하세요 (YYYY-MM-DD):")
        if not date:
            return None
        try:
            date_ = datetime.strptime(date, '%Y-%m-%d')
            return date_.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("오류", "형식에 맞게 입력하세요 (YYYY-MM-DD).")
            continue

def write_schedule(txt):
    with open(txt, "w") as file:
        for key in chart.keys():
            file.write(f"{key}:{chart[key]}\n")

def read_schedule(txt):
    try:
        with open(txt, "r") as file:
            read_data = file.readline()
            while read_data:
                new_date = datetime.strptime(read_data[:10], "%Y-%m-%d").strftime("%Y-%m-%d")
                new_list = ast.literal_eval(read_data[11:])
                chart[new_date] = new_list
                read_data = file.readline()
    except FileNotFoundError:
        pass

def main():
    try:
        read_schedule("schedule.txt")
    except:
        pass
    
    root = tk.Tk()
    root.title("일정 관리 프로그램")
    root.geometry("400x300")

    label = tk.Label(root, text="일정 달력 프로그램", font=("Arial", 16))
    label.pack(pady=10)

    def handle_action(choice):
        result = ""
        match choice:
            case "1":
                result = add_schedule()
            case "2":
                result = check_schedule()
            case "3":
                result = modify_schedule()
            case "4":
                result = delete_schedule()
            case "5":
                write_schedule("schedule.txt")
                root.quit()
            case _:
                result = "올바른 값을 선택하세요."
        if result:
            messagebox.showinfo("결과", result)

    buttons = [
        ("일정 추가", "1"),
        ("일정 확인", "2"),
        ("일정 수정", "3"),
        ("일정 삭제", "4"),
        ("종료", "5"),
    ]

    for text, choice in buttons:
        btn = tk.Button(root, text=text, width=20, command=lambda c=choice: handle_action(c))
        btn.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()
