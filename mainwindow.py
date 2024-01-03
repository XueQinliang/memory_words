import tkinter as tk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import sqlite3
import numpy as np

cos_index = np.load("./data/cos_index.npy")
jaro_index = np.load("./data/jaro_index.npy")
conn = sqlite3.connect("./data/data.db")
c = conn.cursor()
result = c.execute("select count(*) from words;")
word_count = result.fetchall()[0][0]
result = c.execute("select count(*) from words where count >= 3;")
learned_word_count = result.fetchall()[0][0]
result = c.execute("select * from process;")
process_count = result.fetchall()[0][0]
result = c.execute("select * from words where id = ?;", (process_count,))
result = result.fetchall()[0]
# 创建一个简单的Tkinter窗口
window = tk.Tk()
window.title("快背单词")
window.resizable(0, 0)
width = 1042
height = 600
window.geometry(str(width) + "x" + str(height))

word = tk.StringVar()
en = tk.StringVar()
us = tk.StringVar()
meaning = tk.StringVar()
score = tk.StringVar()
learned_str_count = tk.StringVar()
word.set(result[1])
en.set(result[2])
us.set(result[3])
meaning.set(result[4])
this_count = result[5]
score.set(str(this_count)+"/3")
learned_str_count.set(str(learned_word_count)+"/"+str(word_count))

#插入背景图片
canvas = tk.Canvas(window, width=width, height=height)
canvas.pack()
im = Image.open('back.jpg')
im = im.resize((width, height))
img = ImageTk.PhotoImage(im)
canvas.create_image(0, 0, anchor="nw", image=img)
# 添加icon
icon = Image.open('logo.jpg')
icon = icon.resize((100, 100))
icon = ImageTk.PhotoImage(icon)
window.iconphoto(False, icon)

