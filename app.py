import pandas as pd
from tkinter import *
from tkinter import scrolledtext
from io import StringIO
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def display1():
    def read_original_csv():
        with open('datalists.csv', 'r') as file:
            content = file.read()
        text_area.delete(1.0, END)
        text_area.insert(END, content)
        format_csv_content(content)

    def modify_and_display_csv():
        df = pd.read_csv('datalists.csv')

        df['has_value'] = df.notna().all(1).astype(int)

        df = df.sort_values(by='has_value', ascending=False)
        df = df.drop_duplicates()
        df = df.fillna(0)

        def replace_slash_with_dash(series):
            return series.apply(lambda x: str(x).replace("/", "-") if isinstance(x, str) else x)

        df['Latest_Launch'] = replace_slash_with_dash(df['Latest_Launch'])

        df = df.drop(columns=['has_value'])

        df.to_csv("output.csv", index=False)
        button1.configure(state=NORMAL)
        button2.configure(state=NORMAL)
        with open('output.csv', 'r') as file:
            content = file.read()
        text_area.delete(1.0, END)
        text_area.insert(END, content)
        format_csv_content(content)

    def format_csv_content(content):
        text_area.delete(1.0, END)
        lines = content.strip().split('\n')
        formatted_lines = ['\n']
        for line in lines:
            if line.strip():
                parts = line.strip().split(',')
                formatted_parts = [part.strip() for part in parts]
                formatted_lines.append(','.join(formatted_parts) + '\n')
                formatted_lines.append(''.join(['-' for _ in formatted_parts]) + '\n')
            else:
                formatted_lines.append('\n')
        text_area.insert(END, ''.join(formatted_lines), ('header', 'column_separator'))

    window = Tk()
    window.attributes('-fullscreen', True)
    window.title("CSV Viewer")

    window.configure(background='#58ddfe')

    button_frame = Frame(window, bg='#d9d9d9')
    button_frame.pack(pady=20)

    def close_window():
        window.destroy()

    button_exit = Button(window, text="Exit", command=close_window, font=('Arial', 20), width=20, bg="white", fg="red",
                         highlightbackground="black",activebackground="red", padx=30, pady=10)
    button_exit.pack(side=TOP, padx=20)

    original_button = Button(button_frame, text="Original CSV file", command=read_original_csv, font=('Arial', 14),
                                bg='#e6e6e6', padx=30, pady=10,highlightbackground="green",activebackground="#9683EC")
    original_button.pack(side=LEFT, padx=20)

    modified_button = Button(button_frame, text="Modified CSV file", command=modify_and_display_csv,
                                font=('Arial', 14), bg='#e6e6e6', padx=30, pady=10,highlightbackground="green",activebackground="#9683EC")
    modified_button.pack(side=LEFT, padx=20)

    text_area_frame = Frame(window, bg='#d9d9d9')
    text_area_frame.pack(fill=BOTH, expand=True, pady=20)

    text_area = scrolledtext.ScrolledText(text_area_frame, wrap=WORD, width=80, height=20, font=('Arial', 12),
                                          bg='#f5f5f5')
    text_area.pack(fill=BOTH, expand=True)

    text_area.tag_config('header', foreground='#005a9c', font=('Arial', 12, 'bold'))
    text_area.tag_config('column_separator', foreground='#000000')


