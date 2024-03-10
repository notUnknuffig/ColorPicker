import tkinter as tk

hex_dict = {0 : "0",
            1 : "1",
            2 : "2",
            3 : "3",
            4 : "4",
            5 : "5",
            6 : "6",
            7 : "7",
            8 : "8",
            9 : "9",
            10 : "a",
            11 : "b",
            12 : "c",
            13 : "d",
            14 : "e",
            15 : "f"}

def isNumberCallback(var):
    content = var.get()
    print(content)

def RGB_to_HEX(rgb):
    _hex = ""

    for value in rgb:
        a = value % 16
        b = value - a
        _hex += hex_dict[b/16] + hex_dict[a]

    return _hex

def HSV_to_RGB(h,s,v):
    r = 0
    g = 0
    b = 0

    c = v * s

    x = c * (1 - abs((h / 60) % 2 - 1))

    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    r += m
    g += m
    b += m
    
    print(r,g,b)
    return [round(r*255), round(g*255), round(b*255)]

def RGB_to_HSV(r,g,b):
    _r = r/255
    _g = g/255
    _b = b/255

    h = 0
    s = 0
    v = 0

    Cmax = max([_r,_g,_b])
    Cmin = min([_r,_g,_b])

    delta = Cmax - Cmin

    if delta == 0:
        h = 0
    elif Cmax == _r:
        h = 60 * (((_g - _b) / delta) % 6)
    elif Cmax == _g:
        h = 60 * (((_b - _r) / delta) + 2)
    elif Cmax == _b:
        h = 60 * (((_r - _g) / delta) + 4)
    
    if Cmax == 0:
        s = 0
    else:
        s = delta/Cmax

    v = Cmax

    return [h, round(s,4), round(v,2)]



def convert():
    global current
    global hsv_value, rgb_value, hex_value
    global color_text_1, color_text_2, color_text_3, output_1, output_2, result_color

    output_str_1 = ""
    output_str_2 = ""

    try:
        if current.get() == "RGB":
            rgb_value = []
            hsv_value = []
            hex_value = ""
            for string in [color_input_1.get(), color_input_2.get(), color_input_3.get()]:
                if len(string) >= 1:
                    value = int(string)
                    if value > 255:
                        value = 255
                else:
                    value = 0
                rgb_value.append(value)
            
            hex_value = RGB_to_HEX(rgb_value)

            hsv = RGB_to_HSV(rgb_value[0],rgb_value[1],rgb_value[2])

            output_str_1 = f"{hsv[0]}°, {round(hsv[1]*10000)/100}%, {round(hsv[2]*10000)/100}%"
            output_str_2 = f"#{hex_value}"

        elif current.get() == "HSV":
            rgb_value = []
            hex_value = ""
            h = float(color_input_1.get())
            s = float(color_input_2.get())/100
            v = float(color_input_3.get())/100
            if h > 360:
                h = h % 360
            if s > 100:
                s = 100
            if v > 100:
                v = 100
            rgb_value = HSV_to_RGB(h,s,v)

            hex_value = RGB_to_HEX(rgb_value)

            output_str_1 = f'{rgb_value[0]}, {rgb_value[1]}, {rgb_value[2]}'
            output_str_2 = f"#{hex_value}"
                    
            
        
        elif current.get() == "HEX":
            str_hex = color_input_1.get()

            if str_hex[0] == "#":
                str_hex = str_hex[1:]

            if len(str_hex) > 6:
                str_hex = str_hex[:5]

            hex_value = str_hex

            split_string = [str_hex[i:i+2] for i in range(0, len(str_hex), 2)]

            rgb_value = []

            for string in split_string:
                int_1 = list(hex_dict.keys())[list(hex_dict.values()).index(string[0])]
                int_1 *= 16
                int_2 = list(hex_dict.keys())[list(hex_dict.values()).index(string[1])]
                rgb_value.append(int_1 + int_2)
            
            hsv = RGB_to_HSV(rgb_value[0],rgb_value[1],rgb_value[2])

            output_str_1 = f'{rgb_value[0]}, {rgb_value[1]}, {rgb_value[2]}'
            output_str_2 = f"{hsv[0]}°, {round(hsv[1]*10000)/100}%, {round(hsv[2]*10000)/100}%"

        result_color.config(bg=f'#{hex_value}')

    except Exception as e:
        output_str = "Invalid Input!"
        print(f"Error: {e}")
        print(e)

    output_1.configure(state='normal')
    output_1.delete(0,"end")
    output_1.insert(0, output_str_1)
    output_1.configure(state='readonly')

    output_2.configure(state='normal')
    output_2.delete(0,"end")
    output_2.insert(0, output_str_2)
    output_2.configure(state='readonly')
            

