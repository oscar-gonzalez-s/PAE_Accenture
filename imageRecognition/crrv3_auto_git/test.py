import sys
import numpy as np
import filecmp
import matplotlib.pyplot as plt
import re

def comparation2(database_txt, test_txt, diff_txt):
    with open(database_txt,'r') as f1, open(test_txt,'r') as f2, open(diff_txt,'w') as outfile:
        for line1, line2 in zip(f1, f2):
            if line1 != line2:
                if 'N/A' in line2: #If 'X' character is printed, it indicates that neural network wasn't able to detect clothing
                    newstr = line1.strip() + 'X' + '\n'
                    print(newstr, end='', file=outfile)
                else:
                    print(line1, end='', file=outfile)  

def count_errors_mistakes(file_txt, cloth_lbl, colour_lbl):
    total_mistakes = 0
    undetected_clothes = 0
    clothing_mistakes = 0
    colour_mistakes = 0

    with open(file_txt,'r') as fp:
        for line in fp:
            line.strip()

            if ("X" in line and any(clothing in line for clothing in cloth_lbl)):
                undetected_clothes += 1
            if (any(clothing in line for clothing in cloth_lbl) and not("X" in line)):
                clothing_mistakes += 1
            if (any(colour in line for colour in colour_lbl) and not("X" in line)):
                colour_mistakes += 1

        total_mistakes = clothing_mistakes + colour_mistakes
        total_errors = total_mistakes + undetected_clothes

    return total_errors, total_mistakes, undetected_clothes, clothing_mistakes, colour_mistakes

if __name__ == '__main__':

    clothing_labels = ['camiseta_manga_corta', 'jersey', 'abrigo_manga_corta', 'abrigo_manga_larga',
                  'chaleco', 'top_tirantes_finos', 'pantalon_corto', 'pantalones', 'falda', 'vestido_manga_corta',
                  'vestido_manga_larga', 'vestido_de_chaleco', 'vestido_tirantes']

    colour_labels = ['amarillo', 'naranja', 'rosa', 'lila', 'marron', 'beige', 'negro', 'blanco', 'verde oscuro' 
                    'caqui', 'gris', 'azul claro', 'azul marino', 'verde', 'azul', 'rojo', 'granate', 
                    'verde claro'] 


    comparation2('database_prueba.txt','test_prueba.txt','diff.txt')
    total_errors, total_mistakes, undetected_clothes, clothing_mistakes, colour_mistakes = count_errors_mistakes('diff.txt', clothing_labels, colour_labels)
    print('Number of total errors: {}\nNumber of total mistakes: {}\nUndetected clothes: {}\nClothing mistakes: {}\n\
Colour mistakes: {} '.format(total_errors, total_mistakes, undetected_clothes, clothing_mistakes, colour_mistakes))

y = np.array([undetected_clothes, clothing_mistakes, colour_mistakes])
mylabels = [ "Undetected clothes", "Clothing mistakes", "Colour mistakes"]

higlight_undetected_clothes = [0.2, 0, 0]
plt.pie(y, labels = mylabels, explode = higlight_undetected_clothes)
plt.savefig('grafica_undetected_clothes.jpg')

higlight_clothing_mistakes = [0, 0.2, 0]
plt.pie(y, labels = mylabels, explode = higlight_clothing_mistakes)
plt.savefig('grafica_clothing_mistakes.jpg')

# i = 0

# for category in y:
#     myexplode = [0, 0, 0]
#     myexplode[i] = 0.2
#     fig = plt.pie(y, labels = mylabels, explode = myexplode)
#     fig.savefig('grafica' + str(category) + '.jpg')
#     i+=1

    
    # dblines = []
    # outlines = []                                    # Declare an empty list.
    # with open ('database_prueba.txt', 'rt') as db, open ('test_prueba.txt', 'rt') as out:
    #     for dbline in db:                       # For each line in the file,
    #         dblines.append(dbline.rstrip('\n'))     # strip newline and add to list.
    #     for outline in out: 
    #         outlines.append(outline.rstrip('\n'))
    #     for clothundetected_clothesent in dblines:                     # For each clothundetected_clothesent in the list,
    #         print(clothundetected_clothesent)                          # print it.
    #     for clothundetected_clothesent in outlines:                     # For each clothundetected_clothesent in the list,
    #         print(clothundetected_clothesent)                          # print it.

    #     pat = re.compile(r"\b\w*.jpg\b")  # compile regex "\bd\w*r\b" to a pattern object
    #     i = 0
    #     dbimgpos = []
    #     for clothundetected_clothesent in dblines:
    #         if pat.search(clothundetected_clothesent) != None:     # Search for the pattern. If found,
    #             dbimgpos.append(i)
    #         i+=1
        
    #     i = 0
    #     outimgpos = []
    #     for clothundetected_clothesent in outlines:
    #         if pat.search(clothundetected_clothesent) != None:     # Search for the pattern. If found,
    #             outimgpos.append(i)
    #         i+=1
        
    #     for clothundetected_clothesent in outimgpos:
    #         print(clothundetected_clothesent)
        