def display2():
    new_window=Tk()
    new_window.configure(bg="#ffe6f5")
    new_window.attributes('-fullscreen', True)
    new_window.title("Statistics Viewer")
    label = Label(new_window, text="\t\t Check out these Statistical Values", font=('Arial', 35))
    label.place(x=0,y=0)
    label = Label(new_window, text="Check out Mean : ", font=('Arial', 20))
    label.place(x=0, y=200)
    label = Label(new_window, text="Check out Median : ", font=('Arial', 20))
    label.place(x=0, y=400)
    label = Label(new_window, text="Check out Mode : ", font=('Arial', 20))
    label.place(x=0, y=600)
    def displaym1():
        data = pd.read_csv("output.csv")
        mean_sales = data.groupby("Manufacturer")["Sales_in_thousands"].mean().reset_index()
        mean_sales1 = data.groupby("Manufacturer")["Power_perf_factor"].mean().reset_index()
        mean_sales2 = data.groupby("Manufacturer")["__year_resale_value"].mean().reset_index()
        mean_combined = pd.merge(mean_sales, mean_sales1, on="Manufacturer")
        mean_combined = pd.merge(mean_combined, mean_sales2, on="Manufacturer")
        mean_combined.to_csv("Mean.csv", index=False)
        mean=pd.read_csv("Mean.csv")
        button3.configure(state=NORMAL)
        code_display = scrolledtext.ScrolledText(new_window, font=('Arial', 20))
        code_display.place(x=500, y=200, relwidth=0.8, relheight=0.8)
        code_display.insert(END,mean)
    button0 = Button(new_window, text='Mean', font=('Comic Sans', 20, 'bold'), command=displaym1, bg="white",fg="black",activebackground="#89CFF0")
    button0.place(x=300, y=200)
    def displaym2():
        data = pd.read_csv("output.csv")
        median_sales = data.groupby("Manufacturer")["Sales_in_thousands"].median().reset_index()
        median_sales1 = data.groupby("Manufacturer")["Power_perf_factor"].median().reset_index()
        median_sales2 = data.groupby("Manufacturer")["__year_resale_value"].median().reset_index()
        median_combined = pd.merge(median_sales, median_sales1, on="Manufacturer")
        median_combined = pd.merge(median_combined, median_sales2, on="Manufacturer")
        median_combined.to_csv("median.csv", index=False)
        median=pd.read_csv("median.csv")
        button3.configure(state=NORMAL)
        code_display = scrolledtext.ScrolledText(new_window, font=('Arial', 20))
        code_display.place(x=500, y=200, relwidth=0.8, relheight=0.8)
        code_display.insert(END,median)
    button1 = Button(new_window, text='Median', font=('Comic Sans', 20, 'bold'), command=displaym2, bg="white",fg="black",activebackground="#89CFF0")
    button1.place(x=300, y=400)
    def displaym3():
        data = pd.read_csv("output.csv")
        mode_sales = data.groupby("Manufacturer")["Sales_in_thousands"].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None).reset_index()
        mode_sales1 = data.groupby("Manufacturer")["Power_perf_factor"].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None).reset_index()
        mode_sales2 = data.groupby("Manufacturer")["__year_resale_value"].apply(lambda x: x.mode().iloc[0] if not x.mode().empty else None).reset_index()
        mode_combined = pd.merge(mode_sales, mode_sales1, on="Manufacturer")
        mode_combined = pd.merge(mode_combined, mode_sales2, on="Manufacturer")
        mode_combined.to_csv("mode.csv", index=False)
        mode=pd.read_csv("mode.csv")
        button3.configure(state=NORMAL)
        code_display = scrolledtext.ScrolledText(new_window, font=('Arial', 20))
        code_display.place(x=500, y=200, relwidth=0.8, relheight=0.8)
        code_display.insert(END,mode)
    button2 = Button(new_window, text='Mode', font=('Comic Sans', 20, 'bold'), command=displaym3, bg="white",fg="black",activebackground="#89CFF0")
    button2.place(x=300, y=600)
    def close_window():
        new_window.destroy()

    button_exit = Button(new_window, text="Exit", command=close_window, font=('Arial', 20), width=20, bg="white", fg="red",
                         highlightbackground="black",activebackground="red")
    button_exit.place(x=100, y=750)

