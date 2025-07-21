from tkinter import *
import random

pay=0
elapsed_time=0
book_pay = 0

# 우측 주차구역 버튼들을 저장할 리스트. 각 층별로 따로 관리하도록 변경
# 층별 버튼 리스트를 딕셔너리로 관리
right_parking_buttons_by_floor = {
    '1f': [],
    '2f': [],
    '3f': []
}

# 현재 예약 상태를 추적하는 변수
current_reservation = None  # None이면 예약 없음, 층 정보가 있으면 해당 층에 예약됨

def des():
    root.destroy()    
def firstview():
    frame1.lift()
def secondview():
    frame2_1f.lift() # Default to 1st floor when "현 주차장 정보" is clicked
def thirdview():
    frame3.lift()
def secondfh():
    frame2_1f.lift()
def secondsh():
    frame2_2f.lift()
def secondth():
    frame2_3f.lift()

def get():
    nameg = name_entry.get()
    telg = tel_entry.get()
    car_numg = car_num_entry.get()
    car_mdlg = car_mdl_entry.get()
    
    #정보 표시 업데이트
    name_label.config(text=f'이름: {nameg}')
    tel_label.config(text=f'전화번호: {telg}')
    car_num_label.config(text=f'차량번호: {car_numg}')
    car_mdl_label.config(text=f'차량모델: {car_mdlg}')
    
def reset():
    name_label.config(text=f'이름: -')
    tel_label.config(text=f'전화번호: -')
    car_num_label.config(text=f'차량번호: -')
    car_mdl_label.config(text=f'차량모델: -')
    name_entry.delete(0, END)
    tel_entry.delete(0, END)
    car_num_entry.delete(0, END)
    car_mdl_entry.delete(0, END)

def update_reservation_status():
    """예약 상태를 업데이트하는 함수"""
    if current_reservation:
        reservation_status.config(text=f"예약됨 ({current_reservation}층)", fg='#e74c3c')
    else:
        reservation_status.config(text="예약 대기 중", fg='#7f8c8d')

def make_reservation_random():
    """메인화면용 예약 기능 - 3개층 중 랜덤 선택"""
    global current_reservation
    
    # 이미 예약이 있는 경우 예약 불가
    if current_reservation:
        return
    
    # 모든 층의 빈 자리를 수집
    all_available_spots = []
    floors = ['1f', '2f', '3f']
    
    for floor_key in floors:
        available_spots = [btn for btn in right_parking_buttons_by_floor[floor_key] if btn['bg'] == 'lightgreen']
        for spot in available_spots:
            all_available_spots.append((spot, floor_key))
    
    if all_available_spots:
        # 랜덤으로 층과 자리 선택
        selected_spot, selected_floor = random.choice(all_available_spots)
        selected_spot.config(text='예약', bg='orange')
        current_reservation = selected_floor
        update_reservation_status()

def make_reservation(floor_key):
    """특정 층 예약 기능"""
    global current_reservation
    
    # 이미 예약이 있는 경우 예약 불가
    if current_reservation:
        return
    
    current_right_parking_buttons = right_parking_buttons_by_floor[floor_key]
    # 빈 자리(lightgreen) 중에서 랜덤 선택
    available_spots = [btn for btn in current_right_parking_buttons if btn['bg'] == 'lightgreen']
    
    if available_spots:
        # 랜덤으로 빈 자리 선택하여 예약 상태로 변경
        selected_spot = random.choice(available_spots)
        selected_spot.config(text='예약', bg='orange')
        current_reservation = floor_key
        update_reservation_status()

def cancel_reservation_all():
    """전체 예약 취소 기능 - 모든 층에서 예약된 자리를 찾아서 취소"""
    global current_reservation
    
    if not current_reservation:
        return
    
    # 모든 층에서 예약된 자리 찾기
    for floor_key in ['1f', '2f', '3f']:
        current_right_parking_buttons = right_parking_buttons_by_floor[floor_key]
        reserved_spots = [btn for btn in current_right_parking_buttons if btn['bg'] == 'orange']
        
        for spot in reserved_spots:
            spot.config(text='', bg='lightgreen')
    
    current_reservation = None
    update_reservation_status()

def cancel_reservation(floor_key):
    """특정 층 예약 취소 기능"""
    global current_reservation
    
    current_right_parking_buttons = right_parking_buttons_by_floor[floor_key]
    reserved_spots = [btn for btn in current_right_parking_buttons if btn['bg'] == 'orange']
    
    if reserved_spots:
        # 예약된 자리 중 하나를 빈 자리로 변경
        selected_spot = reserved_spots[0]  # 첫 번째 예약된 자리 취소
        selected_spot.config(text='', bg='lightgreen') # 빈 자리로 변경
        current_reservation = None
        update_reservation_status()

