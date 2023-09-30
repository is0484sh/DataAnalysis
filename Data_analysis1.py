import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib


matplotlib.use("TkAgg")

selected_color = (0, 0, 255)

def open_color_chooser_and_file_dialog():
    global selected_color
    color = colorchooser.askcolor(initialcolor=selected_color, parent=main_window)
    if color[1]: 
        selected_color = color[1]
        open_file_dialog()

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("All files", "*.*")], parent=main_window)

    if file_path:
        df = pd.read_csv(file_path)

        data_columns = df.columns
        selected_column = choose_data_column(data_columns)

        if selected_column:
            selected_visualization = visualization_choice.get()
            process_selected_file(df, selected_column, selected_visualization)

def choose_data_column(data_columns):
    data_column_choice = tk.StringVar(value=data_columns[0])  
    column_window = tk.Toplevel(main_window)

    data_column_label = tk.Label(column_window, text="데이터 컬럼(데이터 종류) 선택:")
    data_column_label.pack()

    data_column_option_menu = tk.OptionMenu(column_window, data_column_choice, *data_columns)
    data_column_option_menu.pack()

    def on_ok_button():
        column_window.destroy()

    ok_button = tk.Button(column_window, text="확인", command=on_ok_button)
    ok_button.pack()

    column_window.transient(main_window)
    column_window.grab_set()
    column_window.wait_window(column_window)

    return data_column_choice.get()

def process_selected_file(df, selected_column, selected_visualization):
    try:
        print(f"선택한 데이터 컬럼(데이터 종류): {selected_column}")
        plt.figure(figsize=(10, 6))
        if selected_visualization == "히스토그램":
            plot_histogram(df, selected_column)
        elif selected_visualization == "선 그래프":
            plot_line_chart(df, selected_column)
        elif selected_visualization == "막대 그래프":
            plot_bar_chart(df, selected_column)
    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {file_path}")
    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {e}")



def plot_histogram(df, column_to_plot):
    plot_title = f'히스토그램: {column_to_plot}'
    plt.hist(df[column_to_plot], bins=20, edgecolor=selected_color)
    plt.title(plot_title)
    plt.xticks([]) 
    plt.yticks([])  
    plt.show()

def plot_line_chart(df, column_to_plot):
    plot_title = f'선 그래프: {column_to_plot}'
    plt.plot(df[column_to_plot], color=selected_color)
    plt.title(plot_title)
    plt.xticks([])  
    plt.yticks([]) 
    plt.show()

def plot_bar_chart(df, column_to_plot):
    plot_title = f'막대 그래프: {column_to_plot}'
    df[column_to_plot].value_counts().plot(kind='bar', color=selected_color)
    plt.title(plot_title)
    plt.xticks([])
    plt.yticks([])
    plt.show()

def show_instructions():
    instructions = "사용 방법:\n\n1. 원하는 시각화 방식을 선택하세요.\n2. '색상 선택' 버튼을 눌러 그래프 색상을 선택하세요.\n3. '파일 선택' 버튼을 눌러 데이터를 담은 파일을 선택하세요. \n Warning: 이 프로그램은 엄청나게 방대한 데이터는 재대로 시각화가 되지 않습니다. 간단한 데이터로만 사용해 주십시오."
    messagebox.showinfo("사용 방법", instructions)

main_window = tk.Tk()
main_window.title("데이터 시각화 프로그램")

show_instructions() 

start_menu = tk.Frame(main_window)
start_menu.grid(row=0, column=0, padx=20, pady=20)

file_select_button = tk.Button(start_menu, text="파일 선택", command=open_color_chooser_and_file_dialog)
file_select_button.pack()

visualization_choice = tk.StringVar(value="히스토그램")

visualization_frame = tk.Frame(main_window)
visualization_frame.grid(row=1, column=0, padx=20, pady=10)

visualization_label = tk.Label(visualization_frame, text="시객화 선택:")
visualization_label.grid(row=0, column=0)

visualization_options = ["히스토그램", "선 그래프", "막대 그래프"]

for idx, option in enumerate(visualization_options):
    radio = tk.Radiobutton(visualization_frame, text=option, variable=visualization_choice, value=option)
    radio.grid(row=idx + 1, column=0)

main_window.mainloop()