def display3():

    class OptionMenuWithFunctions:
        def __init__(self, master, options, functions):
            self.selected_option = StringVar(master)
            self.selected_option.set(options[0])  # Default selection

            self.function_dict = {option: func for option, func in zip(options, functions)}

            self.menu = OptionMenu(master, self.selected_option, *options, command=self.execute_selected_function)
            self.menu.pack()

            self.result_label = Label(master, text="Selected option: None")
            self.result_label.pack()

        def execute_selected_function(self, value):
            selected_function = self.function_dict.get(value)
            if selected_function:
                selected_function()
                self.result_label.config(text=f"Selected option: {value}")

    def function1():
        sns.barplot(x="Manufacturer", y="Sales_in_thousands", data=df)
        plt.ylabel("Sales in thousands")
        plt.xticks(rotation=45, ha='right', rotation_mode='anchor')
        plt.show()

    def function2():
        sns.scatterplot(x="Horsepower", y="Price_in_thousands", data=df)
        plt.ylabel("Price in thousands")
        plt.show()

    def function3():
        sns.boxplot(data=df, x="Vehicle_type", y="__year_resale_value")
        plt.xlabel("Vehicle Type")
        plt.ylabel("Resale value")
        plt.show()

    def function4():
        sns.barplot(x="Manufacturer", y="Fuel_capacity", data=df)
        plt.ylabel("Fuel Capacity")
        plt.xticks(rotation=45, ha='right', rotation_mode='anchor')
        plt.show()

    def function5():
        df = pd.read_csv("output.csv")
        df = df.select_dtypes(include=['int64', 'float64'])
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
        plt.title('Heatmap of Correlation Matrix')
        plt.show()

    root = Tk()
    root.configure(bg="#ffe6f5")
    root.attributes("-fullscreen", True)
    root.title("Dropdown List with Functions Example")

    df = pd.read_csv("output.csv")

    def close_window():
        root.destroy()

    button_exit = Button(root, text="Exit", command=close_window, font=('Arial', 20), width=20, bg="white", fg="red",
                         highlightbackground="black", activebackground="red", relief="raised", bd=5)
    button_exit.place(x=700,y=900)

    options = ["Model vs Sale", "Horsepower vs Price", "Vehicle Type vs Resale Price", "Model vs Fuel Capacity",
               "Heat Map"]

    functions = [function1, function2, function3, function4, function5]

    option_menu_with_functions = OptionMenuWithFunctions(root, options, functions)