def toggle_parking_spot(button, spot_id):
    """주차자리 상태를 토글하는 함수"""
    global current_reservation
    
    if button['bg'] == 'lightgreen':  # 빈 자리 -> 주차됨
        button.config(bg='lightcoral', text='주차')
    elif button['bg'] == 'lightcoral':  # 주차됨 -> 빈 자리
        button.config(bg='lightgreen', text='')
    elif button['bg'] == 'orange':  # 예약됨 -> 주차됨
        button.config(bg='lightcoral', text='주차')
        current_reservation = None  # 예약 상태 해제
        update_reservation_status()

def create_parking_layout(frame, floor_key):
    """주차자리 레이아웃을 생성하는 함수"""
    # 통합 주차구역 - 화면 전체 활용
    parking_frame = Frame(frame, bg='white', relief='solid', bd=1)
    parking_frame.place(x=10, y=100, width=580, height=370) # Adjusted y and height to accommodate header

    Label(parking_frame, text="주차구역", font=('고딕', 16), bg='white').pack(pady=5)
    
    grid_frame = Frame(parking_frame, bg='white')
    grid_frame.pack(pady=5, expand=True)
    
    # Clear previous buttons for this floor
    right_parking_buttons_by_floor[floor_key] = []

    # 좌측 7x8 주차구역 + 공백 + 우측 3x8 주차구역 (총 10열)
    for row in range(8):
        for col in range(10):
            if col == 6:  # 7번째 열은 공백으로 건너뛰기
                continue
            
            # 좌측 영역 (0-6열)
            if col < 6:
                spot_id = f"L{row+1:02d}{col+1:02d}"
            # 우측 영역 (8-9열을 1-3열로 매핑)
            else:
                spot_id = f"R{row+1:02d}{col-7:02d}"
            
            btn = Button(grid_frame, text='', font=('고딕', 8), 
                        bg='lightgreen', width=3, height=3, relief='solid', bd=1)
            btn.config(command=lambda b=btn, s=spot_id: toggle_parking_spot(b, s))
            btn.grid(row=row, column=col, padx=1, pady=1)
            
            # 우측 주차구역 버튼들을 리스트에 저장
            if col >= 7:  # 우측 영역
                right_parking_buttons_by_floor[floor_key].append(btn)
    
    # 공백 열 설정 (7번째 열에 여백 추가)
    grid_frame.columnconfigure(6, minsize=25)  # 25px 간격

root = Tk()
root.title("화면 전환~~")
root.geometry("600x700")
root.resizable(False,False)

# 프레임
frame3 = Frame(root, bg='#f5f6fa')

# Updated frame2_Xf backgrounds and removed relief/border
frame2_1f = Frame(root, bg='#f5f6fa')
frame2_2f = Frame(root, bg='#f5f6fa')
frame2_3f = Frame(root, bg='#f5f6fa')

frame1 = Frame(root, relief='solid', border=2,bg='white')

but_frame = Frame(root, relief='solid', border=2)

# 프레임 배치
frame3.place(x=0, y=0, width=600, height=550)
frame2_1f.place(x=0, y=0, width=600, height=550)
frame2_2f.place(x=0,y=0,width=600,height=550)
frame2_3f.place(x=0,y=0,width=600,height=550)
frame1.place(x=0, y=0, width=600, height=550,)
but_frame.place(x=0, y=550, width=600, height=150)


# --- Updated frame3 design ---
# Header Section
header_frame_3 = Frame(frame3, bg='#2c3e50', height=70)
header_frame_3.pack(fill='x', pady=(0, 20))
Label(header_frame_3, text="사용자 정보", font=('맑은 고딕', 24, 'bold'), 
      fg='white', bg='#2c3e50').pack(pady=15)

# Information Input Panel
input_panel = Frame(frame3, bg='white', relief='solid', bd=1)
input_panel.pack(fill='x', padx=30, pady=(0, 20))

input_header = Frame(input_panel, bg='#3498db', height=40)
input_header.pack(fill='x')
Label(input_header, text="정보 입력", font=('맑은 고딕', 14, 'bold'), 
      bg='#3498db', fg='white').pack(pady=8)

# Input fields
input_fields_frame = Frame(input_panel, bg='white')
input_fields_frame.pack(pady=15, padx=20, fill='x')

Label(input_fields_frame, text='이름:', font=('맑은 고딕', 12), bg='white').grid(row=0, column=0, sticky='w', pady=5, padx=5)
name_entry = Entry(input_fields_frame, width=30, font=('맑은 고딕', 12))
name_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=5)