# 装饰器
def logger(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper

# 增加按钮
@logger
def on_click_next():
    global process_count
    global main_input_box, input_box_list, jump_input_box
    global word, en, us, meaning, this_count, answer, spell, score
    process_count += 1
    if process_count > word_count:
        process_count = 1
    result = c.execute("select * from words where id = ?;", (process_count,))
    result = result.fetchall()[0]
    word.set(result[1])
    en.set(result[2])
    us.set(result[3])
    meaning.set(result[4])
    this_count = result[5]
    score.set(str(this_count)+"/3")
    # word, en, us, meaning = result[1], result[2], result[3], result[4]
    c.execute("update process set id =?;", (process_count,))
    print(word.get(), en.get(), us.get(), meaning.get(), process_count)
    answer.set('')
    spell.set('')
    main_input_box.delete(0, 'end')
    jump_input_box.delete(0, 'end')
    for i in range(len(input_box_list)):
        input_box_list[i].destroy()
    input_box_list = []
    for i in range(len(word.get())):
        input_box = tk.Entry(window, width=1, bg='#fdf2eb')
        input_box.place(x=150 + i * 30, y=260)
        input_box.config(font=("微软雅黑", 26))
        input_box_list.append(input_box)
    conn.commit()

nextbutton = tk.Button(window, text='下一个', width=10, height=2, bg='#fdf2eb', command=on_click_next)
nextbutton.place(x=500, y=415)

@logger
def on_click_last():
    global process_count
    global main_input_box, input_box_list, jump_input_box
    global word, en, us, meaning, this_count, answer, spell, score
    process_count -= 1
    if process_count < 1:
        process_count = word_count
    result = c.execute("select * from words where id = ?;", (process_count,))
    result = result.fetchall()[0]
    word.set(result[1])
    en.set(result[2])
    us.set(result[3])
    meaning.set(result[4])
    this_count = result[5]
    score.set(str(this_count)+"/3")
    # word, en, us, meaning = result[1], result[2], result[3], result[4]
    c.execute("update process set id =?;", (process_count,))
    print(word.get(), en.get(), us.get(), meaning.get(), process_count)
    answer.set('')
    spell.set('')
    main_input_box.delete(0, 'end')
    jump_input_box.delete(0, 'end')
    for i in range(len(input_box_list)):
        input_box_list[i].destroy()
    input_box_list = []
    for i in range(len(word.get())):
        input_box = tk.Entry(window, width=1, bg='#fdf2eb')
        input_box.place(x=150 + i * 30, y=260)
        input_box.config(font=("微软雅黑", 26))
        input_box_list.append(input_box)
    conn.commit()

lastbutton = tk.Button(window, text='上一个', width=10, height=2, bg='#fdf2eb', command=on_click_last)
lastbutton.place(x=350, y=415)

answer = tk.StringVar()
spell = tk.StringVar()
label_spell = tk.Label(window, textvariable=spell, bg='#fdf2eb')
label_spell.place(x=30, y=310)
label_word = tk.Label(window, textvariable=answer, bg='#fdf2eb')
label_word.place(x=150, y=310)

@logger
def on_click_check():
    global word, answer, this_count, process_count, spell, score, word_count, learned_str_count
    global main_input_box
    answer.set(word.get())
    if word.get() == main_input_box.get():
        spell.set('拼写正确：')
        label_spell.config(font=("微软雅黑", 22), fg="green")
        label_word.config(font=("微软雅黑", 22), fg="green")
        this_count += 1
        score.set(str(this_count)+"/3")
        c.execute("update words set count =? where id =?;", (this_count, process_count))
    else:
        spell.set('正确拼写：')
        label_spell.config(font=("微软雅黑", 22), fg="red")
        label_word.config(font=("微软雅黑", 22), fg="red")
        this_count = 0
        score.set(str(this_count)+"/3")
        c.execute("update words set count =? where id =?;", (this_count, process_count))
        c.execute("update words set count =? where id =?;", (this_count, process_count))
    result = c.execute("select count(*) from words where count >= 3;")
    learned_word_count = result.fetchall()[0][0]
    learned_str_count.set(str(learned_word_count)+"/"+str(word_count))
    conn.commit()

checkbutton = tk.Button(window, text='检查', width=10, height=2, bg='#fdf2eb', command=on_click_check)
checkbutton.place(x=200, y=415)

@logger
def on_click_ok():
    global word, process_count, this_count, score, word_count, learned_str_count
    this_count = 3
    score.set(str(this_count)+"/3")
    c.execute("update words set count =? where id =?;", (this_count, process_count))
    result = c.execute("select count(*) from words where count >= 3;")
    learned_word_count = result.fetchall()[0][0]
    learned_str_count.set(str(learned_word_count)+"/"+str(word_count))
    conn.commit()
    
okbutton = tk.Button(window, text='我已掌握', width=10, height=2, bg='#fdf2eb', command=on_click_ok)
okbutton.place(x=50, y=415)

@logger
def on_click_jump_jaro():
    global process_count
    global main_input_box, input_box_list, jump_input_box
    global word, en, us, meaning, this_count, answer, spell, score
    process_count = int(jaro_index[process_count])
    result = c.execute('''select * from words where id = ?;''', (process_count,))
    result = result.fetchall()
    result = result[0]
    word.set(result[1])
    en.set(result[2])
    us.set(result[3])
    meaning.set(result[4])
    this_count = result[5]
    score.set(str(this_count)+"/3")
    # word, en, us, meaning = result[1], result[2], result[3], result[4]
    c.execute("update process set id = ?;", (process_count,))
    print(word.get(), en.get(), us.get(), meaning.get(), process_count)
    answer.set('')
    spell.set('')
    main_input_box.delete(0, 'end')
    jump_input_box.delete(0, 'end')
    for i in range(len(input_box_list)):
        input_box_list[i].destroy()
    input_box_list = []
    for i in range(len(word.get())):
        input_box = tk.Entry(window, width=1, bg='#fdf2eb')
        input_box.place(x=150 + i * 30, y=260)
        input_box.config(font=("微软雅黑", 26))
        input_box_list.append(input_box)
    conn.commit()

@logger
def on_click_jump_cos():
    global process_count
    global main_input_box, input_box_list, jump_input_box
    global word, en, us, meaning, this_count, answer, spell, score
    process_count = int(cos_index[process_count])
    result = c.execute('''select * from words where id = ?;''', (process_count,))
    result = result.fetchall()
    result = result[0]
    word.set(result[1])
    en.set(result[2])
    us.set(result[3])
    meaning.set(result[4])
    this_count = result[5]
    score.set(str(this_count)+"/3")
    # word, en, us, meaning = result[1], result[2], result[3], result[4]
    c.execute("update process set id = ?;", (process_count,))
    print(word.get(), en.get(), us.get(), meaning.get(), process_count)
    answer.set('')
    spell.set('')
    main_input_box.delete(0, 'end')
    jump_input_box.delete(0, 'end')
    for i in range(len(input_box_list)):
        input_box_list[i].destroy()
    input_box_list = []
    for i in range(len(word.get())):
        input_box = tk.Entry(window, width=1, bg='#fdf2eb')
        input_box.place(x=150 + i * 30, y=260)
        input_box.config(font=("微软雅黑", 26))
        input_box_list.append(input_box)
    conn.commit()

jump_button_jaro = tk.Button(window, text='形近词跳转', width=10, height=2, bg='#fdf2eb', command=on_click_jump_jaro)
jump_button_jaro.place(x=650, y=415)
jump_button_cos = tk.Button(window, text='近义词跳转', width=10, height=2, bg='#fdf2eb', command=on_click_jump_cos)
jump_button_cos.place(x=800, y=415)

label = tk.Label(window, text='可以按回车键检查，按↓键或者→键到下一个单词，按↑键或者←到上一个单词', bg='#fdf2eb')
label.place(x=50, y=465)
label.config(font=("微软雅黑", 22))

@logger
def key_press(event):
    global process_count
    global word, en, us, meaning
    global main_input_box
    if event.keysym == 'Left' or event.keysym == 'Up':
        on_click_last()
    if event.keysym =='Right' or event.keysym == 'Down':
        on_click_next()
    if event.keysym == 'Return' and main_input_box.get() != '':
        on_click_check()

# 绑定动作到键盘
window.bind('<Key>', key_press)

# 添加文本
label = tk.Label(window, text='掌握程度：', bg='#fdf2eb')
label.place(x=30, y=90)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, text='学习进度：', bg='#fdf2eb')
label.place(x=200, y=90)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, text='中文释义：', bg='#fdf2eb')
label.place(x=30, y=130)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, text='美式音标：', bg='#fdf2eb')
label.place(x=30, y=170)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, text='英式音标：', bg='#fdf2eb')
label.place(x=30, y=210)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, text='单词拼写：', bg='#fdf2eb')
label.place(x=30, y=260)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, text='这里输入：', bg='#fdf2eb')
label.place(x=30, y=360)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, textvariable=score, bg='#fdf2eb')
label.place(x=150, y=90)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, textvariable=learned_str_count, bg='#fdf2eb')
label.place(x=320, y=90)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, textvariable=meaning, bg='#fdf2eb')
label.place(x=150, y=130)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, textvariable=us, bg='#fdf2eb')
label.place(x=150, y=170)
label.config(font=("微软雅黑", 22))
label = tk.Label(window, textvariable=en, bg='#fdf2eb')
label.place(x=150, y=210)
label.config(font=("微软雅黑", 22))

