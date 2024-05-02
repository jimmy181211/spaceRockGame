from tkinter import *


class MsgBox:
    def __init__(self, input_obj_type):
        self.tk = Tk()
        self.tk.title("equip before the game")
        self.tk.geometry("300x120")
        self.input_obj_type = input_obj_type
        self.input_pairs = {}
        self.result_list = {}
        # add the messageboxes into self.input_pairs dictionary
        for cnt, obj in enumerate(input_obj_type):
            label = Label(self.tk, text="enter the number of " + obj)
            label.grid(row=cnt + 1, column=1, sticky="n")
            input_box = Spinbox(self.tk, values=[str(i) for i in range(20)], width=5)
            input_box.grid(row=cnt + 1, column=2, sticky="NW")
            # add the label and the input box
            self.input_pairs[label] = input_box

    def __get_val(self):
        self.result_list = {self.input_obj_type[i]: self.input_pairs[key].get() for i, key in
                            enumerate(self.input_pairs)}
        self.tk.quit()
        self.tk.destroy()

    def show(self):
        submit = Button(self.tk, text="submit", command=self.__get_val)
        submit.grid(row=3 + len(self.result_list), column=2, sticky="NW")
        self.tk.mainloop()


if __name__ == "__main__":
    msg_box = MsgBox(["coin","shield"])
    msg_box.show()
    print(msg_box.result_list)