Label(input_fields_frame, text='전화번호:', font=('맑은 고딕', 12), bg='white').grid(row=1, column=0, sticky='w', pady=5, padx=5)
tel_entry = Entry(input_fields_frame, width=30, font=('맑은 고딕', 12))
tel_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=5)

Label(input_fields_frame, text='차량번호:', font=('맑은 고딕', 12), bg='white').grid(row=2, column=0, sticky='w', pady=5, padx=5)
car_num_entry = Entry(input_fields_frame, width=30, font=('맑은 고딕', 12))
car_num_entry.grid(row=2, column=1, sticky='ew', pady=5, padx=5)

Label(input_fields_frame, text='차량모델:', font=('맑은 고딕', 12), bg='white').grid(row=3, column=0, sticky='w', pady=5, padx=5)
car_mdl_entry = Entry(input_fields_frame, width=30, font=('맑은 고딕', 12))
car_mdl_entry.grid(row=3, column=1, sticky='ew', pady=5, padx=5)

input_fields_frame.grid_columnconfigure(1, weight=1)

# Buttons for input
button_control_frame = Frame(input_panel, bg='white')
button_control_frame.pack(pady=(0, 15))

save_button = Button(button_control_frame, text='정보 저장', command=get,
                     font=('맑은 고딕', 11),
                     width=12, relief='flat')
save_button.pack(side='left', padx=5)

reset_button = Button(button_control_frame, text='정보 초기화', command=reset,
                      font=('맑은 고딕', 11),
                      width=12, relief='flat')
reset_button.pack(side='left', padx=5)

# Information Display Panel
display_panel = Frame(frame3, bg='white', relief='solid', bd=1)
display_panel.pack(fill='x', padx=30, pady=(0, 20))

display_header = Frame(display_panel, bg='#9b59b6', height=40)
display_header.pack(fill='x')
Label(display_header, text="등록된 사용자 정보", font=('맑은 고딕', 14, 'bold'), 
      bg='#9b59b6', fg='white').pack(pady=8)

# Display labels
display_info_frame = Frame(display_panel, bg='white')
display_info_frame.pack(pady=15, padx=20, fill='x')

name_label = Label(display_info_frame, text='이름: -', font=('맑은 고딕', 12), bg='white', anchor='w')
name_label.pack(fill='x', pady=2)
tel_label = Label(display_info_frame, text='전화번호: -', font=('맑은 고딕', 12), bg='white', anchor='w')
tel_label.pack(fill='x', pady=2)
car_num_label = Label(display_info_frame, text='차량번호: -', font=('맑은 고딕', 12), bg='white', anchor='w')
car_num_label.pack(fill='x', pady=2)
car_mdl_label = Label(display_info_frame, text='차량모델: -', font=('맑은 고딕', 12), bg='white', anchor='w')
car_mdl_label.pack(fill='x', pady=2)
# --- End of Updated frame3 design ---


# --- Updated frame2_Xf design ---

# 1층 주차장
# Header Section for frame2_1f
header_frame_2_1f = Frame(frame2_1f, bg='#2c3e50', height=70)
header_frame_2_1f.pack(fill='x', pady=(0, 20))
Label(header_frame_2_1f, text="주차장 현황 - 1층", font=('맑은 고딕', 24, 'bold'),
      fg='white', bg='#2c3e50').pack(pady=15)
create_parking_layout(frame2_1f, '1f') # Pass floor_key

# 2층 주차장
# Header Section for frame2_2f
header_frame_2_2f = Frame(frame2_2f, bg='#2c3e50', height=70)
header_frame_2_2f.pack(fill='x', pady=(0, 20))
Label(header_frame_2_2f, text="주차장 현황 - 2층", font=('맑은 고딕', 24, 'bold'),
      fg='white', bg='#2c3e50').pack(pady=15)
create_parking_layout(frame2_2f, '2f') # Pass floor_key

# 3층 주차장
# Header Section for frame2_3f
header_frame_2_3f = Frame(frame2_3f, bg='#2c3e50', height=70)
header_frame_2_3f.pack(fill='x', pady=(0, 20))
Label(header_frame_2_3f, text="주차장 현황 - 3층", font=('맑은 고딕', 24, 'bold'),
      fg='white', bg='#2c3e50').pack(pady=15)
create_parking_layout(frame2_3f, '3f') # Pass floor_key

# Floor Navigation Buttons for frame2_1f
floor_nav_frame_1f = Frame(frame2_1f, bg='#f5f6fa')
floor_nav_frame_1f.place(x=0, y=490, relwidth=1, height=60) # Position at the bottom