def display4():

    df = pd.read_csv("Modified.csv")

    def meansalesbar():
        column1 = 'Manufacturer'
        column2 = 'Sales_in_thousands'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Bar Plot of Manufacturer vs Mean Sales')
        plt.show()

    def meanpowerbar():
        column1 = 'Manufacturer'
        column2 = 'Power_perf_factor'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Bar Plot of Manufacturer vs Mean Sales')
        plt.show()

    def meanresalebar():
        column1 = 'Manufacturer'
        column2 = '__year_resale_value'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Bar Plot of Manufacturer vs Mean Sales')
        plt.show()

    def mediansalesbar():
        column1 = 'Manufacturer'
        column2 = 'Sales'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Bar Plot of Manufacturer vs Mean Sales')
        plt.show()

    def medianresalebar():
        column1 = 'Manufacturer'
        column2 = 'Power'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Bar Plot of Manufacturer vs Mean Sales')
        plt.show()

    def medianpowerbar():
        column1 = 'Manufacturer'
        column2 = 'Resale'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Bar Plot of Manufacturer vs Mean Sales')
        plt.show()

    def modesalesbar():
        column1 = 'Manufacturer'
        column2 = 'Sales1'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Bar Plot of Manufacturer vs Mean Sales')
        plt.show()

    def moderesalebar():
        column1 = 'Manufacturer'
        column2 = 'Power1'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Bar Plot of Manufacturer vs Mean Sales')
        plt.show()

    def modepowerbar():
        column1 = 'Manufacturer'
        column2 = 'Resale1'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Bar Plot of Manufacturer vs Mean Sales')
        plt.show()

    def meansalesbox():
        column1 = 'Manufacturer'
        column2 = 'Sales_in_thousands'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Box Plot of Manufacturer vs Mean Sales')
        plt.show()

    def meanpowerbox():
        column1 = 'Manufacturer'
        column2 = 'Power_perf_factor'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Box Plot of Manufacturer vs Mean Power')
        plt.show()

    def meanresalebox():
        column1 = 'Manufacturer'
        column2 = '__year_resale_value'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Box Plot of Manufacturer vs Mean Resale Value')
        plt.show()

    def mediansalesbox():
        column1 = 'Manufacturer'
        column2 = 'Sales'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Box Plot of Manufacturer vs Median Sales')
        plt.show()

    def medianresalebox():
        column1 = 'Manufacturer'
        column2 = 'Power'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Box Plot of Manufacturer vs Median Resale Value')
        plt.show()

    def medianpowerbox():
        column1 = 'Manufacturer'
        column2 = 'Resale'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Box Plot of Manufacturer vs Median Power')
        plt.show()

    def modesalesbox():
        column1 = 'Manufacturer'
        column2 = 'Sales1'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Box Plot of Manufacturer vs Mode Sales')
        plt.show()

    def moderesalebox():
        column1 = 'Manufacturer'
        column2 = 'Power1'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Box Plot of Manufacturer vs Mode Resale Value')
        plt.show()

    def modepowerbox():
        column1 = 'Manufacturer'
        column2 = 'Resale1'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Box Plot of Manufacturer vs Mode Power')
        plt.show()

    def meansalesscatter():
        column1 = 'Manufacturer'
        column2 = 'Sales_in_thousands'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Scatter Plot of Manufacturer vs Mean Sales')
        plt.show()

    def meanpowerscatter():
        column1 = 'Manufacturer'
        column2 = 'Power_perf_factor'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Scatter Plot of Manufacturer vs Mean Power')
        plt.show()

    def meanresalescatter():
        column1 = 'Manufacturer'
        column2 = '__year_resale_value'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Scatter Plot of Manufacturer vs Mean Resale Value')
        plt.show()

    def mediansalesscatter():
        column1 = 'Manufacturer'
        column2 = 'Sales'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Scatter Plot of Manufacturer vs Median Sales')
        plt.show()

    def medianresalescatter():
        column1 = 'Manufacturer'
        column2 = 'Power'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Scatter Plot of Manufacturer vs Median Resale Value')
        plt.show()

    def medianpowerscatter():
        column1 = 'Manufacturer'
        column2 = 'Resale'
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=column1, y=column2, data=df, palette="viridis")
        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Scatter Plot of Manufacturer vs Median Power')
        plt.show()

    def modesalesscatter():
        column1 = 'Manufacturer'
        column2 = 'Sales1'

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))

        sns.scatterplot(x=column1, y=column2, data=df, palette="viridis")

        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Scatter Plot of Manufacturer vs Mode Sales')

        plt.show()

    def moderesalescatter():
        column1 = 'Manufacturer'
        column2 = 'Power1'

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))

        sns.scatterplot(x=column1, y=column2, data=df, palette="viridis")

        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Scatter Plot of Manufacturer vs Mode Resale Value')

        plt.show()

    def modepowerscatter():
        column1 = 'Manufacturer'
        column2 = 'Resale1'

        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))

        sns.scatterplot(x=column1, y=column2, data=df, palette="viridis")

        plt.xlabel(column1)
        plt.ylabel(column2)
        plt.title('Scatter Plot of Manufacturer vs Mode Power')

        plt.show()

    def function1():
        sns.barplot(x="Manufacturer", y="Sales_in_thousands", data=df)
        plt.ylabel("Sales in thousands")
        plt.xticks(rotation=45, ha='right', rotation_mode='anchor')
        plt.show()

    def function2():
        sns.scatterplot(x="Horsepower", y="Price_in_thousands", data=df)
        plt.ylabel("Price in thousands")
        plt.show()

    def function3():
        sns.boxplot(data=df, x="Vehicle_type", y="__year_resale_value")
        plt.xlabel("Vehicle Type")
        plt.ylabel("Resale value")
        plt.show()

    def function4():
        sns.barplot(x="Manufacturer", y="Fuel_capacity", data=df)
        plt.ylabel("Fuel Capacity")
        plt.xticks(rotation=45, ha='right', rotation_mode='anchor')
        plt.show()

    def execute_sub_function(selected_option, sub_option):
        if (selected_option == "Manufacturer vs Mean Sales" and sub_option == "Bar Plot"):
            meansalesbar()
        elif (selected_option == "Manufacturer vs Mean Power Factor" and sub_option == "Bar Plot"):
            meanpowerbar()
        elif (selected_option == "Manufacturer vs Mean Resale value" and sub_option == "Bar Plot"):
            meanresalebar()
        elif (selected_option == "Manufacturer vs Median Sales" and sub_option == "Bar Plot"):
            mediansalesbar()
        elif (selected_option == "Manufacturer vs Median Power Factor" and sub_option == "Bar Plot"):
            medianpowerbar()
        elif (selected_option == "Manufacturer vs Median Resale value" and sub_option == "Bar Plot"):
            medianresalebar()
        elif (selected_option == "Manufacturer vs Mode Sales" and sub_option == "Bar Plot"):
            modesalesbar()
        elif (selected_option == "Manufacturer vs Mode Power Factor" and sub_option == "Bar Plot"):
            modepowerbar()
        elif (selected_option == "Manufacturer vs Mode Resale value" and sub_option == "Bar Plot"):
            moderesalebar()
        elif (selected_option == "Manufacturer vs Mean Sales" and sub_option == "Box Plot"):
            meansalesbox()
        elif (selected_option == "Manufacturer vs Mean Power Factor" and sub_option == "Box Plot"):
            meanpowerbox()
        elif (selected_option == "Manufacturer vs Mean Resale value" and sub_option == "Box Plot"):
            meanresalebox()
        elif (selected_option == "Manufacturer vs Median Sales" and sub_option == "Box Plot"):
            mediansalesbox()
        elif (selected_option == "Manufacturer vs Median Power Factor" and sub_option == "Box Plot"):
            medianpowerbox()
        elif (selected_option == "Manufacturer vs Median Resale value" and sub_option == "Box Plot"):
            medianresalebox()
        elif (selected_option == "Manufacturer vs Mode Sales" and sub_option == "Box Plot"):
            modesalesbox()
        elif (selected_option == "Manufacturer vs Mode Power Factor" and sub_option == "Box Plot"):
            modepowerbox()
        elif (selected_option == "Manufacturer vs Mode Resale value" and sub_option == "Box Plot"):
            moderesalebox()
        elif (selected_option == "Manufacturer vs Mean Sales" and sub_option == "Scatter Plot"):
            meansalesscatter()
        elif (selected_option == "Manufacturer vs Mean Power Factor" and sub_option == "Scatter Plot"):
            meanpowerscatter()
        elif (selected_option == "Manufacturer vs Mean Resale value" and sub_option == "Scatter Plot"):
            meanresalescatter()
        elif (selected_option == "Manufacturer vs Median Sales" and sub_option == "Scatter Plot"):
            mediansalesscatter()
        elif (selected_option == "Manufacturer vs Median Power Factor" and sub_option == "Scatter Plot"):
            medianpowerscatter()
        elif (selected_option == "Manufacturer vs Median Resale value" and sub_option == "Scatter Plot"):
            medianresalescatter()
        elif (selected_option == "Manufacturer vs Mode Sales" and sub_option == "Scatter Plot"):
            modesalesscatter()
        elif (selected_option == "Manufacturer vs Mode Power Factor" and sub_option == "Scatter Plot"):
            modepowerscatter()
        elif (selected_option == "Manufacturer vs Mode Resale value" and sub_option == "Scatter Plot"):
            moderesalescatter()

    def on_option_selected(*args):
        selected_option = main_dropdown.get()
        sub_options = sub_dropdowns.get(selected_option, [])

        sub_dropdown.set('')
        sub_dropdown_menu['menu'].delete(0, 'end')

        if sub_options:
            sub_label.pack()
            sub_dropdown_menu.pack()

            for option in sub_options:
                sub_dropdown_menu['menu'].add_command(label=option,
                                                      command=lambda opt=option: execute_sub_function(selected_option,
                                                                                                      opt))
        else:
            sub_label.pack_forget()
            sub_dropdown_menu.pack_forget()

    root = Tk()
    root.configure(bg="#ffe6f5")
    root.attributes("-fullscreen",True)
    root.title("Hierarchical Dropdown Example")

    def close_window():
        root.destroy()

    button_exit = Button(root, text="Exit", command=close_window, font=('Arial', 20), width=20, bg="white", fg="red",
                         highlightbackground="black", activebackground="red", relief="raised", bd=5)
    button_exit.pack()

    options = ['Company vs Sales', 'Manufacturer vs Mean Sales', 'Manufacturer vs Mean Power Factor',
               'Manufacturer vs Mean Resale value', 'Manufacturer vs Mode Sales', 'Manufacturer vs Mode Power Factor',
               'Manufacturer vs Mode Resale value', 'Manufacturer vs Median Sales',
               'Manufacturer vs Median Power Factor', 'Manufacturer vs Median Resale value']
    main_dropdown = StringVar(root)
    main_dropdown.set(options[0])

    main_dropdown_menu = OptionMenu(root, main_dropdown, *options)
    main_dropdown_menu.pack()
    sub_dropdowns = {
        'Manufacturer vs Mean Sales': ['Bar Plot', 'Box Plot', 'Scatter Plot'],
        'Manufacturer vs Mean Power Factor': ['Bar Plot', 'Box Plot', 'Scatter Plot'],
        'Manufacturer vs Mean Resale value': ['Bar Plot', 'Box Plot', 'Scatter Plot'],
        'Manufacturer vs Median Sales': ['Bar Plot', 'Box Plot', 'Scatter Plot'],
        'Manufacturer vs Median Power Factor': ['Bar Plot', 'Box Plot', 'Scatter Plot'],
        'Manufacturer vs Median Resale value': ['Bar Plot', 'Box Plot', 'Scatter Plot'],
        'Manufacturer vs Mode Sales': ['Bar Plot', 'Box Plot', 'Scatter Plot'],
        'Manufacturer vs Mode Power Factor': ['Bar Plot', 'Box Plot', 'Scatter Plot'],
        'Manufacturer vs Mode Resale value': ['Bar Plot', 'Box Plot', 'Scatter Plot'],
    }
    sub_label = Label(root, text="Select Sub-Option:")
    sub_dropdown = StringVar(root)
    sub_dropdown_menu = OptionMenu(root, sub_dropdown, '')
    main_dropdown.trace('w', on_option_selected)

