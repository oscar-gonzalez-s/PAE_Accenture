import sys
import numpy as np
import filecmp
import matplotlib.pyplot as plt
import re
import numpy


def comparation2(database_txt, test_txt, diff_txt):
    with open(database_txt,'r') as f1, open(test_txt,'r') as f2, open(diff_txt,'w') as outfile:
        for line1, line2 in zip(f1, f2):
            if line1 != line2:
                if 'N/A' in line2: #If 'X' character is printed, it indicates that neural network wasn't able to detect clothing
                    newstr = line1.strip() + 'X' + '\n'
                    print(newstr, end='', file=outfile)
                else:
                    print(line1, end='', file=outfile)  

def count_errors_mistakes(diff_txt, database_txt, cloth_lbl, colour_lbl):
    total_elements = 0
    total_errors = 0
    total_mistakes = 0
    undetected_clothes = 0
    clothing_mistakes = 0
    colour_mistakes = 0

    with open(database_txt,'r') as fp:
        for line in fp:
            line.strip()
            if not('.jpg' in line or 'N/A' in line or line=='\n' ):
                total_elements += 1

    with open(diff_txt,'r') as fp:
        for line in fp:
            line.strip()
            if ("X" in line and any(clothing in line for clothing in cloth_lbl)):
                undetected_clothes += 1
            if (any(clothing in line for clothing in cloth_lbl) and not("X" in line)):
                clothing_mistakes += 1
            #If a cloth is not detected, no color will be detected so it is counted only as undetected_cloth:
            if (any(colour in line for colour in colour_lbl) and not("X" in line)):
                colour_mistakes += 1

        total_mistakes = clothing_mistakes + colour_mistakes
        total_errors = total_mistakes + undetected_clothes

    return total_errors, total_mistakes, undetected_clothes, clothing_mistakes, colour_mistakes, total_elements

def make_autopct(errors_values):
    def my_autopct(pct):
        total = sum(errors_values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
    return my_autopct

if __name__ == '__main__':

    clothing_labels = ['camiseta_manga_corta', 'jersey', 'abrigo_manga_corta', 'abrigo_manga_larga',
                  'chaleco', 'top_tirantes_finos', 'pantalon_corto', 'pantalones', 'falda', 'vestido_manga_corta',
                  'vestido_manga_larga', 'vestido_de_chaleco', 'vestido_tirantes']

    colour_labels = ['amarillo', 'naranja', 'rosa', 'lila', 'marron', 'beige', 'negro', 'blanco', 'verde oscuro' 
                    'caqui', 'gris', 'azul claro', 'azul marino', 'verde', 'azul', 'rojo', 'granate', 
                    'verde claro'] 


    comparation2('database.txt','test.txt','diff_final.txt')
    total_errors, total_mistakes, undetected_clothes, clothing_mistakes, colour_mistakes, total_elements = count_errors_mistakes('diff_final.txt', 'database.txt', clothing_labels, colour_labels)
    print('Number of total elements: {}\nNumber of total errors: {}\nNumber of total mistakes: {}\nUndetected clothes: {}\nClothing mistakes: {}\n\
Colour mistakes: {} '.format(
    total_elements, #Clothes and colors that are detectable
    total_errors, #Sum of (mistakenly detected colors and clothes ) and non detected clothes
    total_mistakes, #Sum of mistakenly detected colors and clothes
    undetected_clothes,  #Non detected clothes
    clothing_mistakes, #Mistakenly detected clothes 
    colour_mistakes)) #Mistakenly detected colors

#If a cloth is not detected, no color will be detected so it is counted only as undetected_cloth
general_values = np.array([total_elements-total_errors, undetected_clothes, total_mistakes])
general_labels = ["Detected elements", "Undetected elements", "Mistaken elements"]

colors = ['yellowgreen', 'gold', 'lightskyblue']

plt.pie(general_values, labels = general_labels, colors=colors, autopct=make_autopct(general_values), shadow=True)
plt.savefig('Grafica General.jpg')
plt.close()

errors_values = np.array([undetected_clothes, clothing_mistakes, colour_mistakes])
errors_labels = [ "Undetected clothes", "Clothing mistakes", "Colour mistakes"]

colors = ['yellowgreen', 'gold', 'lightskyblue']

i = 0
for category in errors_labels:
    myexplode = [0, 0, 0]
    myexplode[i] = 0.2
    plt.pie(errors_values, labels = errors_labels, explode = myexplode, colors=colors, autopct=make_autopct(errors_values), shadow=True)
    plt.savefig('Grafica ' + category + '.jpg')
    plt.close()
    i+=1

    
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
        