ff_button_1f = Button(floor_nav_frame_1f, text='1층', font=('맑은 고딕', 12, 'bold'), command=secondfh, width=8, height=2)
ff_button_1f.pack(side='left', padx=20, pady=5)
sf_button_1f = Button(floor_nav_frame_1f, text='2층', font=('맑은 고딕', 12, 'bold'), command=secondsh, width=8, height=2) # Gray for inactive
sf_button_1f.pack(side='left', padx=20, pady=5)
th_button_1f = Button(floor_nav_frame_1f, text='3층', font=('맑은 고딕', 12, 'bold'), command=secondth, width=8, height=2) # Gray for inactive
th_button_1f.pack(side='left', padx=20, pady=5)

# Add Reservation and Cancel buttons to frame2_1f
reserve_btn_1f = Button(floor_nav_frame_1f, text="예약", font=('맑은 고딕', 12),
                        command=lambda: make_reservation('1f'), width=4, height=2)
reserve_btn_1f.pack(side='left', padx=15, pady=5)

cancel_btn_1f = Button(floor_nav_frame_1f, text="취소", font=('맑은 고딕', 12),
                       command=lambda: cancel_reservation('1f'), width=4, height=2)
cancel_btn_1f.pack(side='left', padx=5, pady=5)


# Floor Navigation Buttons for frame2_2f
floor_nav_frame_2f = Frame(frame2_2f, bg='#f5f6fa')
floor_nav_frame_2f.place(x=0, y=490, relwidth=1, height=60)

ff_button_2f = Button(floor_nav_frame_2f, text='1층', font=('맑은 고딕', 12, 'bold'), command=secondfh, width=8, height=2)
ff_button_2f.pack(side='left', padx=20, pady=5)
sf_button_2f = Button(floor_nav_frame_2f, text='2층', font=('맑은 고딕', 12, 'bold'), command=secondsh, width=8, height=2) # Blue for active
sf_button_2f.pack(side='left', padx=20, pady=5)
th_button_2f = Button(floor_nav_frame_2f, text='3층', font=('맑은 고딕', 12, 'bold'), command=secondth, width=8, height=2)
th_button_2f.pack(side='left', padx=20, pady=5)

# Add Reservation and Cancel buttons to frame2_2f
reserve_btn_2f = Button(floor_nav_frame_2f, text="예약", font=('맑은 고딕', 12),
                        command=lambda: make_reservation('2f'), width=4, height=2)
reserve_btn_2f.pack(side='left', padx=15, pady=5)

cancel_btn_2f = Button(floor_nav_frame_2f, text="취소", font=('맑은 고딕', 12),
                       command=lambda: cancel_reservation('2f'), width=4, height=2)
cancel_btn_2f.pack(side='left', padx=5, pady=5)

# Floor Navigation Buttons for frame2_3f
floor_nav_frame_3f = Frame(frame2_3f, bg='#f5f6fa')
floor_nav_frame_3f.place(x=0, y=490, relwidth=1, height=60)

ff_button_3f = Button(floor_nav_frame_3f, text='1층', font=('맑은 고딕', 12, 'bold'), command=secondfh, width=8, height=2)
ff_button_3f.pack(side='left', padx=20, pady=5)
sf_button_3f = Button(floor_nav_frame_3f, text='2층', font=('맑은 고딕', 12, 'bold'), command=secondsh, width=8, height=2)
sf_button_3f.pack(side='left', padx=20, pady=5)
th_button_3f = Button(floor_nav_frame_3f, text='3층', font=('맑은 고딕', 12, 'bold'), command=secondth, width=8, height=2) # Blue for active
th_button_3f.pack(side='left', padx=20, pady=5)

# Add Reservation and Cancel buttons to frame2_3f
reserve_btn_3f = Button(floor_nav_frame_3f, text="예약", font=('맑은 고딕', 12),
                        command=lambda: make_reservation('3f'), width=4, height=2)
reserve_btn_3f.pack(side='left', padx=15, pady=5)

cancel_btn_3f = Button(floor_nav_frame_3f, text="취소", font=('맑은 고딕', 12),
                       command=lambda: cancel_reservation('3f'), width=4, height=2)
cancel_btn_3f.pack(side='left', padx=5, pady=5)


# --- End of Updated frame2_Xf design ---


# 현 주차 상태 (frame1) - 모던한 디자인
frame1.configure(bg='#f5f6fa')  # 배경색 변경

# 상단 헤더
header_frame = Frame(frame1, bg='#2c3e50', height=70)
header_frame.pack(fill='x', pady=(0, 20))
Label(header_frame, text="주차장 현황 대시보드", font=('맑은 고딕', 24, 'bold'), 
      fg='white', bg='#2c3e50').pack(pady=15)