window = Tk()
window.configure(bg="#ffe6f5")
window.title("DataViz")
window.attributes('-fullscreen', True)

label0=Label(window,text='''DataViz - Data Analysis & Visualization Tool''',font=('Aerial',45,'bold'))
label0.configure(bg="#004cbf",fg="white",padx=20,pady=20,relief="ridge",bd=20)
label0.place(x=225,y=50)
label5=Label(window,text="Exploratory Data Analysis with Python Libraries - Simple GUI",font=('Aerial',26,'bold'))
label5.configure(bg="#ffe6f5",fg="black")
label5.place(x=350,y=280)
label4 = Label(window, text="Click here to view the Original and Cleaned Data Sheet", font=('Arial', 25, 'bold'))
label4.configure(bg="#ffe6f5", fg="black")
label4.place(x=25, y=400)
label4 = Label(window, text="Click Here to View the Statistical Values", font=('Arial', 25, 'bold'))
label4.configure(bg="#ffe6f5", fg="black")
label4.place(x=25, y=500)
label4 = Label(window, text="Click Here to View the Analytical Graphs", font=('Arial', 25, 'bold'))
label4.configure(bg="#ffe6f5", fg="black")
label4.place(x=25, y=600)
label5 = Label(window, text="Click Here to View the Statistical Graphs", font=('Arial', 25, 'bold'))
label5.configure(bg="#ffe6f5", fg="black")
label5.place(x=25, y=700)
label6=Label(window,text='''Done By:- 
Tharunkrishna M''',font=('Times New Roman',25,'bold'))
label6.configure(bg="#004cbf",fg="#ffe6f5",padx=20,pady=20,relief="ridge",bd=20)
label6.place(x=1225,y=650)
button = Button(window, text='Check it out', font=('Comic Sans', 20, 'bold'), command=display1, bg="white",fg="black",activebackground="#40E0D0",relief="raised",bd=5)
button.place(x=925, y=400)
button1 = Button(window, text='Check it out', font=('Comic Sans', 20, 'bold'), command=display2, bg="white",fg="black",activebackground="#40E0D0",relief="raised",bd=5,state=DISABLED)
button1.place(x=925, y=500)
button2 = Button(window, text='Check it out', font=('Comic Sans', 20, 'bold'), command=display3,bg="white",fg="black",activebackground="#40E0D0",relief="raised",bd=5,state=DISABLED)
button2.place(x=925, y=600)
button3 = Button(window, text='Check it out', font=('Comic Sans', 20, 'bold'),command=display4, bg="white",fg="black",activebackground="#40E0D0",relief="raised",bd=5,state=DISABLED)
button3.place(x=925, y=700)
def close_window():
    window.destroy()
button_exit = Button(window, text="Exit", command=close_window, font=('Arial', 20), width=20,bg="white",fg="red",highlightbackground="black",activebackground="red",relief="raised",bd=5)
button_exit.place(x=550,y=900)
window.mainloop()