def dropdownChange(*args):
    global current
    global color_text_1, color_text_2, color_text_3, color_input_1, color_input_2, color_input_3, output_label_1, output_label_2

    if current.get() == "RGB":
        color_text_1.config(text="R:")
        color_text_2.config(text="G:")
        color_text_3.config(text="B:")

        #color_input_1.config(text=str(rgb_value[0]))
        #color_input_2.config(text=str(rgb_value[1]))
        #color_input_3.config(text=str(rgb_value[2]))

        color_input_1.grid(row=0, column= 1)
        color_input_2.grid(row=1, column= 1)
        color_input_3.grid(row=2, column= 1)

        color_text_1.grid(row=0, column= 0)
        color_text_2.grid(row=1, column= 0)
        color_text_3.grid(row=2, column= 0)

        output_label_1.config(text="HSV:")
        output_label_2.config(text="HEX:")
    elif current.get() == "HEX":
        color_text_1.config(text="Hex:")
        color_text_2.grid_forget()
        color_text_3.grid_forget()

        color_input_1.config(text=hex_value)
        color_input_2.grid_forget()
        color_input_3.grid_forget()

        output_label_1.config(text="RGB:")
        output_label_2.config(text="HEX:")
    elif current.get() == "HSV":
        color_text_1.config(text="H:")
        color_text_2.config(text="S:")
        color_text_3.config(text="V:")

        #color_input_1.config(text=str(hsv_value[0]))
        #color_input_2.config(text=str(hsv_value[1]))
        #color_input_3.config(text=str(hsv_value[2]))

        color_input_1.grid(row=0, column= 1)
        color_input_2.grid(row=1, column= 1)
        color_input_3.grid(row=2, column= 1)

        color_text_1.grid(row=0, column= 0)
        color_text_2.grid(row=1, column= 0)
        color_text_3.grid(row=2, column= 0)

        output_label_1.config(text="RGB:")
        output_label_2.config(text="HEX:")

def main():
    global hsv_value, rgb_value, hex_value
    global current, color_text_1, color_text_2, color_text_3, color_input_1, color_input_2, color_input_3, output_label_1, output_label_2, output_1, output_2, result_color

    color_codes = ["RGB","HSV","HEX"]

    hex_value = "000000"
    hsv_value = [0,0,0]
    rgb_value = [0,0,0]


    window = tk.Tk() #Make Window...
    window.geometry("400x550") #Make Window 400x500 Units 
    window.minsize(width=500, height=600) #Convigure Minumum Size
    window.title("Colorpicker") #Set Title

    #Title
    title = tk.Label(window, text="Convert Color Formats",font=('Arial',14)) #Title the Window
    title.pack()
 
    current = tk.StringVar()
    current.set("RGB")
    current.trace("w", dropdownChange)

    dropdown = tk.OptionMenu(window, current, *color_codes)
    dropdown.pack()

    #Tabel 
    input_frame = tk.Frame(window)
    input_frame.pack(pady=10, padx=10)
    input_frame.columnconfigure(0, weight=1)
    input_frame.columnconfigure(1, weight=1)
    input_frame.columnconfigure(2, weight=1)

    #Input
    color_text_1 = tk.Label(input_frame,text="R:", font=('Arial',12))
    color_text_1.grid(row=0, column= 0)
    #color_input_1 = tk.Scale(input_frame, from_=0, to= 255, orient="horizontal")
    #color_input_1.grid(row=0, column= 1)
    #input_1 = tk.IntVar()
    #input_1.trace("w", lambda name, index,mode, var=input_1: isNumberCallback(var))
    color_input_1 = tk.Entry(input_frame, font=('Arial',12))
    color_input_1.grid(row=0, column= 1)

    color_text_2 = tk.Label(input_frame,text="G:", font=('Arial',12))
    color_text_2.grid(row=1, column= 0)
    #color_input_2 = tk.Scale(input_frame, from_=0, to= 255, orient="horizontal")
    #color_input_2.grid(row=1, column= 1)
    #input_2 = tk.IntVar()
    #input_2.trace("w", lambda name, index,mode, var=input_2: isNumberCallback(var))
    color_input_2 = tk.Entry(input_frame, font=('Arial',12))
    color_input_2.grid(row=1, column= 1)

    color_text_3 = tk.Label(input_frame,text="B:", font=('Arial',12))
    color_text_3.grid(row=2, column= 0)
    #color_input_3 = tk.Scale(input_frame, from_=0, to= 255, orient="horizontal")
    #color_input_3.grid(row=2, column= 1)
    #input_3 = tk.IntVar()
    #input_3.trace("w", lambda name, index,mode, var=input_3: isNumberCallback(var))
    color_input_3 = tk.Entry(input_frame, font=('Arial',12))
    color_input_3.grid(row=2, column= 1)

    button = tk.Button(window, text="Convert", font=('Arial',12),command=convert)
    button.pack(padx=10, pady=10)

    output_label_1 = tk.Label(input_frame,text="HSV:", font=('Arial',12))
    output_label_1.grid(row=3, column= 0, pady=10)

    output_1 = tk.Entry(input_frame, text="", font=('Arial', 12))
    output_1.configure(state='disabled')
    output_1.grid(row=3, column= 1)

    output_label_2 = tk.Label(input_frame,text="HEX:", font=('Arial',12))
    output_label_2.grid(row=4, column= 0)

    output_2 = tk.Entry(input_frame, text="", font=('Arial', 12))
    output_2.configure(state='disabled')
    output_2.grid(row=4, column= 1)

    result_color_title = tk.Label(window, text="Color:", font=('Arial',12)) #Title for the Color rectangle
    result_color_title.pack()

    result_color = tk.Canvas(window,width=300, height=300, bg=f'#{hex_value}')
    result_color.pack()

    window.mainloop() #Do Window...

main()