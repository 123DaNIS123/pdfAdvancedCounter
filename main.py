import PyPDF2
import os


def flatten_list(some_list:list):
    flat_ls = []
    for i in some_list:
        print(type(i))
        print(str(type(i)))
        print(type(i)==str, "str")
        print(type(i)==list, "list")
        print(str(type(i))=="str")
        if type(i) == str:
            print("it is a string")
            flat_ls.append(i)
        else:
            print("IT IS a LIST!!")
            flat_ls.append(*flatten_list(i))
            print(flat_ls, "123")
    return flat_ls

def is_pdf(x, dest, check):
    if x[-4:] in [".pdf", ".PDF"]:
        if os.path.isfile(os.path.join(dest, x)):
            print(x, "returned a file!")
            return x
    elif(check):
        if os.path.isdir(os.path.join(dest, x)):
            pdf_files = list(filter(lambda y: is_pdf(y, os.path.join(dest, x), check), os.listdir(os.path.join(dest, x))))
            print(os.listdir(os.path.join(dest, x)), "wayoncheck")
            print(pdf_files, "changed")
            return pdf_files

def calculate_all(destination:str, result:str, err:int, checkSubs:bool):
    pdf_files = list(map(lambda x: is_pdf(x, destination, checkSubs), os.listdir(destination)))
    print(pdf_files, "calculate_all")
    pdf_files = list(filter(lambda x: x!=None, pdf_files))
    print(pdf_files, "after filtering")
    if pdf_files == []:
        raise Exception("No pdf files was found in the selected folder")
    if set(type(x).__name__ for x in pdf_files) != set(["str"]):
        pdf_files = flatten_list(pdf_files)
        print(pdf_files, "flattering")
    print(pdf_files, "after flattering")
    types_dict = dict()
    types_dict_pages = dict()

    for pdf_file in pdf_files:
        pdfReader = PyPDF2.PdfReader(os.path.join(destination, pdf_file))
        totalPages = len(pdfReader.pages)
        for page in range(totalPages):
            box = pdfReader.pages[page].mediabox
            pFormat = (box.width, box.height)
            if pFormat in types_dict:
                types_dict[pFormat] += 1
                types_dict_pages[pFormat].add(page+1)
            else:
                types_dict[pFormat] = 1
                types_dict_pages[pFormat] = set([page+1])

    standard_types = [[74, 105, "A10", 0, set()],
                    [105, 147, "A9", 0, set()],
                    [147, 210, "A8", 0, set()],
                    [210, 298, "A7", 0, set()],
                    [298, 420, "A6", 0, set()],
                    [420, 595, "A5", 0, set()],
                    [595, 842,"A4", 0, set()],
                    [842, 1191,"A3", 0, set()],
                    [1191, 1684,"A2", 0, set()],
                    [1684, 2384,"A1", 0, set()],
                    [2384, 3370,"A0", 0, set()],
                    [3370, 4768, "2A0", 0, set()],
                    [4768, 6741, "4A0", 0, set()]]

    err = 26 # in pixels
    notcommon_count = 1
    for key, value in types_dict.items():
        all_standard_x = list(map(lambda x: abs(x[0]-key[0]), standard_types))
        all_standard_y = list(map(lambda x: abs(x[1]-key[1]), standard_types))
        min_index_x = all_standard_x.index(min(all_standard_x))
        min_index_y = all_standard_y.index(min(all_standard_y))
        if all_standard_x[min_index] < err:
            standard_types[min_index][3] += value
            standard_types[min_index][4].update(types_dict_pages[key])
        else:
            standard_types.append([key[0], key[1], f"not common №{notcommon_count}", value])
    with open(f"{result}\\result.txt", "w") as file:
        for i in standard_types:
            file.write(f"Format: {i[2]} | Count: {i[3]} | Size in px(72ppi): ({i[0]}, {i[1]}) | Pages: {i[4]}\n")