# 실시간 정보 패널
info_panel = Frame(frame1, bg='#f5f6fa')
info_panel.pack(fill='x', padx=30, pady=(0, 20))

# 시간 및 요금 정보 (좌측)
time_pay_frame = Frame(info_panel, bg='white', relief='solid', bd=1)
time_pay_frame.pack(side='left', padx=10, fill='both', expand=True)

# 경과 시간 표시
time_display = Frame(time_pay_frame, bg='#3498db', height=40)
time_display.pack(fill='x')
Label(time_display, text=f"경과 시간: {elapsed_time}", 
      font=('맑은 고딕', 14, 'bold'), bg='#3498db', fg='white').pack(pady=8)

# 현재 요금 표시
current_pay = Frame(time_pay_frame, bg='white')
current_pay.pack(fill='x', pady=20)
Label(current_pay, text="현재 종합 요금", font=('맑은 고딕', 12), 
      bg='white').pack()
Label(current_pay, text=f"{pay:,}원", font=('맑은 고딕', 36, 'bold'), 
      bg='white', fg='#2c3e50').pack()

# 요금 정보 표시 (우측)
fee_info_frame = Frame(info_panel, bg='white', relief='solid', bd=1)
fee_info_frame.pack(side='right', padx=10, fill='both', expand=True)

fee_header = Frame(fee_info_frame, bg='#2ecc71', height=40)
fee_header.pack(fill='x')
Label(fee_header, text="요금 안내", font=('맑은 고딕', 14, 'bold'), 
      bg='#2ecc71', fg='white').pack(pady=8)

fees = [
    ("예약 요금", "5,000원"),
    ("시간당 요금", "3,000원/10분"),
    ("추가 요금", "6,000원/10분")
]

for title, amount in fees:
    fee_row = Frame(fee_info_frame, bg='white')
    fee_row.pack(fill='x', padx=15, pady=8)
    Label(fee_row, text=title, font=('맑은 고딕', 11), 
          bg='white').pack(side='left')
    Label(fee_row, text=amount, font=('맑은 고딕', 11, 'bold'), 
          bg='white', fg='#2c3e50').pack(side='right')

# 예약 시스템 (중앙)
reservation_frame = Frame(frame1, bg='white', relief='solid', bd=1)
reservation_frame.pack(fill='x', padx=30, pady=20)

# 예약 헤더
reserve_header = Frame(reservation_frame, bg='#9b59b6', height=40)
reserve_header.pack(fill='x')
Label(reserve_header, text="주차 예약 시스템", font=('맑은 고딕', 14, 'bold'), 
      bg='#9b59b6', fg='white').pack(pady=8)

# 예약 컨트롤
reserve_controls = Frame(reservation_frame, bg='white')
reserve_controls.pack(pady=15)

# 상태 표시
reservation_status = Label(reserve_controls, text="예약 대기 중", 
                         font=('맑은 고딕', 12), bg='white', fg='#7f8c8d')
reservation_status.pack(pady=5)

# 버튼 프레임
button_frame = Frame(reserve_controls, bg='white')
button_frame.pack(pady=10)

# 메인화면 예약 버튼 - 3개층에서 랜덤 배정
reserve_btn = Button(button_frame, text="예약", font=('맑은 고딕', 12),
                    command=make_reservation_random,
                    width=10, height=2, relief='flat')
reserve_btn.pack(side='left', padx=5)

cancel_btn = Button(button_frame, text="취소", font=('맑은 고딕', 12),
                   command=cancel_reservation_all,
                   width=10, height=2, relief='flat')
cancel_btn.pack(side='left', padx=5)

# 범례
legend_frame = Frame(reservation_frame, bg='white')
legend_frame.pack(pady=10)



# for symbol, text, color in legends:
#     Frame(legend_frame, width=20, bg='white').pack(side='left')
#     Label(legend_frame, text=symbol, font=('맑은 고딕', 14), 
#           fg=color, bg='white').pack(side='left')
#     Label(legend_frame, text=text, font=('맑은 고딕', 10), 
#           bg='white').pack(side='left')

Button(but_frame,text='현 주차 정보',command=firstview, width=10,height=4).pack(side='left',padx=33)
Button(but_frame,text='현 주차장 정보',command=secondview, width=10,height=4).pack(side='left',padx=33)
Button(but_frame,text='사용자 정보',command=thirdview, width=10,height=4).pack(side='left',padx=33)
Button(but_frame,text='X',font=('고딕',20),fg = 'red',command=des).place(x=1,y=1)

root.mainloop()