# 添加n个输入框，依次可以输入n个字母
input_box_list = []
for i in range(len(word.get())):
    input_box = tk.Entry(window, width=1, bg='#fdf2eb')
    input_box.place(x=150 + i * 30, y=260)
    input_box.config(font=("微软雅黑", 26))
    input_box_list.append(input_box)

main_input_box = tk.Entry(window, width=20, bg='#fdf2eb')
main_input_box.place(x=150, y=360)
main_input_box.config(font=("微软雅黑", 26))

@logger
def on_click_jump():
    global process_count
    global main_input_box, input_box_list, jump_input_box
    global word, en, us, meaning, this_count, answer, spell, score
    jump_word = jump_input_box.get()
    if jump_word == '':
        return
    result = c.execute("select * from words where word = ?;", (jump_word,))
    result = result.fetchall()
    if len(result) == 0:
        messagebox.showinfo('提示', '没有找到该单词')
        jump_input_box.delete(0, 'end')
        return
    result = result[0]
    process_count = result[0]
    word.set(result[1])
    en.set(result[2])
    us.set(result[3])
    meaning.set(result[4])
    this_count = result[5]
    score.set(str(this_count)+"/3")
    # word, en, us, meaning = result[1], result[2], result[3], result[4]
    c.execute("update process set id =?;", (process_count,))
    print(word.get(), en.get(), us.get(), meaning.get(), process_count)
    answer.set('')
    spell.set('')
    main_input_box.delete(0, 'end')
    jump_input_box.delete(0, 'end')
    for i in range(len(input_box_list)):
        input_box_list[i].destroy()
    input_box_list = []
    for i in range(len(word.get())):
        input_box = tk.Entry(window, width=1, bg='#fdf2eb')
        input_box.place(x=150 + i * 30, y=260)
        input_box.config(font=("微软雅黑", 26))
        input_box_list.append(input_box)
    conn.commit()

jump_button = tk.Button(window, text='跳转到：', width=6, height=2, bg='#fdf2eb', command=on_click_jump)
jump_button.place(x=550, y=360)
jump_input_box = tk.Entry(window, width=15, bg='#fdf2eb')
jump_input_box.place(x=650, y=360)
jump_input_box.config(font=("微软雅黑", 26))

@logger
def on_entry_change(event):
    global input_box_list
    global main_input_box
    value = main_input_box.get() # 获取输入框的值
    # 把value依次填入输入框列表中
    if len(value) > len(word.get()):
        value = value[:len(word.get())]
        # 设置input_box的值
        main_input_box.delete(0, 'end')
        main_input_box.insert(0, value)
    for i in range(len(input_box_list)):
        input_box_list[i].delete(0, 'end')
    for i in range(len(value)):
        input_box_list[i].insert(0, value[i])
main_input_box.bind('<KeyRelease>', on_entry_change)
main_input_box.bind('<Key-BackSpace>', on_entry_change)

# 启动主事件循环
window.mainloop()
conn.close()